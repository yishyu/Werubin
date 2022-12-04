from django.urls import path
import feeds.api_views as views

app_name = "feeds_api"
urlpatterns = [
    path("all_posts/", views.all_posts, name="all_posts"),

]