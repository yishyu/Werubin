from django.urls import path, include
from travels import views as views

urlpatterns = [
    path("api/", include(('travels.api_urls', 'travels_api'), namespace='api')),
    path('post/<str:postID>/', views.singlePost, name='post'),

]
