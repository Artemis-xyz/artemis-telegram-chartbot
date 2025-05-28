# 🚀 Artemis Telegram Chart Bot

> A powerful Telegram bot for generating beautiful charts and market insights from Artemis Analytics.

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)](https://t.me/your_bot_username)

## ✨ Features

- 📊 Generate beautiful charts for various crypto metrics (price, volume, TVL, fees, etc.)
- 🔄 Support for multiple assets and time periods
- 📰 News analysis and market summaries
- 👥 Group chat support with `=art` prefix
- 🎨 Beautiful chart visualizations with AI-powered analysis

## 🛠️ Setup

### Prerequisites

- 🐍 Python 3.11 or higher
- 🤖 Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- 🔑 Artemis Analytics API Key
- 📰 CryptoPanic API Key (for news feature)
- 🧠 OpenAI API Key (for news analysis)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Artemis-xyz/artemis-telegram-chartbot.git
cd artemis-telegram-chartbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your API keys and settings
nano .env  # or use your preferred text editor
```

#### Required Environment Variables
| Variable | Description | Source |
|----------|-------------|--------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token | [@BotFather](https://t.me/BotFather) |
| `ARTEMIS_API_KEY` | Your Artemis Analytics API key | [Artemis Analytics](https://artemis.xyz) |
| `CRYPTOPANIC_API_KEY` | Your CryptoPanic API key | [CryptoPanic](https://cryptopanic.com/developers/api/) |
| `OPENAI_API_KEY` | Your OpenAI API key | [OpenAI Platform](https://platform.openai.com/api-keys) |

#### Optional Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug logging | `false` |
| `LOG_LEVEL` | Set the log level | `INFO` |

### Running Locally

```bash
python main.py
```

### 🚀 Deploying to Heroku

1. Create a new Heroku app:
```bash
heroku create your-app-name
```

2. Set up environment variables on Heroku:
```bash
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set ARTEMIS_API_KEY=your_key
heroku config:set CRYPTOPANIC_API_KEY=your_key
heroku config:set OPENAI_API_KEY=your_key
```

3. Deploy to Heroku:
```bash
git push heroku master
```

## 📱 Usage

### Private Chat Commands

- `/start` - Start the bot
- `/help` - Show help message

### Chart Commands

Format: `<metric> <asset> <time_period> <granularity> [%]`

#### Examples
- `price solana 1w 1d` - Daily Solana price for the last week
- `fees ethereum 3m 1d` - Daily Ethereum fees for the last 3 months
- `tvl bitcoin 1y 1w %` - Weekly Bitcoin TVL as percentage for the last year

### Group Chat Commands

In group chats, start your command with `=art`:
- `=art price solana 1m 1d`
- `=art news` - Get market news summary
- `=art news bitcoin` - Get Bitcoin-specific news

### 📊 Available Metrics

| Metric | Description |
|--------|-------------|
| `price` | Price charts |
| `volume` | Trading volume |
| `tvl` | Total Value Locked |
| `fees` | Protocol fees |
| `revenue` | Revenue |
| `mc` | Market cap |
| `txns` | Transaction count |
| `daa` | Daily Active Addresses |
| `dau` | Daily Active Users |
| `fdmc` | Fully Diluted Market Cap |

### ⏱️ Time Periods

| Period | Description |
|--------|-------------|
| `1w` | 1 week |
| `mtd` | Month to date |
| `1m` | 1 month |
| `3m` | 3 months |
| `6m` | 6 months |
| `ytd` | Year to date |
| `1y` | 1 year |
| `all` | All time |

### 📈 Granularity

| Granularity | Description |
|-------------|-------------|
| `1d` | Daily |
| `1w` | Weekly |
| `1m` | Monthly |

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by the Artemis Team