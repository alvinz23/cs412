from rest_framework import serializers
from .models import Profile, Post, Photo


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "username", "display_name", "profile_image_url", "bio_text", "join_date"]


class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ["id", "image", "timestamp"]

    def get_image(self, obj):
        return obj.get_image_url()


class PostSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()
    profile_id = serializers.IntegerField(source="profile.id", read_only=True)
    profile_username = serializers.CharField(source="profile.username", read_only=True)
    profile_display_name = serializers.CharField(source="profile.display_name", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "profile_id",
            "profile_username",
            "profile_display_name",
            "caption",
            "timestamp",
            "photos",
        ]

    def get_photos(self, obj):
        return PhotoSerializer(obj.get_all_photos(), many=True).data


class CreatePostSerializer(serializers.Serializer):
    caption = serializers.CharField(required=False, allow_blank=True, default="")
    image_url = serializers.URLField(required=False, allow_blank=True, default="")
