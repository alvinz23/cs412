"""
Author: Alvin Zhu
Email: alvinz@bu.edu
Description: Class-based views for listing and viewing mini_insta profiles.
"""

from django.views.generic import DetailView, ListView

from .models import Profile


class ProfileListView(ListView):
    """Display all Profile records on one page."""

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"


class ProfileDetailView(DetailView):
    """Display one Profile record using its primary key."""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"
