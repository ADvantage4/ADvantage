from django.urls import path
from .views import NewsScraper

urlpatterns = [
    path('fetch-news/', NewsScraper.as_view(), name='fetch-news'),
]
