from django.db import models
# https://stackoverflow.com/questions/15285740/make-django-admin-to-display-no-more-than-100-characters-in-list-results
from django.template.defaultfilters import truncatechars  # or truncatewords


class Post(models.Model):
    """
        A Post:
            - is created by a User
            - contains a text content
            - can contain images (the image are a separate models named PostImages each pointing to a post)
            - might be in multiple Albums or none
            - can be shared
            - can be commented
            - can be liked
    """
    content = models.TextField("Text content")
    creation_date = models.DateTimeField("creation date", auto_now=False, auto_now_add=True)
    last_edited = models.DateTimeField("Last edit", auto_now=True, auto_now_add=False)
    author = models.ForeignKey("users.User", verbose_name="User", on_delete=models.CASCADE, related_name="author")
    shares = models.ForeignKey("self", verbose_name="Shared post", on_delete=models.CASCADE, null=True, blank=True)  # for me sharig a post means, creating a new post containing the post
    likes = models.ManyToManyField("users.User", verbose_name="Likes", related_name="likes", blank=True)

    @property
    def short_description(self):
        return truncatechars(self.content, 100)


class Comment(models.Model):
    """
        A comment is contained in a post, it looks a bit like a post but it doesn't have certain of post features
    """
    author = models.ForeignKey("users.User", verbose_name="Author", on_delete=models.CASCADE)
    content = models.TextField("Text content")
    post = models.ForeignKey("travels.Post", verbose_name="Post", on_delete=models.CASCADE)
    creation_date = models.DateTimeField("creation date", auto_now=False, auto_now_add=True)
    likes = models.ManyToManyField("users.User", verbose_name="Likes", related_name="Commentlikes")


class PostImage(models.Model):
    """
        PostImages are contained in posts
        Note: It would be great to make a unique name for the images
        so that they don't overwrite another image having the same filename
    """
    post = models.ForeignKey("travels.Post", verbose_name="post", on_delete=models.CASCADE)
    image = models.ImageField("image", upload_to="post/images", height_field=None, width_field=None, max_length=None, blank=True, null=True)


class Album(models.Model):
    """
        An Album contains posts

    """
    user = models.ForeignKey("users.User", verbose_name="User", on_delete=models.CASCADE)
    name = models.CharField("Title", max_length=100)
    posts = models.ManyToManyField("travels.Post", verbose_name="posts")
