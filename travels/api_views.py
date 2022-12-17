from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.contrib.auth.decorators import login_required
from travels.models import Post, Comment, PostImage, Tag, Location, Album
from travels.serializers import PostSerializer, CommentSerializer, AlbumSerializer
from travels.forms import PostForm
from django.shortcuts import get_object_or_404
from travels.decorators import has_postid, has_commentId

from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.core.files import File
import os
from travels.utils import validate_post


@permission_classes((IsAuthenticated,))
@api_view(['GET'])
def get_post(request, postId):
    post = get_object_or_404(Post, id=postId)
    serializer = PostSerializer(post, context={'request': request})
    return Response(status=status.HTTP_200_OK, data=serializer.data)


@permission_classes((IsAuthenticated,))
@api_view(['PUT'])  # Put: Update/Replace
@has_postid
def update_post(request, postId):
    """
        Edit a post
        Note: the images in the request are all additional images to the existing post
        There's an endpoint to delete images
    """
    passed, errors = validate_post(request)
    if not passed:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=errors)

    post = get_object_or_404(Post, id=postId)
    if post.author != request.user:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "You can only edit your own posts"})

    # insert update code here

    # create location
    location, _ = Location.objects.get_or_create(
        name=request.data["googleAddress"],
        lat=float(request.data["lat"]),
        lng=float(request.data["lng"])
    )
    # create post
    post.location = location
    post.content = request.data["content"]
    post.tags.clear()
    # create tag and add to post
    for key in request.data.keys():
        if "postTag" in key:
            tag, _ = Tag.objects.get_or_create(name=request.data[key].strip().replace(' ', ''))
            if tag not in post.tags.all():
                post.tags.add(tag)

    # save image
    for file in request.FILES.getlist('pictures'):
        postimage = PostImage.objects.create(post=post)
        postimage.image.save(
            os.path.basename(file.name),
            File(file)
        )
        postimage.save()

    post.save()
    serializer = PostSerializer(post)
    return Response(status=status.HTTP_200_OK, data=serializer.data)


@permission_classes((IsAuthenticated,))
@api_view(['POST'])  # Post: Create
def add_post(request):
    """
        Adding a post
    """
    passed, errors = validate_post(request)
    if not passed:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=errors)
    # create location
    location, _ = Location.objects.get_or_create(
        name=request.data["googleAddress"],
        lat=float(request.data["lat"]),
        lng=float(request.data["lng"])
    )
    # create post
    post = Post.objects.create(
        author=request.user,
        content=request.data["content"],
        location=location
    )
    # create tag and add to post
    for key in request.data.keys():
        if "postTag" in key:
            tag, _ = Tag.objects.get_or_create(name=request.data[key].strip().replace(' ', ''))
            if tag not in post.tags.all():
                post.tags.add(tag)

    # save image
    for file in request.FILES.getlist('pictures'):
        postimage = PostImage.objects.create(post=post)
        postimage.image.save(
            os.path.basename(file.name),
            File(file)
        )
        postimage.save()

    post.save()
    serializer = PostSerializer(post)
    return Response(status=status.HTTP_200_OK, data=serializer.data)


@permission_classes((IsAuthenticated,))
@api_view(['DELETE'])  # Delete: Delete
@has_postid
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


user_response = openapi.Response('response description', openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={'like-status': openapi.Schema(type=openapi.TYPE_INTEGER, description='True if the post is liked')},
))


@swagger_auto_schema(methods=['put'], request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={'post-id': openapi.Schema(type=openapi.TYPE_INTEGER, description='The id of a post')},
), responses={200: user_response})
@permission_classes((IsAuthenticated,))
@api_view(['PUT'])  # Put: Update/Replace
@has_postid
def toggle_like_post(request, postId):
    """
        Like a post and Cancel a like
    """
    post = get_object_or_404(Post, id=postId)  # test if the post exists
    if Post.objects.filter(id=post.id, likes=request.user).count() == 0:  # the user has not already liked the post
        post.likes.add(request.user)
        data = {"like-status": True}
    else:
        post.likes.remove(request.user)
        data = {"like-status": False}
    return Response(status=status.HTTP_200_OK, data=data)


@permission_classes((IsAuthenticated,))
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


@permission_classes((IsAuthenticated,))
@api_view(['POST'])
def add_album(request):
    album, created = Album.objects.get_or_create(
        user=request.user,
        name=request.data["albumName"]
    )
    if not created:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": f"An album with the name {request.data['albumName']} already exist"})
    serializer = AlbumSerializer(album)
    return Response(status=status.HTTP_200_OK, data=serializer.data)


@permission_classes((IsAuthenticated,))
@api_view(['DELETE'])
def delete_album(request):
    album_qs = Album.objects.filter(
        user=request.user,
        id=request.data["albumId"]
    )
    if album_qs.count() > 0:
        album_qs.first().delete()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': f'album with id {request.data["albumId"]} does not exist'})


@permission_classes((IsAuthenticated,))
@api_view(['PUT'])
def add_post_to_album(request):
    post_qs = Post.objects.filter(
        author=request.user,
        id=request.data["postId"]
    )
    if post_qs.count() == 0:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': f'post with id {request.data["postId"]} does not exist'})

    album_qs = Album.objects.filter(
        user=request.user,
        id=request.data["albumId"]
    )
    if album_qs.count() == 0:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': f'album with id {request.data["albumId"]} does not exist'})

    post = post_qs.first()
    album = album_qs.first()
    if post not in album.posts.all():
        album.posts.add(post)
    return Response(status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
@api_view(['PUT'])
def remove_post_from_album(request):
    post_qs = Post.objects.filter(
        author=request.user,
        id=request.data["postId"]
    )
    if post_qs.count() == 0:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': f'post with id {request.data["postId"]} does not exist'})

    album_qs = Album.objects.filter(
        user=request.user,
        id=request.data["albumId"]
    )
    if album_qs.count() == 0:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': f'album with id {request.data["albumId"]} does not exist'})

    post = post_qs.first()
    album = album_qs.first()
    if post in album.posts.all():
        album.posts.remove(post)
    return Response(status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
@api_view(['PUT'])
def remove_image_from_post(request):
    post_qs = Post.objects.filter(
        author=request.user,
        id=request.data["postId"]
    )
    if post_qs.count() == 0:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': f'post with id {request.data["postId"]} does not exist'})

    image_qs = PostImage.objects.filter(
        id=request.data["imageId"]
    )
    if image_qs.count() == 0:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': f'image with id {request.data["imageId"]} does not exist'})

    post = post_qs.first()
    image = image_qs.first()
    if image in post.postimage_set.all():
        image.delete()
    return Response(status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
@api_view(['GET'])
def get_albums(request):
    albums = Album.objects.filter(user=request.user)
    serializer = AlbumSerializer(albums, many=True)
    return Response(status=status.HTTP_200_OK, data=serializer.data)


@permission_classes((IsAuthenticated,))
@api_view(['GET'])
@has_postid
def get_comments(request, postId):
    post = get_object_or_404(Post, id=postId)

    serializer = CommentSerializer(post.comment_set.all().order_by("creation_date"), many=True)
    return Response(status=status.HTTP_200_OK, data=serializer.data)


@permission_classes((IsAuthenticated,))
@api_view(['PUT'])  # Put: Update/Replace
@has_commentId
def toggle_like_comment(request, commentId):
    """
        Like a comment and Cancel a like
    """
    comment = get_object_or_404(Comment, id=commentId)  # test if the comment exists
    if Comment.objects.filter(id=comment.id, likes=request.user).count() == 0:  # the user has not already liked the post
        comment.likes.add(request.user)
        data = {"like-status": True}
    else:
        comment.likes.remove(request.user)
        data = {"like-status": False}
    return Response(status=status.HTTP_200_OK, data=data)


@permission_classes((IsAuthenticated,))
@api_view(['POST'])
@has_postid
def add_comment(request, postId):
    if "content" not in request.data:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "no content"})
    content = request.data["content"]
    if len(content) > Post.MAX_LENGTH:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "The content of this comment is superior to 150 characters."})
    post = get_object_or_404(Post, id=postId)

    comment = Comment.objects.create(
        author=request.user,
        content=content,
        post=post
    )
    serializer = CommentSerializer(comment)
    return Response(status=status.HTTP_200_OK, data=serializer.data)
