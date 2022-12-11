from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from users.serializers import PostUserSerializer
from users.models import User
from travels.models import Post, Comment


@login_required
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
        users = get_object_or_404(User, id=data["id"]).followers_set.all()
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
