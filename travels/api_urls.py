from django.urls import path
import travels.api_views as views

app_name = "travels_api"
urlpatterns = [
    path("post/get/<str:postId>/", views.get_post, name="get_post"),
    path("post/add", views.add_post, name="add_post"),
    path("post/delete/<str:postId>/", views.delete_post, name="delete_post"),
    path("post/update/", views.update_post, name="update_post"),
    path("post/add-comment/", views.add_comment, name="add_comment"),
    path("post/toggle-like-post/<str:postId>/", views.toggle_like_post, name="toggle_like_post"),
    path("post/share/<str:postId>/", views.share_post, name="share_post"),
]
