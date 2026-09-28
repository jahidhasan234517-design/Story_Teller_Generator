import json
import logging
from collections import Counter
from datetime import datetime, timedelta
from typing import Any

from django.core.cache import cache
from django.db.models import Count, Q

from news.models import Article, Bookmark
from news.services.categorizer import classify_category
from news.services.google_news import fetch_google_news
from news.services.hackernews import fetch_hacker_news
from news.services.keywords import extract_keywords
from news.services.sentiment import analyze_sentiment

logger = logging.getLogger(__name__)

CATEGORY_SEQUENCE = [
    'World', 'Technology', 'Business', 'Science', 'AI', 'Programming', 'Cybersecurity', 'Startups', 'Finance', 'Health', 'Education', 'Environment'
]


def normalize_datetime(value):
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    except ValueError:
        return None


def normalize_article_entry(item: dict[str, Any], source_name: str = 'Hacker News') -> dict[str, Any]:
    title = (item.get('title') or item.get('story_title') or item.get('headline') or 'Untitled').strip()
    url = item.get('url') or item.get('story_url') or item.get('link') or ''
    description = (item.get('description') or item.get('story_text') or item.get('summary') or item.get('excerpt') or '').strip()
    author = (item.get('author') or item.get('creator') or '').strip()
    published = normalize_datetime(item.get('created_at_i') or item.get('published_at') or item.get('created_at'))

    if published is None:
        if 'published' in item:
            try:
                published = datetime.fromisoformat(str(item['published']).replace('Z', '+00:00'))
            except ValueError:
                published = None

    if source_name == 'Google News' and not url:
        url = item.get('link', '')
    content = f'{title} {description}'
    category = classify_category(content)
    sentiment, sentiment_score = analyze_sentiment(content)
    keywords = extract_keywords(content, limit=8)
    collective_score = item.get('points') or item.get('score') or item.get('votes') or 0
    comments = item.get('num_comments') or item.get('comments') or 0
    if published:
        hours_old = max((datetime.now(published.tzinfo) - published).total_seconds() / 3600, 1)
    else:
        hours_old = 1
    popularity_score = float(collective_score) + float(comments) * 1.5 + (max(24 - hours_old, 0) * 0.2)
    return {
        'title': title,
        'description': description,
        'url': url,
        'source': source_name,
        'author': author,
        'published_at': published,
        'category': category,
        'sentiment': sentiment,
        'sentiment_score': sentiment_score,
        'keywords': ', '.join(keywords),
        'popularity_score': round(popularity_score, 2),
    }


def fetch_news_data(query: str = '', page: int = 0):
    payload = []
    try:
        hacker_hits = fetch_hacker_news(query=query, page=page) or []
        for hit in hacker_hits:
            payload.append(normalize_article_entry(hit, 'Hacker News'))
    except Exception:
        logger.exception('Failed to fetch Hacker News payload')

    try:
        google_entries = fetch_google_news(query=query) or []
        for entry in google_entries:
            article = {
                'title': entry.get('title', ''),
                'description': entry.get('summary', ''),
                'url': entry.get('link', ''),
                'source': 'Google News',
                'author': '',
                'published_at': entry.get('published_parsed') or entry.get('published'),
                'points': 0,
                'num_comments': 0,
            }
            payload.append(normalize_article_entry(article, 'Google News'))
    except Exception:
        logger.exception('Failed to fetch Google news payload')

    unique_by_url = {}
    for article in payload:
        normalized_url = article.get('url') or ''
        if normalized_url and normalized_url not in unique_by_url:
            unique_by_url[normalized_url] = article
    filtered = list(unique_by_url.values())
    filtered.sort(key=lambda item: (item.get('published_at') or datetime.min, float(item.get('popularity_score', 0))), reverse=True)
    return filtered


def save_articles_from_feed(articles):
    saved = 0
    for item in articles:
        url = item.get('url', '').strip()
        if not url:
            continue
        article, created = Article.objects.get_or_create(
            url=url,
            defaults={
                'title': item.get('title', 'Untitled')[:500],
                'description': item.get('description', '')[:5000],
                'source': item.get('source', 'Hacker News'),
                'author': item.get('author', '')[:200],
                'published_at': item.get('published_at'),
                'category': item.get('category', 'World'),
                'sentiment': item.get('sentiment', 'Neutral'),
                'sentiment_score': item.get('sentiment_score', 0.0),
                'keywords': item.get('keywords', ''),
                'popularity_score': item.get('popularity_score', 0.0),
            },
        )
        if not created:
            article.title = item.get('title', article.title)[:500]
            article.description = item.get('description', article.description)[:5000]
            article.source = item.get('source', article.source)
            article.author = item.get('author', article.author)[:200]
            article.published_at = item.get('published_at') or article.published_at
            article.category = item.get('category', article.category)
            article.sentiment = item.get('sentiment', article.sentiment)
            article.sentiment_score = item.get('sentiment_score', article.sentiment_score)
            article.keywords = item.get('keywords', article.keywords)
            article.popularity_score = item.get('popularity_score', article.popularity_score)
            article.save(update_fields=[
                'title', 'description', 'source', 'author', 'published_at',
                'category', 'sentiment', 'sentiment_score', 'keywords', 'popularity_score'
            ])
        saved += 1
    return saved


def get_dashboard_stats():
    total_articles = Article.objects.count()
    today = datetime.now().date()
    articles_today = Article.objects.filter(published_at__date=today).count()
    trending = Article.objects.filter(popularity_score__gte=40).count()
    saved_articles = Bookmark.objects.count()
    positive = Article.objects.filter(sentiment='Positive').count()
    negative = Article.objects.filter(sentiment='Negative').count()
    neutral = Article.objects.filter(sentiment='Neutral').count()
    return {
        'total_articles': total_articles,
        'articles_today': articles_today,
        'trending': trending,
        'saved_articles': saved_articles,
        'positive': positive,
        'negative': negative,
        'neutral': neutral,
    }


def get_trending_articles(limit: int = 8):
    articles = list(Article.objects.all())
    for article in articles:
        article.dashboard_score = compute_trending_score(article)
    articles.sort(key=lambda item: item.dashboard_score, reverse=True)
    return articles[:limit]


def compute_trending_score(article):
    points = float(article.popularity_score or 0)
    recency = 0
    if article.published_at:
        age_hours = max((datetime.now(article.published_at.tzinfo) - article.published_at).total_seconds() / 3600, 1)
        recency = max(0, 48 - age_hours) * 0.6
    comments = 0
    if 'comments' in article.keywords:
        comments = 10
    return points + recency + comments


def get_topics_summary(limit: int = 10):
    articles = Article.objects.exclude(keywords='')
    counts = Counter()
    for article in articles:
        for keyword in (article.keywords or '').split(','):
            word = keyword.strip().lower()
            if word:
                counts[word] += 1
    return [{'label': label, 'value': value} for label, value in counts.most_common(limit)]


def build_analytics_payload():
    categories = Article.objects.values('category').annotate(count=Count('id')).order_by('-count')
    sentiments = Article.objects.values('sentiment').annotate(count=Count('id')).order_by('-count')
    by_day = Article.objects.extra(select={'day': "date(published_at)"}).values('day').annotate(count=Count('id')).order_by('day')
    source_counts = Article.objects.values('source').annotate(count=Count('id')).order_by('-count')
    topic_data = get_topics_summary(8)
    return {
        'categories': list(categories),
        'sentiments': list(sentiments),
        'by_day': list(by_day),
        'sources': list(source_counts),
        'topics': topic_data,
    }


def get_cached_news(query=''):
    cache_key = f'news-feed-{query or "all"}'
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    data = fetch_news_data(query=query)
    cache.set(cache_key, data, timeout=600)
    return data


def refresh_news(query=''):
    cache_key = f'news-feed-{query or "all"}'
    data = fetch_news_data(query=query)
    save_articles_from_feed(data)
    cache.delete(cache_key)
    return data
