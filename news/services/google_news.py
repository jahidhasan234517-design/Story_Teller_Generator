import logging
from xml.etree import ElementTree as ET

import feedparser
import requests

logger = logging.getLogger(__name__)


def fetch_google_news(query: str = 'technology'):
    url = 'https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en'
    if query:
        url = f'https://news.google.com/rss/search?q={query.replace(" ", "+")}&hl=en-US&gl=US&ceid=US:en'

    try:
        response = requests.get(url, timeout=12)
        response.raise_for_status()
        feed = feedparser.parse(response.content)
        return feed.entries[:10]
    except (requests.RequestException, ET.ParseError, ValueError):
        logger.warning('Google News fetch failed', exc_info=True)
        return []
