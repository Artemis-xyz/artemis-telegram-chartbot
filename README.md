# 🚀 Artemis Telegram Chartbot

A Telegram bot that generates charts and provides market news summaries using the Artemis API.

## ✨ Features
- Generate charts for various metrics (price, TVL, etc.)
- Get market news summaries
- Support for both private and group chats

## 🚀 Quick Start
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/artemis-telegram-chartbot.git
   cd artemis-telegram-chartbot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your credentials:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   ARTEMIS_API_KEY=your_artemis_api_key
   OPENAI_API_KEY=your_openai_api_key
   CRYPTOPANIC_API_KEY=your_cryptopanic_api_key
   ```

4. Run the bot:
   ```bash
   python3 main.py
   ```

## 📝 Usage
- In private chat: `/chart <metric> <ticker> <time_period> <granularity>`
- In group chat: `=art <metric> <ticker> <time_period> <granularity>`
- For news: `=art news`

### Examples
- `/chart price solana 1w 1d` - Daily Solana price for the last week
- `/chart fees ethereum 3m 1d` - Daily Ethereum fees for the last 3 months
- `/chart tvl bitcoin 1y 1w %` - Weekly Bitcoin TVL as percentage for the last year
- `=art price solana 1m 1d` - Daily Solana price for the last month in a group chat
- `=art news` - Get a market news summary

## 🚀 Deployment
### GitHub
1. Commit your changes:
   ```bash
   git add .
   git commit -m "Your commit message"
   ```

2. Push to GitHub:
   ```bash
   git push origin main
   ```

### Heroku
1. Install the Heroku CLI and login:
   ```bash
   heroku login
   ```

2. Create a Heroku app (if not already done):
   ```bash
   heroku create your-app-name
   ```

3. Set environment variables on Heroku:
   ```bash
   heroku config:set TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   heroku config:set ARTEMIS_API_KEY=your_artemis_api_key
   heroku config:set OPENAI_API_KEY=your_openai_api_key
   ```

4. Deploy to Heroku:
   ```bash
   git push heroku main
   ```

## 📄 License
MIT