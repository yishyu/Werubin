from django.urls import path, include
from django.contrib.auth import views as dviews
import users.views as views

urlpatterns = [
    path('login/', dviews.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.registration, name='register'),
    path('register_tag/', views.register_tag, name='register_tag'),
    path('forgotpass/', views.forgotpass, name='forgotpass'),
    path('reset-password/<str:key>/', views.resetpass, name='resetpass'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path("api/", include(('users.api_urls', 'users_api'), namespace='api')),

]
