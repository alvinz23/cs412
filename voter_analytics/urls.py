"""
Author: Alvin Zhu
Email: alvinz@bu.edu
Description: URL patterns for the voter_analytics application.
"""

from django.urls import path

from .views import GraphListView, VoterDetailView, VoterListView

urlpatterns = [
    path("", VoterListView.as_view(), name="voters"),
    path("voter/<int:pk>", VoterDetailView.as_view(), name="voter"),
    path("graphs", GraphListView.as_view(), name="graphs"),
]
