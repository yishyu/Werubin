from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.decorators import login_required
from travels.models import Post
from travels.serializers import PostSerializer, CommentSerializer
from travels.forms import PostForm, CommentForm


@api_view(['POST'])
def add_post(request):
    print(request.POST)
    print(request.GET)
    print(request.data)
    form = PostForm(request.data)
    print(form.errors)
    if form.is_valid() :
        print("ratio")
        formA = form.save()
        print("works")
        serializer = PostSerializer([formA], context={'request': request}, many=True)
        return Response(serializer.data)
    return Response(
            status=status.HTTP_400_BAD_REQUEST
)

@api_view(['POST'])
def add_comment(request):
    form = CommentForm(request.data)
    if form.is_valid():
        formA = form.save()
        serializer = CommentSerializer([formA], context={'request': request}, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def delete_post(request):
    inst = Post.objects.get(id=request['post-id'])
    inst.delete()

