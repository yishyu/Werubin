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
            - has a location
            - has tags
    """
    content = models.TextField("Text content")
    creation_date = models.DateTimeField("creation date", auto_now=False, auto_now_add=True)
    last_edited = models.DateTimeField("Last edit", auto_now=True, auto_now_add=False)
    author = models.ForeignKey("users.User", verbose_name="User", on_delete=models.CASCADE, related_name="author")
    shares = models.ForeignKey("self", verbose_name="Shared post", on_delete=models.CASCADE, null=True, blank=True)  # for me sharig a post means, creating a new post containing the post
    likes = models.ManyToManyField("users.User", verbose_name="Likes", related_name="likes", blank=True)
    location = models.ForeignKey("Location", verbose_name="Location", on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField("Tag", verbose_name="Tags", blank=True)

    @property
    def short_description(self):
        return truncatechars(self.content, 100)


class Tag(models.Model):
    name = models.CharField("name", max_length=50)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField("Location Place Name", max_length=50)
    lat = models.CharField("latitude", max_length=50, null=True, blank=True)
    lng = models.CharField("longitude", max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    """
        A comment is contained in a post, it looks a bit like a post but it doesn't have certain of post features
    """
    author = models.ForeignKey("users.User", verbose_name="Author", on_delete=models.CASCADE)
    content = models.TextField("Text content")
    post = models.ForeignKey("travels.Post", verbose_name="Post", on_delete=models.CASCADE)
    creation_date = models.DateTimeField("creation date", auto_now=False, auto_now_add=True)
    likes = models.ManyToManyField("users.User", verbose_name="Likes", related_name="Commentlikes", blank=True)

    @property
    def time_ago(self):
        '''
        TODO method return now - creation_date => min if < 1h, hour if < 1 day, day
        '''
        return "8 min"


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
