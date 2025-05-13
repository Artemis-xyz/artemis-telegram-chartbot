from typing import List
from telegram import Update, Message, Bot
from telegram.ext import ContextTypes
from artemisbot.utils.command_parser import parse_command
from artemisbot.chart.chart_generator import ChartGenerator
import logging

# Initialize ChartGenerator
chart_generator = ChartGenerator()

async def process_chart_command(update: Update, context: ContextTypes.DEFAULT_TYPE, 
                      metrics: List[str], tickers_raw: List[str], asset_type: str, 
                      time_period: str, granularity: str, is_percentage: bool,
                      is_group: bool = False) -> None:
    """
    Process a chart command and respond with the appropriate chart.
    
    Args:
        update: Telegram update object
        context: Telegram context object
        metrics: List of metrics to chart
        tickers_raw: List of tickers to chart
        asset_type: Asset type (CHAIN, APPLICATION, etc.)
        time_period: Time period for the chart
        granularity: Data granularity
        is_percentage: Whether to display as percentages
        is_group: Whether this is a group chat message
    """
    status_message = await update.message.reply_text(f"📊 Generating chart for {', '.join(metrics)} of {', '.join(tickers_raw)}... \n\nPlease wait while I fetch the data and analyze it for you.")
    
    try:
        # Generate chart using ChartGenerator
        chart_image, chart_url, title, analysis = chart_generator.generate_chart(
            metrics, tickers_raw, asset_type, time_period, granularity, is_percentage
        )
        
        # Format the caption with the analysis, ensuring it never exceeds Telegram's 1024 character limit
        max_caption_length = 1024
        base_caption = f"*{title}*\n\n*Summary:* "
        # Reserve space for base_caption
        reserved = len(base_caption)
        max_analysis_length = max_caption_length - reserved
        safe_analysis = analysis[:max_analysis_length]
        caption = f"{base_caption}{safe_analysis}"
        
        # Send successful chart with analysis
        await update.message.reply_photo(
            photo=chart_image,
            caption=caption,
            parse_mode="Markdown"
        )
        await status_message.delete()
        
    except ValueError as e:
        await status_message.delete()
        await update.message.reply_text(str(e))
    except Exception as e:
        await status_message.delete()
        await update.message.reply_text(
            f"❌ Error: {str(e)}\n\n"
            f"Please try again later."
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Process incoming messages and generate charts based on user commands.
    """
    message_text = update.message.text.strip()
    parts = message_text.split()
    
    # Only process messages that start with a valid metric
    valid_metrics = ["price", "volume", "tvl", "fees", "revenue", "mc", "txns", "daa", "dau", "fdmc"]
    
    # If message is too short or doesn't start with a valid metric, ignore it completely
    if len(parts) < 4 or parts[0].lower() not in valid_metrics:
        return
    
    try:
        metrics, tickers_raw, asset_type, time_period, granularity, is_percentage = parse_command(message_text)
        
        await process_chart_command(
            update, context, metrics, tickers_raw, asset_type, time_period, granularity, is_percentage
        )
    except ValueError as e:
        await update.message.reply_text(
            f"Error: {str(e)}\n\n"
            f"Format: <metric> [vs <metric>] <asset> <time_period> <granularity> [%]\n"
            f"Example: price vs tvl solana 1w 1d"
        )


async def handle_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle messages in group chats."""
    print(f"Received group message: {update.message.text}")  # Debug log
    
    # Only process messages that start with '=art'
    if not update.message.text or not update.message.text.strip().startswith('=art'):
        print("Message doesn't start with =art, ignoring")  # Debug log
        return
        
    # Remove the '=art' prefix and process the command
    command_text = update.message.text[4:].strip()
    if not command_text:
        print("Empty command after =art, ignoring")  # Debug log
        return
        
    print(f"Processing command: {command_text}")  # Debug log
    parts = command_text.split()
    if len(parts) < 1:
        print("Command too short, ignoring")  # Debug log
        return

    # Handle news command
    if parts[0].lower() == 'news':
        await handle_news_command(update, context, parts[1:] if len(parts) > 1 else [])
        return
        
    # Only process messages that start with a valid metric
    valid_metrics = ["price", "volume", "tvl", "fees", "revenue", "mc", "txns", "daa", "dau", "fdmc"]
    if parts[0].lower() not in valid_metrics:
        print(f"Invalid metric: {parts[0]}")  # Debug log
        return
        
    try:
        metrics, tickers_raw, asset_type, time_period, granularity, is_percentage = parse_command(command_text, is_group=True)
        
        await process_chart_command(
            update, context, metrics, tickers_raw, asset_type, time_period, granularity, is_percentage, is_group=True
        )
    except ValueError as e:
        print(f"Error processing command: {str(e)}")  # Debug log
        await update.message.reply_text(
            f"Error: {str(e)}\n\n"
            f"Format: =art <metric> [vs <metric>] <asset> <time_period> <granularity> [%]\n"
            f"Example: =art price vs tvl solana 1w 1d"
        )


async def handle_news_command(update: Update, context: ContextTypes.DEFAULT_TYPE, args: List[str]) -> None:
    """
    Handle the news command to get market news summary.
    
    Args:
        update: Telegram update object
        context: Telegram context object
        args: List of arguments (optional asset identifier)
    """
    status_message = await update.message.reply_text("📰 Fetching latest market news... \n\nPlease wait while I analyze the market news.")
    
    try:
        # Get the asset identifier if provided
        asset_id = args[0].lower() if args else None
        
        # Generate news summary using ChatGPT
        from artemisbot.news.news_analyzer import NewsAnalyzer
        news_analyzer = NewsAnalyzer()
        summary = await news_analyzer.get_market_news(asset_id)
        
        # Send the news summary
        await update.message.reply_text(
            f"*Market News Summary*\n\n{summary}",
            parse_mode="Markdown"
        )
        await status_message.delete()
        
    except Exception as e:
        await status_message.delete()
        await update.message.reply_text(
            f"❌ Error: {str(e)}\n\n"
            f"Please try again later."
        )


async def welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Send a welcome message when the bot is added to a group chat.
    
    Args:
        update: Telegram update
        context: CallbackContext
    """
    try:
        # Make sure we have the required attributes
        if not update or not update.message or not update.message.new_chat_members:
            return
            
        # Get information about the new member
        new_members = update.message.new_chat_members
        
        # Get our bot's user ID
        try:
            bot_id = context.bot.id
        except (AttributeError, Exception) as e:
            return
        
        # Only proceed if our bot is one of the new members
        if any(member.id == bot_id for member in new_members):
            # Get the chat name for a personalized welcome
            chat_name = update.effective_chat.title or "this group" if update.effective_chat else "this group"
            
            # Send a beautifully formatted welcome message
            await update.message.reply_text(
                f"🌟 *Hello {chat_name}!* 🌟\n\n"
                f"Thanks for adding me to your group! I'm your Artemis Analytics Chart Bot, ready to generate beautiful crypto market visualizations right here in the chat.\n\n"
                
                f"📈 *What I can do for you:*\n"
                f"Generate charts for fees, price, volume, TVL, revenue, and more for various crypto assets.\n\n"
                
                f"👉 *How to use me:*\n"
                f"Just type `=art` followed by your chart request, like:\n\n"
                
                f"```\n"
                f"=art fees ethereum eth chain 1m 1d\n"
                f"=art price solana sol chain 3m\n"
                f"=art tvl uniswap uni application 1y 1w\n"
                f"```\n\n"
                
                f"The format is: `=art <metric> <artemis_id> <symbol> <asset_type> <time_period> [granularity]`\n\n"
                
                f"👋 Get started by trying one of the examples above!\n"
                f"📖 For more details, any member can message me directly with /help",
                parse_mode="Markdown"
            )
    except Exception as e:
        pass


async def command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Redirects commands to the appropriate handlers.
    
    Args:
        update: Telegram update
        context: CallbackContext
    """
    # Extract the command
    command = update.message.text.split()[0][1:].lower()  # Remove '/' and make lowercase
    
    # Route to the appropriate handler
    if command == 'start':
        await start_command(update, context)
    elif command == 'help':
        await help_command(update, context)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /start command - welcome new users.
    
    Args:
        update: Telegram update
        context: CallbackContext
    """
    await update.message.reply_text(
        "🔍 Welcome to Artemis Analytics Chart Bot! 📊\n\n"
        "I can generate charts from Artemis Analytics for you.\n\n"
        "The command format is:\n"
        "<metric> <artemis_id> <symbol> <asset_type> <time_period> [granularity] [options]\n\n"
        "Example: fees ethereum eth chain 1w 1d\n"
        "In group chats, start with 'art', like: art fees ethereum eth chain 1w 1d\n"
        "For more details, use /help"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /help command - provide detailed instructions.
    
    Args:
        update: Telegram update
        context: CallbackContext
    """
    await update.message.reply_text(
        "📊 Artemis Analytics Chart Bot\n\n"
        "Format: <metric> [vs <metric>] <asset> <time_period> <granularity> [%]\n\n"
        "Examples:\n"
        "• price solana 1w 1d\n"
        "• fees ethereum 3m 1d\n"
        "• price vs tvl solana 1y 1d\n"
        "• fees vs revenue ethereum 6m 1w %\n\n"
        "Metrics: price, volume, tvl, fees, revenue, mc, tx, fc\n"
        "Time Periods: 1w, mtd, 1m, 3m, 6m, ytd, 1y, all\n"
        "Granularity: 1d, 1w, 1m\n\n"
        "In group chats, start with '=art '",
        parse_mode='Markdown'
    )