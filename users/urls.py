from django.urls import path, include
from django.contrib.auth import views as dviews
import users.views as views

urlpatterns = [
    path('login/', dviews.LoginView.as_view(), name='login'),
    path('logout/', dviews.LogoutView.as_view(), name='logout'),
    path('register/', views.registration, name='register'),
    path('forgotpass/', views.forgotpass, name='forgotpass'),
    path('reset-password/<str:key>/', views.resetpass, name='resetpass'),
    path('profile/', views.profile, name='profile'),
    path("api/", include(('users.api_urls', 'users_api'), namespace='api')),

]
