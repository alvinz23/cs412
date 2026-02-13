"""
Author: Alvin Zhu
Email: alvinz@bu.edu
Description: Admin registrations for mini_insta models.
"""

from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Define Django admin options for Profile records."""

    list_display = ("username", "display_name", "join_date")
    search_fields = ("username", "display_name")
