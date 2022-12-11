from django.shortcuts import render
from travels.models import Post
from django.contrib.auth.decorators import login_required


@login_required
def singlePost(request, postID):
    return render(request, 'posts/singlepostpage.html', locals())
