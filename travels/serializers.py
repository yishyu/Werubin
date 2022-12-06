from rest_framework import serializers
from travels.models import Post, Comment, PostImage, Album, Tag, Location





class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = "__all__"


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"

"""
Care not all the fields are present.
Still works on the website.
"""
class PostSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    tags = TagSerializer()
    class Meta:
        model = Post
        fields = ['content','author','location','tags']


"""
Care not all the fields are present.
Still works on the website.
"""
class CommentSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    class Meta:
        model = Comment
        fields = ['author','content','post','likes']