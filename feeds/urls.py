from django.urls import path

from feeds import views as views

urlpatterns = [
    path("", views.front_feed, name='front_feed'),
    path('post/<str:postID>/', views.singlePost, name='post')
]