from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Profile, Post, Photo
from .api_serializers import (
    ProfileSerializer,
    PostSerializer,
    CreatePostSerializer,
)


@api_view(["POST"])
@permission_classes([AllowAny])
def api_login(request):
    # Login endpoint: checks username/password and returns token.
    username = request.data.get("username", "")
    password = request.data.get("password", "")
    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)
    profile = Profile.objects.filter(user=user).order_by("id").first()

    return Response(
        {
            "token": token.key,
            "user_id": user.id,
            "profile_id": profile.id if profile else None,
            "username": user.username,
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_profiles(request):
    # Return all profiles (token required).
    profiles = Profile.objects.all().order_by("id")
    return Response(ProfileSerializer(profiles, many=True).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_profile(request, pk):
    # Return one profile by id.
    profile = get_object_or_404(Profile, pk=pk)
    return Response(ProfileSerializer(profile).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_profile_posts(request, pk):
    # Return posts for one profile.
    profile = get_object_or_404(Profile, pk=pk)
    posts = profile.get_all_posts()
    return Response(PostSerializer(posts, many=True).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_profile_feed(request, pk):
    # Return feed for one profile (people this profile follows).
    profile = get_object_or_404(Profile, pk=pk)
    posts = profile.get_post_feed()
    return Response(PostSerializer(posts, many=True).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_create_post(request):
    # Create a post for currently authenticated user.
    serializer = CreatePostSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # We always use request.user -> profile, not profile id from client.
    profile = Profile.objects.filter(user=request.user).order_by("id").first()
    if profile is None:
        return Response({"detail": "No profile for this user."}, status=status.HTTP_400_BAD_REQUEST)

    post = Post.objects.create(
        profile=profile,
        caption=serializer.validated_data.get("caption", ""),
    )

    image_url = serializer.validated_data.get("image_url", "")
    if image_url:
        # Optional image URL.
        Photo.objects.create(post=post, image_url=image_url)

    return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
