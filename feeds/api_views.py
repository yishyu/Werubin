from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from travels.models import Post, Comment, Album, PostImage
from travels.serializers import PostSerializer, CommentSerializer, AlbumSerializer, PostImageSerializer


@api_view(['GET'])
def all_posts(request):
    post_qs = Post.objets.order_by("-creation_date")
    serializer = PostSerializer(post_qs, context={'request': request}, many=True)
    return Response(serializer.data)
