from django.urls import path, include
from feeds import views as views


urlpatterns = [
    path("api/", include(('feeds.api_urls', 'feeds_api'), namespace='api')),
    path("", views.front_feed, name='front_feed'),
]
