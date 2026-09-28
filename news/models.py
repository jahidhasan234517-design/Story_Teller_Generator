from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, default='')
    url = models.URLField(max_length=1000, unique=True)
    source = models.CharField(max_length=200, default='Hacker News')
    author = models.CharField(max_length=200, blank=True, default='')
    published_at = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=100, default='World')
    sentiment = models.CharField(max_length=20, default='Neutral')
    sentiment_score = models.FloatField(default=0.0)
    keywords = models.TextField(blank=True, default='')
    popularity_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-popularity_score', '-created_at']
        indexes = [
            models.Index(fields=['published_at']),
            models.Index(fields=['category']),
            models.Index(fields=['sentiment']),
            models.Index(fields=['source']),
        ]

    def __str__(self):
        return self.title


class Bookmark(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('article',)

    def __str__(self):
        return f'Bookmark: {self.article.title}'


class SearchHistory(models.Model):
    query = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query
