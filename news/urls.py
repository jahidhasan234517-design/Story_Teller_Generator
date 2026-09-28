from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('news/', views.news_list_view, name='news_list'),
    path('news/<int:pk>/', views.article_detail_view, name='article_detail'),
    path('trending/', views.trending_view, name='trending'),
    path('topics/', views.topics_view, name='topics'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('bookmarks/', views.bookmarks_view, name='bookmarks'),
    path('about/', views.about_view, name='about'),
    path('refresh-news/', views.refresh_news_view, name='refresh_news'),
    path('api/news/', views.news_api, name='news_api'),
    path('api/trending/', views.trending_api, name='trending_api'),
    path('api/analytics/', views.analytics_api, name='analytics_api'),
    path('api/topics/', views.topics_api, name='topics_api'),
    path('api/bookmark/', views.bookmark_article, name='bookmark_api'),
]
