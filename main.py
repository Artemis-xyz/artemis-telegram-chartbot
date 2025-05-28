#!/usr/bin/env python3
"""
Artemis Analytics Telegram Chart Bot

A Telegram bot for generating and sharing charts from Artemis Analytics.
Command format: <metric> <artemis_id> <symbol> <asset_type> <time_period> [granularity] [options]

Example: fees ethereum eth chain 1w 1d
"""

import os
import sys
import signal
import logging
from pathlib import Path
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import LOG_LEVEL, LOG_FORMAT, LOG_FILE
from artemisbot.handlers.message_handlers import (
    help_command,
    handle_message,
    handle_group_message,
    welcome_message,
    command_handler
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not set in environment variables")

def check_environment():
    """Check if all required environment variables and directories are set up correctly."""
    # Print current working directory and .env file location
    logger.info(f"Current working directory: {os.getcwd()}")
    env_path = os.path.join(os.getcwd(), '.env')
    logger.info(f"Looking for .env file in: {env_path}")

    # Check if .env file exists
    if not os.path.exists(env_path):
        logger.error("❌ .env file not found!")
        logger.error("Please create a .env file in the project root with the following variables:")
        logger.error("TELEGRAM_BOT_TOKEN=your_telegram_bot_token")
        logger.error("ARTEMIS_API_KEY=your_artemis_api_key")
        return False

    # Verify required environment variables
    required_vars = ['TELEGRAM_BOT_TOKEN', 'ARTEMIS_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please ensure these are set in your .env file")
        return False

    # Check if logs directory exists
    logs_dir = Path('logs')
    if not logs_dir.exists():
        logger.info("Creating logs directory...")
        logs_dir.mkdir(exist_ok=True)

    # Check if config directory exists
    config_dir = Path('config')
    if not config_dir.exists():
        logger.error("❌ Config directory not found!")
        logger.error("Please ensure the config directory exists with required configuration files")
        return False

    # Check if artemis_mappings.json exists
    mappings_file = config_dir / 'artemis_mappings.json'
    if not mappings_file.exists():
        logger.error("❌ artemis_mappings.json not found in config directory!")
        logger.error("Please ensure the config/artemis_mappings.json file exists")
        return False

    logger.info("✅ Environment check passed successfully")
    return True

def signal_handler(signum, frame):
    """Handle shutdown signals."""
    logger.info("Received shutdown signal")
    sys.exit(0)

def main():
    """Start the bot."""
    logger.info("Initializing bot...")
    
    # Check environment first
    if not check_environment():
        logger.error("❌ Environment check failed. Please fix the issues above and try again.")
        sys.exit(1)
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create lock file
    lock_file = "/tmp/artemis_telegram_bot.lock"
    if os.path.exists(lock_file):
        logger.error("❌ Another instance is already running")
        logger.error("If this is incorrect, please remove the lock file: " + lock_file)
        sys.exit(1)
        
    with open(lock_file, "w") as f:
        f.write(str(os.getpid()))
    
    try:
        logger.info("Creating Telegram application...")
        # Create the Application
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        
        logger.info("Adding handlers...")
        # Add handlers
        application.add_handler(CommandHandler("start", welcome_message))
        application.add_handler(CommandHandler("help", help_command))
        # Handle private messages
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        # Handle group messages that start with =art
        application.add_handler(MessageHandler(filters.ChatType.GROUPS & filters.TEXT & ~filters.COMMAND, handle_group_message))
        # Handle new chat members (for welcome message)
        application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_message))
        
        # Start the bot
        logger.info("Starting bot...")
        application.run_polling()
        
    except Exception as e:
        logger.error(f"❌ Error starting bot: {str(e)}")
        logger.error("Please check the following:")
        logger.error("1. Your TELEGRAM_BOT_TOKEN is valid")
        logger.error("2. You have an active internet connection")
        logger.error("3. The bot has been added to your group (if using group features)")
        import traceback
        logger.error("Full error traceback:")
        logger.error(traceback.format_exc())
        sys.exit(1)
        
    finally:
        # Clean up lock file
        if os.path.exists(lock_file):
            os.remove(lock_file)

if __name__ == "__main__":
    main()
