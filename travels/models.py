from django.db import models
# https://stackoverflow.com/questions/15285740/make-django-admin-to-display-no-more-than-100-characters-in-list-results
from django.template.defaultfilters import truncatechars  # or truncatewords
import datetime
from django.utils import timezone


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
    MAX_LENGTH = 300
    content = models.TextField("Text content", blank=True, null=True)
    creation_date = models.DateTimeField("creation date", auto_now=False, auto_now_add=True)
    last_edited = models.DateTimeField("Last edit", auto_now=True, auto_now_add=False)
    author = models.ForeignKey("users.User", verbose_name="User", on_delete=models.CASCADE, related_name="author")
    shares = models.ForeignKey("Post", verbose_name="Shared post", on_delete=models.CASCADE, null=True, blank=True)  # for me sharig a post means, creating a new post containing the post
    likes = models.ManyToManyField("users.User", verbose_name="Likes", related_name="likes", blank=True)
    location = models.ForeignKey("Location", verbose_name="Location", on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField("Tag", verbose_name="Tags", blank=True)

    @property
    def short_description(self):
        return truncatechars(self.content, 100)

    @property
    def time_ago(self):
        """
            Returns the time since the post was created
        """
        time = datetime.datetime.now() - self.creation_date
        if time.days > 0:
            if time.days > 7:
                return self.creation_date
            return f"{time.days}day ago" if time.days == 1 else f"{time.days}days ago"
        if time.total_seconds() // 3600 > 0:
            return f"{int(time.total_seconds() // 3600)}h ago"
        else:
            return f"{int(time.total_seconds() // 60)}min ago"


class Tag(models.Model):
    name = models.CharField("name", max_length=50)

    @property
    def used_count(self):
        return self.post_set.all().count()

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField("Location Place Name", max_length=250)
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
        """
            Returns the time since the comment was created
        """
        time = datetime.datetime.now() - self.creation_date
        if time.days > 0:
            if time.days > 7:
                return self.creation_date
            return f"{time.days}day" if time.days == 1 else f"{time.days}days"
        if time.total_seconds() // 3600 > 0:
            return f"{int(time.total_seconds() // 3600)}h ago"
        else:
            return f"{int(time.total_seconds() // 60)}min ago"


class PostImage(models.Model):
    """
        PostImages are contained in posts
        Note: It would be great to make a unique name for the images
        so that they don't overwrite another image having the same filename
    """
    post = models.ForeignKey("travels.Post", verbose_name="post", on_delete=models.CASCADE)
    image = models.ImageField("image", upload_to="post/images", height_field=None, width_field=None, max_length=300, blank=True, null=True)


class Album(models.Model):
    """
        An Album contains posts

    """
    user = models.ForeignKey("users.User", verbose_name="User", on_delete=models.CASCADE)
    name = models.CharField("Title", max_length=250)
    posts = models.ManyToManyField("travels.Post", verbose_name="posts")
