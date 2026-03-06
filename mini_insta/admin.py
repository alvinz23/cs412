"""
Author: Alvin Zhu
Email: alvinz@bu.edu
Description: Admin registrations for mini_insta models.
"""

from django.contrib import admin

from .models import Comment, Follow, Like, Photo, Post, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Define Django admin options for Profile records."""

    list_display = ("username", "display_name", "user", "join_date")
    search_fields = ("username", "display_name", "user__username")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Define Django admin options for Post records."""

    list_display = ("id", "profile", "timestamp")
    list_filter = ("profile", "timestamp")
    search_fields = ("caption", "profile__username", "profile__display_name")


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Define Django admin options for Photo records."""

    list_display = ("id", "post", "timestamp")
    list_filter = ("timestamp",)
    search_fields = ("image_url", "post__caption")


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Define Django admin options for Follow records."""

    list_display = ("id", "follower_profile", "profile", "timestamp")
    list_filter = ("timestamp",)
    search_fields = (
        "profile__username",
        "profile__display_name",
        "follower_profile__username",
        "follower_profile__display_name",
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Define Django admin options for Comment records."""

    list_display = ("id", "post", "profile", "timestamp")
    list_filter = ("timestamp",)
    search_fields = ("text", "profile__username", "post__caption")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """Define Django admin options for Like records."""

    list_display = ("id", "post", "profile", "timestamp")
    list_filter = ("timestamp",)
    search_fields = ("profile__username", "post__caption")
