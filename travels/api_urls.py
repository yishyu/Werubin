from django.urls import path
import travels.api_views as views

app_name = "travels_api"
urlpatterns = [
    path("add_post/", views.add_post, name="add_post"),
    path("add_comment/",views.add_comment, name="add_comment"),

]