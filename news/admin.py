from django.contrib import admin

from .models import Article, Bookmark, SearchHistory


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'category', 'sentiment', 'published_at', 'popularity_score')
    list_filter = ('source', 'category', 'sentiment', 'published_at')
    search_fields = ('title', 'description', 'source', 'author', 'keywords')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('article', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('article__title',)


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('query', 'created_at')
    search_fields = ('query',)
    list_filter = ('created_at',)
