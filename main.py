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
    """Check if all required environment variables and files are present."""
    logger.info("Current working directory: %s", os.getcwd())
    
    # Check if we're running on Heroku
    is_heroku = 'DYNO' in os.environ
    logger.info("Running on Heroku: %s", is_heroku)
    
    if not is_heroku:
        # Only check for .env file in local development
        env_path = os.path.join(os.getcwd(), '.env')
        logger.info("Looking for .env file in: %s", env_path)
        if not os.path.exists(env_path):
            logger.error("❌ .env file not found!")
            logger.error("Please create a .env file with the required environment variables.")
            return False
    
    # Check required environment variables
    required_vars = ['TELEGRAM_BOT_TOKEN', 'ARTEMIS_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error("❌ Missing required environment variables: %s", ', '.join(missing_vars))
        if is_heroku:
            logger.error("Please set these variables in your Heroku config vars.")
        else:
            logger.error("Please add these variables to your .env file.")
        return False
    
    # Check config directory and artemis_mappings.json
    config_dir = os.path.join(os.getcwd(), 'config')
    mappings_file = os.path.join(config_dir, 'artemis_mappings.json')
    
    if not os.path.exists(config_dir):
        logger.error("❌ config directory not found!")
        return False
        
    if not os.path.exists(mappings_file):
        logger.error("❌ artemis_mappings.json not found in config directory!")
        return False
    
    logger.info("✅ Environment check passed!")
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
    
    try:
        logger.info("Creating Telegram application...")
        # Create the Application
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        
        logger.info("Adding handlers...")
        # Add handlers
        application.add_handler(CommandHandler("start", welcome_message))
        application.add_handler(CommandHandler("help", help_command))
        
        # Handle private messages
        application.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Handle group messages that start with =art
        application.add_handler(MessageHandler(
            filters.ChatType.GROUPS & 
            filters.TEXT & 
            ~filters.COMMAND, 
            handle_group_message
        ))
        
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

if __name__ == "__main__":
    main()
