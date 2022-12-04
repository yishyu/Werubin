from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from travels.models import Post, Tag


@login_required
def front_feed(request):
    if len(request.GET) > 0:
        feed_type = request.GET.get('type')
        if feed_type == "Followers":
            feed = "Followers"
            posts = Post.objects.filter(author__in=request.user.followers.all())
        elif feed_type == "Explore":
            feed = "Explore"
            posts = Post.objects.all()
        elif feed_type == "ForYou":
            feed = "ForYou"
            posts = Post.objects.filter(tags__in=request.user.tags.all())
        elif feed_type == "SingleTag":
            feed = "SingleTag"
            posts = Post.objects.filter(tags__name=request.GET.get("tag"))
    else:  # ForYou by Default
        # ForYou
        feed = "ForYou"
        posts = Post.objects.filter(tags__in=request.user.tags.all())

    posts = posts.order_by("-creation_date")
    return render(request, 'feeds/feed.html', locals())


@login_required
def singlePost(request, postID):
    post = Post.objects.get(id=postID)
    return render(request, 'posts/singlepostpage.html', locals())
