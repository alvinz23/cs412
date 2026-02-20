"""
Author: Alvin Zhu
Email: alvinz@bu.edu
Description: Forms for creating mini_insta post records.
"""

from django import forms

from .models import Post


class CreatePostForm(forms.ModelForm):
    """Collect user input needed to create a Post and initial Photo."""

    image_url = forms.URLField(label="Image URL")

    class Meta:
        """Bind this form to the Post model."""

        model = Post
        fields = ["caption"]
