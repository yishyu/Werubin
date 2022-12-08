from django.urls import path
import users.api_views as views

app_name = "users_api"
urlpatterns = [
    path("get/", views.get_users, name="get_users"),
]
