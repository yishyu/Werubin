from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, get_list_or_404
from users.serializers import PostUserSerializer, UserSerializer
from travels.serializers import PostSerializer, LocationSerializer
from users.models import User
from travels.models import Post, Comment
from travels.decorators import has_postid

from rest_framework.permissions import AllowAny
from users.decorators import no_user


@api_view(['GET'])
def get_users(request):
    """
        Params: - type (followers, following, shared, liked)
                - id   (userId   , userId   , postId, postId)
    """
    data = request.GET
    if "type" not in data.keys() or "id" not in data.keys():
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "missing parameters"})

    if data["type"] == "following":
        users = get_object_or_404(User, id=data["id"]).followers
    elif data["type"] == "followers":
        user = get_object_or_404(User, id=data["id"])
        users = User.objects.filter(followers__id=user.id)
    elif data["type"] == "shared":
        post = get_object_or_404(Post, id=data["id"])
        users = User.objects.filter(id__in=Post.objects.filter(shares=post).values_list("author", flat=True))
    elif data["type"] == "liked":
        if "model" not in data.keys():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "missing parameters"})
        if data["model"] == "comment":
            users = get_object_or_404(Comment, id=data["id"]).likes
        else:
            users = get_object_or_404(Post, id=data["id"]).likes
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": f"Unrecognized parameter '{data['type']}'"})

    data = PostUserSerializer(users, many=True).data
    return Response(status=status.HTTP_200_OK, data=data)


@api_view(["GET"])
def current_user(request):
    data = UserSerializer(request.user).data
    return Response(status=status.HTTP_200_OK, data=data)


@api_view(["PUT"])
def follow_user(request):

    user = get_object_or_404(User, id=request.data['user-id'])
    if request.user.id == user.id:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "You may like yourself a lot but unfortunately you cannot follow yourself"})
    if user in request.user.followers.all():
        request.user.followers.remove(user)
        data = {"follow-status": 0}
    else:
        request.user.followers.add(user)
        data = {"follow-status": 1}

    return Response(status=status.HTTP_200_OK, data=data)


@api_view(["PUT"])
@permission_classes([AllowAny, ])
def user_exists(request):
    if User.objects.filter(username=request.data["username"]).count() > 0:
        data = {"user_exists": True}
    else:
        data = {"user_exists": False}
    return Response(status=status.HTTP_200_OK, data=data)


@api_view(["PUT"])
@permission_classes([AllowAny, ])
def email_exists(request):
    if User.objects.filter(email=request.data["email"].lower()).count() > 0:
        data = {"email_exists": True}
    else:
        data = {"email_exists": False}
    return Response(status=status.HTTP_200_OK, data=data)


@api_view(["GET"])
def road_map(request):
    """
        Returns a list of all locations shared by a specific user
        the locations are shown on a map in a user profile
    """
    user = get_object_or_404(User, id=request.GET['user-id'])
    posts = Post.objects.filter(author=user).exclude(location=None)
    # we might want to show post information on the map so we prefer returning the post information instead of the location
    serializer = PostSerializer(posts, many=True)
    return Response(status=status.HTTP_200_OK, data=serializer.data)


@api_view(["GET"])
def notification(request):
    return
