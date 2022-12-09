from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from travels.models import Post, Comment, Album, PostImage
from travels.serializers import PostSerializer, CommentSerializer, AlbumSerializer, PostImageSerializer
from rest_framework import status


@login_required
@api_view(["GET"])
def feed(request):
    """
        Add Pagination, limit
    """
    if len(request.GET) > 0:
        feed_type = request.GET.get('type')
        if feed_type == "Followers":
            posts = Post.objects.filter(author__in=request.user.followers.all())
        elif feed_type == "Explore":
            posts = Post.objects.all()
        elif feed_type == "ForYou":
            posts = Post.objects.filter(tags__in=request.user.tags.all())
        elif feed_type == "SingleTag":
            posts = Post.objects.filter(tags__name=request.GET.get("tag"))

    posts = posts.order_by("-creation_date")
    data = PostSerializer(posts, many=True).data
    return Response(status=status.HTTP_200_OK, data=data)
