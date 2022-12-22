from django.contrib import admin
from travels.models import Post, Comment, PostImage, Album, Tag, Location

# Register models in the admin panel


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "creation_date", "last_edited", "short_description")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "creation_date")


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ("post", "image")


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "lat", "lng")
