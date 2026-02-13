"""
Author: Alvin Zhu
Email: alvinz@bu.edu
Description: URL patterns for the mini_insta application.
"""

from django.urls import path

from .views import ProfileDetailView, ProfileListView

urlpatterns = [
    path("", ProfileListView.as_view(), name="show_all_profiles"),
    path("profile/<int:pk>", ProfileDetailView.as_view(), name="show_profile"),
]
