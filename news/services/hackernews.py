import logging
from urllib.parse import urlencode

import requests

logger = logging.getLogger(__name__)


def fetch_hacker_news(query: str = '', page: int = 0):
    params = {'query': query, 'page': page}
    url = 'https://hn.algolia.com/api/v1/search?' + urlencode({k: v for k, v in params.items() if v not in (None, '', 0)})
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        hits = data.get('hits', []) if isinstance(data, dict) else []
        return hits
    except requests.RequestException as exc:
        logger.warning('Hacker News fetch failed: %s', exc)
        return []
    except ValueError:
        logger.warning('Hacker News returned invalid JSON')
        return []
