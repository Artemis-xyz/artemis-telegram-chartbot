"""Configuration settings and constants for the Artemis Telegram Bot."""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ARTEMIS_API_KEY = os.getenv("ARTEMIS_API_KEY")
BOT_USERNAME = "@artemis_chartbot"

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = os.getenv("LOG_FILE", "logs/artemisbot.log")

# Chart configuration
CHART_TIMEOUT = int(os.getenv("CHART_TIMEOUT", "10"))  # seconds
CHART_WINDOW_SIZE = (1920, 1080)
CHART_RENDER_DELAY = int(os.getenv("CHART_RENDER_DELAY", "2"))  # seconds

# Asset configuration
ASSET_MAPPINGS_FILE = os.getenv("ASSET_MAPPINGS_FILE", "config/artemis_mappings.json")

# Artemis URL constants
BASE_URL = "https://app.artemis.xyz/chart-builder/"
DEFAULT_URL_PARAMS: Dict[str, Any] = {
    "id": "",
    "isOwner": False,
    "isPrivate": False,
    "isFavorite": False,
    "title": "Metric Comparison",
    "description": "",
    "period": "",  # Will be set based on user input
    "previewUrl": "",
    "granularity": "",  # Will be set based on user input
    "smaPeriod": "0",
    "series": []
}

# Time period mapping
TIME_PERIOD_MAP: Dict[str, str] = {
    "1w": "WEEKLY",
    "1m": "MONTHLY", 
    "3m": "THREE_MONTHS",
    "6m": "SIX_MONTHS",
    "1y": "ONE_YEAR",
    "ytd": "YEAR_TO_DATE",
    "all": "MAX"
}

# Granularity mapping
GRANULARITY_MAP: Dict[str, str] = {
    "1d": "DAILY",
    "1w": "WEEKLY",
    "1m": "MONTHLY"
}

# Asset type mapping
ASSET_TYPE_MAP: Dict[str, str] = {
    "CHAIN": "CHAIN",
    "APPLICATION": "APPLICATION"
}

# Metric mapping for URL parameters
METRIC_MAP: Dict[str, str] = {
    "fees": "fees",
    "fee": "fees",
    "tvl": "tvl",
    "volume": "volume",
    "vol": "volume", 
    "marketcap": "marketCap",
    "mcap": "marketCap",
    "price": "price",
    "revenue": "revenue",
    "revs": "revenue",
    "rev": "revenue",
    "transactions": "txns",
    "txns": "txns",
    "daa": "dau",
    "dau": "dau",
}

# Selenium configuration
SELENIUM_TIMEOUT = int(os.getenv("SELENIUM_TIMEOUT", "30"))  # seconds
