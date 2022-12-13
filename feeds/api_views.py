from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from travels.models import Post, Comment, Album, PostImage
from travels.serializers import PostSerializer, CommentSerializer, AlbumSerializer, PostImageSerializer
from rest_framework import status
from django.urls import reverse
from django.http import HttpResponseRedirect

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.permissions import IsAuthenticated

type_param = openapi.Parameter('type', openapi.IN_QUERY, description="[Followers, Explore, ForYou, SingleTag, User]", type=openapi.TYPE_STRING)
tag_param = openapi.Parameter('tag', openapi.IN_QUERY, description="a tag name", type=openapi.TYPE_STRING)
user_param = openapi.Parameter('id', openapi.IN_QUERY, description="a user id", type=openapi.TYPE_STRING)
offset_param = openapi.Parameter('offset', openapi.IN_QUERY, description="Starting index", type=openapi.TYPE_INTEGER)
limit_param = openapi.Parameter('limit', openapi.IN_QUERY, description="Amount of posts", type=openapi.TYPE_INTEGER)

user_response = openapi.Response('response description', PostSerializer)


@swagger_auto_schema(method='get', manual_parameters=[type_param, tag_param, user_param, offset_param, limit_param], responses={200: user_response})
@permission_classes((IsAuthenticated,))
@api_view(["GET"])
def feed(request):
    """
        Returns post based on type, offset, limit
    """
    posts = Post.objects.none()
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
        elif feed_type == "User":
            posts = Post.objects.filter(author__id=request.GET.get("id"))
    posts = posts.order_by("-creation_date")
    if request.GET.get('limit'):
        OFFSET = int(request.GET.get('offset', 0))
        LIMIT = int(request.GET.get('limit'))
        posts = posts[OFFSET:OFFSET + LIMIT]
    data = PostSerializer(posts, many=True).data
    return Response(status=status.HTTP_200_OK, data=data)
