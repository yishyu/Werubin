from django.urls import path

from feeds import views

urlpatterns = [
    path("", views.front_feed, name='front_feed'),
]
