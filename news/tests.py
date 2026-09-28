from django.test import TestCase, Client
from django.urls import reverse

from news.models import Article, Bookmark, SearchHistory
from news.services.categorizer import classify_category
from news.services.keywords import extract_keywords
from news.services.sentiment import analyze_sentiment


class ArticleModelTests(TestCase):
    def test_article_creation(self):
        article = Article.objects.create(
            title='Test AI article',
            description='Description about AI and machine learning.',
            url='https://example.com/article-1',
            source='Hacker News',
            author='Tester',
            category='AI',
            sentiment='Positive',
            sentiment_score=0.75,
            keywords='ai,ml,technology',
            popularity_score=99.0,
        )
        self.assertEqual(article.title, 'Test AI article')
        self.assertEqual(Article.objects.count(), 1)

    def test_category_and_sentiment_detection(self):
        self.assertEqual(classify_category('AI system with machine learning and chatgpt'), 'AI')
        self.assertEqual(classify_category('Cybersecurity malware and ransomware patch'), 'Cybersecurity')
        sentiment_label, _ = analyze_sentiment('This product is amazing and innovative')
        self.assertIn(sentiment_label, ['Positive', 'Neutral'])

    def test_keyword_extraction(self):
        keywords = extract_keywords('AI and machine learning are transforming software engineering and cloud systems')
        self.assertTrue(any(keyword in keywords for keyword in ['ai', 'machine', 'learning', 'software', 'cloud']))


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        Article.objects.create(
            title='AI and the future',
            description='This is a positive article about AI and growth.',
            url='https://example.com/future-ai',
            source='Hacker News',
            author='Author',
            category='AI',
            sentiment='Positive',
            sentiment_score=0.85,
            keywords='ai,future,technology',
            popularity_score=92.0,
            published_at='2026-09-28T10:00:00Z',
        )

    def test_dashboard_page_loads(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_news_page_loads(self):
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)

    def test_analytics_endpoint_returns_json(self):
        response = self.client.get(reverse('analytics_api'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('categories', response.json())

    def test_search_and_filter_work(self):
        response = self.client.get(reverse('news_list'), {'q': 'AI', 'category': 'AI'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AI and the future')


class BookmarkModelTests(TestCase):
    def test_bookmark_creation(self):
        article = Article.objects.create(
            title='Bookmark article',
            description='Desc',
            url='https://example.com/bookmark-article',
            source='Hacker News',
            author='Author',
            category='Technology',
            sentiment='Neutral',
            sentiment_score=0.0,
            keywords='bookmark',
            popularity_score=10.0,
        )
        bookmark = Bookmark.objects.create(article=article)
        self.assertEqual(bookmark.article.title, 'Bookmark article')

    def test_search_history_record(self):
        history = SearchHistory.objects.create(query='artificial intelligence')
        self.assertEqual(history.query, 'artificial intelligence')
