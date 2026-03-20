"""
Author: Alvin Zhu
Email: alvinz@bu.edu
Description: Admin registration for voter_analytics models.
"""

from django.contrib import admin

from .models import Voter


@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    """Configure Django admin display for voter records."""

    list_display = (
        "last_name",
        "first_name",
        "street_number",
        "street_name",
        "party_affiliation",
        "voter_score",
    )
    list_filter = (
        "party_affiliation",
        "precinct_number",
        "voter_score",
        "v20state",
        "v21town",
        "v21primary",
        "v22general",
        "v23town",
    )
    search_fields = (
        "first_name",
        "last_name",
        "street_name",
        "zip_code",
    )

# Register your models here.
