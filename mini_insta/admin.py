"""
Author: Alvin Zhu
Email: alvinz@bu.edu
Description: Admin registrations for mini_insta models.
"""

from django.contrib import admin

from .models import Photo, Post, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Define Django admin options for Profile records."""

    list_display = ("username", "display_name", "join_date")
    search_fields = ("username", "display_name")


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
