import logging

from django.core.management.base import BaseCommand

from news.services.news_service import fetch_news_data, refresh_news, save_articles_from_feed

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Fetch public news articles and store them in the database.'

    def add_arguments(self, parser):
        parser.add_argument('--query', default='', help='Optional keyword search query')

    def handle(self, *args, **options):
        query = options.get('query') or ''
        try:
            articles = fetch_news_data(query=query)
            saved_count = save_articles_from_feed(articles)
            self.stdout.write(self.style.SUCCESS(f'Successfully saved {saved_count} articles'))
        except Exception as exc:
            logger.exception('News fetch command failed')
            self.stdout.write(self.style.WARNING(f'News service is temporarily unavailable. Showing previously collected articles. Error: {exc}'))
