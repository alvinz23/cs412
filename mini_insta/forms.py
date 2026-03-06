"""
Author: Alvin Zhu
Email: alvinz@bu.edu
Description: Forms for creating and updating mini_insta records.
"""

from django import forms

from .models import Post, Profile


class CreatePostForm(forms.ModelForm):
    """Collect user input needed to create a Post."""

    class Meta:
        """Bind this form to the Post model."""

        model = Post
        fields = ["caption"]


class UpdateProfileForm(forms.ModelForm):
    """Collect editable Profile fields for the update page."""

    class Meta:
        """Bind this form to the Profile model."""

        model = Profile
        fields = ["display_name", "profile_image_url", "bio_text"]


class UpdatePostForm(forms.ModelForm):
    """Collect the editable caption field for a Post."""

    class Meta:
        """Bind this form to the Post model."""

        model = Post
        fields = ["caption"]


class CreateProfileForm(forms.ModelForm):
    """Collect data needed to create a new Profile."""

    class Meta:
        """Bind this form to the Profile model."""

        model = Profile
        fields = ["username", "display_name", "profile_image_url", "bio_text"]
