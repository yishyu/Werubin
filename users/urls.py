from django.urls import path
from django.contrib.auth import views as dviews

urlpatterns = [
    path('login/', dviews.LoginView.as_view(), name='login'),
    path('logout/', dviews.LogoutView.as_view(), name='logout'),
]
