from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.decorators import login_required
from travels.models import Post, Comment
from travels.serializers import PostSerializer, CommentSerializer
from travels.forms import PostForm
from django.shortcuts import get_object_or_404
from travels.decorators import has_postid, has_commentId


# TODO generate swagger
@login_required
@api_view(['GET'])
def get_post(request, postId):
    post = get_object_or_404(Post, id=postId)
    serializer = PostSerializer(post, context={'request': request})
    return Response(status=status.HTTP_200_OK, data=serializer.data)


@login_required
@api_view(['GET'])
@has_postid
def get_comments(request, postId):
    post = get_object_or_404(Post, id=postId)

    serializer = CommentSerializer(post.comment_set.all().order_by("creation_date"), many=True)
    return Response(status=status.HTTP_200_OK, data=serializer.data)


@login_required
@api_view(['POST'])  # Post: Create
def add_post(request):
    """
        Adding a post
        TODO Condition: The author of the request has to be the author of the post, otherwise
        we would allow people posting in the name of others
    """
    form = PostForm(request.data)
    if form.is_valid():
        formA = form.save()
        serializer = PostSerializer(formA, context={'request': request})
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['DELETE'])  # Delete: Delete
def delete_post(request, postId):
    """
        Delete a post
        Condition: The request is made by the author of the post
    """
    post = get_object_or_404(Post, id=postId)
    if post.author == request.user:
        post.delete()  # this will raise 404 in case
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Impossible to delete someone else's post"})


@login_required
@api_view(['PUT'])  # Put: Update/Replace
def update_post(request):
    """
        TODO Edit a post
    """
    print(request.data['post-id'])
    return Response(status=status.HTTP_200_OK)


@login_required
@api_view(['PUT'])  # Put: Update/Replace
@has_postid
def toggle_like_post(request, postId):
    """
        Like a post and Cancel a like
    """
    post = get_object_or_404(Post, id=postId)  # test if the post exists
    if Post.objects.filter(id=post.id, likes=request.user).count() == 0:  # the user has not already liked the post
        post.likes.add(request.user)
        data = {"like-status": 1}
    else:
        post.likes.remove(request.user)
        data = {"like-status": 0}
    return Response(status=status.HTTP_200_OK, data=data)


@login_required
@api_view(['PUT'])  # Put: Update/Replace
@has_commentId
def toggle_like_comment(request, commentId):
    """
        Like a comment and Cancel a like
    """
    comment = get_object_or_404(Comment, id=commentId)  # test if the comment exists
    if Comment.objects.filter(id=comment.id, likes=request.user).count() == 0:  # the user has not already liked the post
        comment.likes.add(request.user)
        data = {"like-status": 1}
    else:
        comment.likes.remove(request.user)
        data = {"like-status": 0}
    return Response(status=status.HTTP_200_OK, data=data)


@login_required
@api_view(['PUT'])  # Put: Update/Replace
@has_postid
def share_post(request, postId):
    """
        Share a post by creating a new post
        A shared post automatically inherits the tags of the parent post
    """
    post = get_object_or_404(Post, id=postId)  # test if the post exists
    if Post.objects.filter(shares=post, author=request.user).count() > 0:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "You have already shared this post"})
    share_post = Post.objects.create(
        author=request.user,
        shares=post,
    )
    share_post.tags.add(*post.tags.all())
    serializer = PostSerializer(share_post, context={'request': request})
    return Response(status=status.HTTP_200_OK, data=serializer.data)


@login_required
@api_view(['POST'])
@has_postid
def add_comment(request, postId):
    if "content" not in request.data:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "no content"})
    content = request.data["content"]
    if len(content) > 150:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "The content of this comment is superior to 150 characters."})
    post = get_object_or_404(Post, id=postId)

    comment = Comment.objects.create(
        author=request.user,
        content=content,
        post=post
    )
    serializer = CommentSerializer(comment)
    return Response(status=status.HTTP_200_OK, data=serializer.data)
