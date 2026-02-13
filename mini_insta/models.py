"""
Author: Alvin Zhu
Email: alvinz@bu.edu
Description: Data models for the mini_insta application.
"""

from django.db import models


class Profile(models.Model):
    """Represent one mini_insta user profile."""

    username = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    profile_image_url = models.URLField()
    bio_text = models.TextField()
    join_date = models.DateField()

    def __str__(self):
        """
        Return a readable string representation of this profile.

        Parameters:
        self (Profile): The current profile instance.
        """

        return f"{self.username} ({self.display_name})"
