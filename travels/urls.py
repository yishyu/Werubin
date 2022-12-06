from django.urls import path, include
from feeds import views as views

urlpatterns = [
    path("api/", include(('travels.api_urls', 'travels_api'), namespace='api_travels')),
]