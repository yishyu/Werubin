from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()

    def profile_pic(self, obj):
        return obj.profile_pic.url if obj.profile_pic else None

    def get_tags(self, obj):
        from travels.serializers import TagSerializer
        return TagSerializer(
            obj.tags.all(),
            many=True,
        ).data

    class Meta:
        model = User
        exclude = ('password', 'last_login', "is_staff", "is_active", "groups", "user_permissions")


class PostUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "profile_picture", "first_name", "last_name"]
