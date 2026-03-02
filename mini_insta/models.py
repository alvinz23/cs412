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

    def get_followers(self):
        """
        Return a list of Profiles that follow this profile.

        Parameters:
        self (Profile): The current profile instance.
        """

        follows = Follow.objects.filter(profile=self).select_related("follower_profile")
        return [follow.follower_profile for follow in follows]

    def get_num_followers(self):
        """
        Return the number of followers for this profile.

        Parameters:
        self (Profile): The current profile instance.
        """

        return Follow.objects.filter(profile=self).count()

    def get_following(self):
        """
        Return a list of Profiles followed by this profile.

        Parameters:
        self (Profile): The current profile instance.
        """

        follows = Follow.objects.filter(follower_profile=self).select_related("profile")
        return [follow.profile for follow in follows]

    def get_num_following(self):
        """
        Return the number of profiles followed by this profile.

        Parameters:
        self (Profile): The current profile instance.
        """

        return Follow.objects.filter(follower_profile=self).count()

    def get_post_feed(self):
        """
        Return posts created by profiles followed by this profile.

        Parameters:
        self (Profile): The current profile instance.
        """

        followed_ids = Follow.objects.filter(
            follower_profile=self
        ).values_list("profile_id", flat=True)
        return Post.objects.filter(profile_id__in=followed_ids).order_by("-timestamp")

    def get_absolute_url(self):
        """
        Return the canonical detail URL for this profile.

        Parameters:
        self (Profile): The current profile instance.
        """

        return reverse("show_profile", kwargs={"pk": self.pk})


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

    def get_all_comments(self):
        """
        Return all comments for this post, newest first.

        Parameters:
        self (Post): The current post instance.
        """

        return Comment.objects.filter(post=self).order_by("-timestamp")

    def get_likes(self):
        """
        Return all likes for this post.

        Parameters:
        self (Post): The current post instance.
        """

        return Like.objects.filter(post=self).order_by("-timestamp")


class Photo(models.Model):
    """Represent one photo associated with a post."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(upload_to="mini_insta/", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return a readable string representation of this photo.

        Parameters:
        self (Photo): The current photo instance.
        """

        return f"Photo {self.pk}: {self.get_image_url()}"

    def get_image_url(self):
        """
        Return the stored URL or uploaded media URL for this photo.

        Parameters:
        self (Photo): The current photo instance.
        """

        if self.image_url:
            return self.image_url
        if self.image_file:
            return self.image_file.url
        return ""


class Follow(models.Model):
    """Represent one follow relationship between two profiles."""

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="profile"
    )
    follower_profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="follower_profile"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return a readable string representation of this follow.

        Parameters:
        self (Follow): The current follow instance.
        """

        return f"{self.follower_profile.display_name} follows {self.profile.display_name}"


class Comment(models.Model):
    """Represent one comment left by a profile on a post."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        """
        Return a readable string representation of this comment.

        Parameters:
        self (Comment): The current comment instance.
        """

        short_text = self.text[:40] if self.text else "(no text)"
        return f"Comment by {self.profile.username} on Post {self.post_id}: {short_text}"


class Like(models.Model):
    """Represent one like left by a profile on a post."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return a readable string representation of this like.

        Parameters:
        self (Like): The current like instance.
        """

        return f"{self.profile.username} likes Post {self.post_id}"
