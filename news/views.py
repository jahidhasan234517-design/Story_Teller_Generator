import json
import logging
from datetime import datetime, timedelta

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from news.models import Article, Bookmark, SearchHistory
from news.services.news_service import (
    build_analytics_payload,
    get_dashboard_stats,
    get_topics_summary,
    get_trending_articles,
    refresh_news,
)

logger = logging.getLogger(__name__)

CATEGORY_CHOICES = [
    'World', 'Technology', 'Business', 'Science', 'AI', 'Programming', 'Cybersecurity', 'Startups', 'Finance', 'Health', 'Education', 'Environment'
]
SENTIMENT_CHOICES = ['Positive', 'Neutral', 'Negative']


def build_base_context(request):
    return {
        'active_section': 'dashboard',
        'categories': CATEGORY_CHOICES,
        'sentiments': SENTIMENT_CHOICES,
        'now': datetime.now(),
        'request': request,
    }


def dashboard_view(request):
    ctx = build_base_context(request)
    ctx['stats'] = get_dashboard_stats()
    ctx['trending'] = get_trending_articles(4)
    ctx['top_topics'] = get_topics_summary(6)
    return render(request, 'dashboard.html', ctx)


def news_list_view(request):
    ctx = build_base_context(request)
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    sentiment = request.GET.get('sentiment', '').strip()
    source = request.GET.get('source', '').strip()
    date_filter = request.GET.get('date', '').strip()

    if query:
        SearchHistory.objects.create(query=query)

    results = Article.objects.all()
    if query:
        results = results.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(keywords__icontains=query))
    if category:
        results = results.filter(category=category)
    if sentiment:
        results = results.filter(sentiment=sentiment)
    if source:
        results = results.filter(source__icontains=source)
    if date_filter:
        if date_filter == '7':
            cutoff = datetime.now() - timedelta(days=7)
            results = results.filter(published_at__gte=cutoff)
        elif date_filter == '30':
            cutoff = datetime.now() - timedelta(days=30)
            results = results.filter(published_at__gte=cutoff)
        elif date_filter == '90':
            cutoff = datetime.now() - timedelta(days=90)
            results = results.filter(published_at__gte=cutoff)

    ctx['query'] = query
    ctx['category'] = category
    ctx['sentiment'] = sentiment
    ctx['source'] = source
    ctx['date_filter'] = date_filter
    ctx['articles'] = results.order_by('-published_at', '-popularity_score')[:30]
    return render(request, 'news/list.html', ctx)


def article_detail_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    ctx = build_base_context(request)
    ctx['article'] = article
    ctx['keywords'] = [item.strip() for item in (article.keywords or '').split(',') if item.strip()]
    return render(request, 'news/detail.html', ctx)


def trending_view(request):
    ctx = build_base_context(request)
    ctx['active_section'] = 'trending'
    ctx['trending'] = get_trending_articles(12)
    return render(request, 'trending.html', ctx)


def topics_view(request):
    ctx = build_base_context(request)
    ctx['active_section'] = 'topics'
    ctx['topics'] = get_topics_summary(12)
    return render(request, 'topics.html', ctx)


def analytics_view(request):
    ctx = build_base_context(request)
    ctx['active_section'] = 'analytics'
    return render(request, 'analytics.html', ctx)


def bookmarks_view(request):
    ctx = build_base_context(request)
    ctx['active_section'] = 'bookmarks'
    ctx['bookmarks'] = Bookmark.objects.select_related('article').order_by('-created_at')
    return render(request, 'bookmarks.html', ctx)


def about_view(request):
    ctx = build_base_context(request)
    ctx['active_section'] = 'about'
    return render(request, 'about.html', ctx)


def refresh_news_view(request):
    refresh_news()
    return render(request, 'dashboard.html', {'stats': get_dashboard_stats(), 'trending': get_trending_articles(4), 'top_topics': get_topics_summary(6)})


@require_http_methods(['GET'])
def news_api(request):
    articles = list(Article.objects.order_by('-published_at', '-popularity_score')[:20].values())
    return JsonResponse({'articles': articles})


@require_http_methods(['GET'])
def trending_api(request):
    trending = list(get_trending_articles(8))
    payload = [{'title': article.title, 'score': round(article.popularity_score, 2), 'source': article.source} for article in trending]
    return JsonResponse({'trending': payload})


@require_http_methods(['GET'])
def analytics_api(request):
    payload = build_analytics_payload()
    return JsonResponse(payload)


@require_http_methods(['GET'])
def topics_api(request):
    return JsonResponse({'topics': get_topics_summary(12)})


@require_http_methods(['POST'])
def bookmark_article(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)

    article_id = payload.get('article_id')
    if not article_id:
        return JsonResponse({'error': 'Missing article_id'}, status=400)

    article = get_object_or_404(Article, pk=article_id)
    bookmark, created = Bookmark.objects.get_or_create(article=article)
    return JsonResponse({'status': 'saved' if created else 'exists', 'bookmark_id': bookmark.id})
