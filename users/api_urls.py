from django.urls import path
import users.api_views as views

app_name = "users_api"
urlpatterns = [
    path("get/", views.get_users, name="get_users"),
    path("current_user/", views.current_user, name="current_user"),
    path("follow_user/", views.follow_user, name="follow_user"),
    path("road_map/", views.road_map, name="road_map"),

]
