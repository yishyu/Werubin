from django.urls import path
import travels.api_views as views

app_name = "travels_api"
urlpatterns = [
    path("post/get/<str:postId>/", views.get_post, name="get_post"),
    path("post/add/", views.add_post, name="add_post"),
    path("post/delete/", views.delete_post, name="delete_post"),
    path("post/update/", views.update_post, name="update_post"),
    path("post/add-album/", views.add_album, name="add_album"),
    path("post/delete-album/", views.delete_album, name="delete_album"),
    path("post/add-post-to-album/", views.add_post_to_album, name="add_post_to_album"),
    path("post/remove-post-from-album/", views.remove_post_from_album, name="remove_post_from_album"),
    path("post/remove-image-from-post/", views.remove_image_from_post, name="remove_image_from_post"),
    path("post/get-albums/", views.get_albums, name="get_albums"),
    path("post/add-comment/", views.add_comment, name="add_comment"),
    path("post/get-comments/", views.get_comments, name="get_comments"),
    path("post/toggle-like-comment/", views.toggle_like_comment, name="toggle_like_comment"),
    path("post/toggle-like-post/", views.toggle_like_post, name="toggle_like_post"),
    path("post/share/", views.share_post, name="share_post"),
]
