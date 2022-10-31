from django.urls import path
from django.contrib.auth import views as dviews
from users.views import RegistrationView

urlpatterns = [
    path('login/', dviews.LoginView.as_view(), name='login'),
    path('logout/', dviews.LogoutView.as_view(), name='logout'),
    path('register/', RegistrationView.as_view(), name='register')
]
