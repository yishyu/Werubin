from rest_framework.response import Response
from rest_framework import status


def has_postid(func):
    """
        This decorator is used to check if the request has a post-id
        and pass it to the function
    """
    def wrapper(*args, **kwargs):
        request = args[0]
        data = request.GET if request.method == "GET" else request.data
        if "post-id" not in data:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Missing post-id"})
        return func(*args, **kwargs, postId=data["post-id"])
    return wrapper


def has_commentId(func):
    """
        This decorator is used to check if the request has a comment-id
        and pass it to the function
    """
    def wrapper(*args, **kwargs):
        request = args[0]
        data = request.GET if request.method == "GET" else request.data
        if "comment-id" not in data:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Missing comment-id"})
        return func(*args, **kwargs, commentId=data["comment-id"])
    return wrapper
