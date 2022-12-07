from rest_framework import serializers
from travels.models import Post, Comment, PostImage, Album, Tag, Location
from users.serializers import PostUserSerializer


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ("id", "image")


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


class PostSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    shares = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()

    def get_comment(self, obj):
        return CommentSerializer(
            obj.comment_set.all(),
            many=True
        ).data

    def get_author(self, obj):
        return PostUserSerializer(
            obj.author
        ).data

    def get_images(self, obj):
        return PostImageSerializer(
            obj.postimage_set.all(),
            many=True
        ).data

    def get_likes(self, obj):
        return PostUserSerializer(
            obj.likes.all(),
            many=True
        ).data

    def get_shares(self, obj):
        return PostSerializer(
            obj.shares
        ).data

    def get_location(self, obj):
        return LocationSerializer(
            obj.location
        ).data

    def get_tags(self, obj):
        return TagSerializer(
            obj.tags.all(),
            many=True,
        ).data

    class Meta:
        model = Post
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return PostUserSerializer(
            obj.author
        ).data

    def get_likes(self, obj):
        return PostUserSerializer(
            obj.likes.all(),
            many=True
        ).data

    class Meta:
        model = Comment
        exclude = ("post", )
