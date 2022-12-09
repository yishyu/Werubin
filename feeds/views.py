from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from travels.models import Post, Tag


@login_required
def front_feed(request):
    return render(request, 'feeds/feed.html')


@login_required
def singlePost(request, postID):
    post = Post.objects.get(id=postID)
    return render(request, 'posts/singlepostpage.html', locals())
