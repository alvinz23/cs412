"""
Author: Alvin Zhu
Email: alvinz@bu.edu
Description: Data models for the mini_insta application.
"""

from django.db import models
from django.urls import reverse


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

    def get_all_posts(self):
        """
        Return all posts created by this profile, newest first.

        Parameters:
        self (Profile): The current profile instance.
        """

        return Post.objects.filter(profile=self).order_by("-timestamp")


class Post(models.Model):
    """Represent one post created by a profile."""

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        """
        Return a readable string representation of this post.

        Parameters:
        self (Post): The current post instance.
        """

        short_caption = self.caption[:40] if self.caption else "(no caption)"
        return f"Post {self.pk} by {self.profile.username}: {short_caption}"

    def get_all_photos(self):
        """
        Return all photos for this post, ordered by timestamp.

        Parameters:
        self (Post): The current post instance.
        """

        return Photo.objects.filter(post=self).order_by("timestamp")

    def get_absolute_url(self):
        """
        Return the canonical detail URL for this post.

        Parameters:
        self (Post): The current post instance.
        """

        return reverse("show_post", kwargs={"pk": self.pk})


class Photo(models.Model):
    """Represent one photo associated with a post."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return a readable string representation of this photo.

        Parameters:
        self (Photo): The current photo instance.
        """

        return f"Photo {self.pk} for Post {self.post_id}"
