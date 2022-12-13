from django.urls import path, re_path
import feeds.api_views as views


app_name = "feeds_api"
urlpatterns = [
    path("feed/", views.feed, name="feed"),
]
