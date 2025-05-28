import os
import logging
from openai import AsyncOpenAI
from typing import Optional, List
import httpx
from datetime import datetime
import json
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

logger = logging.getLogger(__name__)

CRYPTOPANIC_API_KEY = os.getenv('CRYPTOPANIC_API_KEY')
CRYPTOPANIC_API_URL = 'https://cryptopanic.com/api/v1/posts/?public=true'

logger.info(f"CRYPTOPANIC_API_KEY present: {bool(CRYPTOPANIC_API_KEY)}")

# Load artemis_mappings.json using absolute path
try:
    # Get the absolute path to the project root
    project_root = Path(__file__).parent.parent.parent
    mappings_path = project_root / 'config' / 'artemis_mappings.json'
    logger.info(f"Looking for artemis_mappings.json at: {mappings_path}")
    
    with open(mappings_path, 'r') as f:
        artemis_mappings = json.load(f)
    logger.info(f"Successfully loaded artemis_mappings.json with {len(artemis_mappings)} entries")
except Exception as e:
    logger.error(f"Error loading artemis_mappings.json: {str(e)}")
    artemis_mappings = {}

class NewsAnalyzer:
    def __init__(self):
        """Initialize the NewsAnalyzer with OpenAI client and CryptoPanic API key."""
        self.client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.cryptopanic_api_key = os.getenv('CRYPTOPANIC_API_KEY')
        logger.info(f"NewsAnalyzer initialized with CRYPTOPANIC_API_KEY: {bool(self.cryptopanic_api_key)}")
        if not self.cryptopanic_api_key:
            logger.error("CRYPTOPANIC_API_KEY not set in environment.")
    
    async def fetch_today_news(self, asset: Optional[str] = None) -> List[str]:
        """
        Fetch today's crypto news headlines from CryptoPanic.
        Optionally filter by asset (symbol).
        Returns a list of headlines. If no news for today, returns the most recent news.
        """
        logger.info(f"Fetching news for asset: {asset}")
        if not self.cryptopanic_api_key:
            logger.error("CRYPTOPANIC_API_KEY not set in environment.")
            return []
        params = {
            'auth_token': self.cryptopanic_api_key,
            'filter': 'hot',
            'public': 'true',
        }
        if asset:
            params['currencies'] = asset.lower()
        logger.info(f"Making request to CryptoPanic with params: {params}")
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(CRYPTOPANIC_API_URL, params=params, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                logger.info(f"CryptoPanic response status: {resp.status_code}")
                today = datetime.utcnow().date()
                headlines_today = []
                headlines_recent = []
                for post in data.get('results', []):
                    published = post.get('published_at', '')
                    if published:
                        pub_date = datetime.fromisoformat(published.replace('Z', '+00:00')).date()
                        if pub_date == today:
                            headlines_today.append(post.get('title', ''))
                        if len(headlines_recent) < 5:
                            headlines_recent.append(post.get('title', ''))
                logger.info(f"Found {len(headlines_today)} headlines for today, {len(headlines_recent)} recent headlines")
                if headlines_today:
                    return headlines_today[:10]
                else:
                    return headlines_recent[:5]
            except Exception as e:
                logger.error(f"Error fetching news from CryptoPanic: {str(e)}")
                return []

    async def get_market_news(self, asset: Optional[str] = None) -> str:
        """
        Get a summary of today's market news, optionally filtered by asset.
        If asset is provided, check artemis_mappings.json for the asset symbol or artemis_id.
        """
        logger.info(f"Getting market news for asset: {asset}")
        if asset:
            # Check artemis_mappings.json for the asset symbol or artemis_id
            asset_symbol = artemis_mappings.get(asset.lower(), asset.lower())
            logger.info(f"Using asset symbol: {asset_symbol}")
            headlines = await self.fetch_today_news(asset_symbol)
        else:
            headlines = await self.fetch_today_news()
        
        logger.info(f"Retrieved {len(headlines)} headlines")
        if not headlines:
            return "No fresh news found for today."
            
        prompt = (
            f"Summarize the following crypto news headlines from today ({datetime.utcnow().date()}):\n"
            + '\n'.join(f"- {h}" for h in headlines)
            + "\nFocus on price movements, significant events, and market sentiment. Keep it under 850 characters."
        )
        try:
            logger.info("Generating summary with OpenAI")
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a crypto market analyst providing concise news summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=850,
                temperature=0.7
            )
            summary = response.choices[0].message.content.strip()
            logger.info("Successfully generated summary")
            if len(headlines) < 5:
                return "No fresh news found for today. Here is the most recent news:\n" + summary
            return summary
        except Exception as e:
            logger.error(f"Error generating market news summary: {str(e)}")
            return "Failed to generate market news summary. Please try again later." 