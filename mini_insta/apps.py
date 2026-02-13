"""
Author: Alvin Zhu
Email: alvinz@bu.edu
Description: App configuration for the mini_insta Django application.
"""

from django.apps import AppConfig


class MiniInstaConfig(AppConfig):
    """Configure metadata for the mini_insta app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "mini_insta"
