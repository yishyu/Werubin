from django.shortcuts import render
from travels.models import Post
from django.contrib.auth.decorators import login_required


@login_required
def singlePost(request, postID):
    """
        This view is used to display a single post
        It is called when a user clicks on a post id in a shared post
    """
    return render(request, 'posts/singlePostPage.html', locals())
