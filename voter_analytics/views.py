"""
Author: Alvin Zhu
Email: alvinz@bu.edu
Description: Views for voter listing, filtering, detail, and graphing.
"""

from django.db.models import Count, Q
from django.db.models.functions import ExtractYear
from django.views.generic import DetailView, ListView

from .models import Voter


class VoterFilterMixin:
    """Provide shared filtering logic for list and graph pages."""

    election_fields = ["v20state", "v21town", "v21primary", "v22general", "v23town"]

    def get_filtered_queryset(self):
        """
        Return a filtered queryset of voters based on GET parameters.

        Parameters:
        self (VoterFilterMixin): The current view instance.
        """

        queryset = Voter.objects.all().order_by("last_name", "first_name")
        params = self.request.GET

        selected_party = params.get("party", "")
        if selected_party:
            queryset = queryset.filter(party_affiliation=selected_party)

        min_year = params.get("min_year", "").strip()
        if min_year:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_year))

        max_year = params.get("max_year", "").strip()
        if max_year:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_year))

        selected_score = params.get("voter_score", "").strip()
        if selected_score:
            queryset = queryset.filter(voter_score=int(selected_score))

        for field in self.election_fields:
            if params.get(field) == "on":
                queryset = queryset.filter(**{field: True})

        return queryset

    def get_filter_context(self):
        """
        Return reusable filter metadata and selected values.

        Parameters:
        self (VoterFilterMixin): The current view instance.
        """

        params = self.request.GET
        party_choices = (
            Voter.objects.values_list("party_affiliation", flat=True)
            .distinct()
            .order_by("party_affiliation")
        )
        year_values = (
            Voter.objects.annotate(birth_year=ExtractYear("date_of_birth"))
            .values_list("birth_year", flat=True)
            .distinct()
            .order_by("birth_year")
        )
        score_values = (
            Voter.objects.values_list("voter_score", flat=True)
            .distinct()
            .order_by("voter_score")
        )

        context = {
            "party_choices": party_choices,
            "year_choices": year_values,
            "score_choices": score_values,
            "selected_party": params.get("party", ""),
            "selected_min_year": params.get("min_year", "").strip(),
            "selected_max_year": params.get("max_year", "").strip(),
            "selected_score": params.get("voter_score", "").strip(),
            "selected_elections": {
                field: params.get(field) == "on" for field in self.election_fields
            },
        }
        return context


class VoterListView(VoterFilterMixin, ListView):
    """Display and filter voter records with pagination."""

    model = Voter
    template_name = "voter_analytics/voters.html"
    context_object_name = "voters"
    paginate_by = 100

    def get_queryset(self):
        """
        Return filtered voter records.

        Parameters:
        self (VoterListView): The current view instance.
        """

        return self.get_filtered_queryset()

    def get_context_data(self, **kwargs):
        """
        Add filter metadata to template context.

        Parameters:
        kwargs (dict): Additional keyword arguments from Django.
        """

        context = super().get_context_data(**kwargs)
        context.update(self.get_filter_context())
        return context


class VoterDetailView(DetailView):
    """Display all fields for one voter record."""

    model = Voter
    template_name = "voter_analytics/voter.html"
    context_object_name = "voter"


class GraphListView(VoterFilterMixin, ListView):
    """Display filtered voter data plus aggregate Plotly graphs."""

    model = Voter
    template_name = "voter_analytics/graphs.html"
    context_object_name = "voters"
    paginate_by = 100

    def get_queryset(self):
        """
        Return filtered voter records.

        Parameters:
        self (GraphListView): The current view instance.
        """

        return self.get_filtered_queryset()

    def _build_plotly_graphs(self, queryset):
        """
        Build three Plotly graph divs from the filtered queryset.

        Parameters:
        self (GraphListView): The current view instance.
        queryset (QuerySet): The filtered voter queryset.
        """

        try:
            import plotly.graph_objects as go
            from plotly.offline import plot
        except ImportError:
            return {
                "birth_year_graph": "<p>Install plotly to render graphs.</p>",
                "party_graph": "<p>Install plotly to render graphs.</p>",
                "election_graph": "<p>Install plotly to render graphs.</p>",
            }

        by_year = (
            queryset.annotate(birth_year=ExtractYear("date_of_birth"))
            .values("birth_year")
            .annotate(total=Count("id"))
            .order_by("birth_year")
        )
        year_x = [item["birth_year"] for item in by_year if item["birth_year"] is not None]
        year_y = [item["total"] for item in by_year if item["birth_year"] is not None]
        birth_fig = go.Figure(data=[go.Bar(x=year_x, y=year_y)])
        birth_fig.update_layout(
            title="Distribution of Voters by Birth Year",
            xaxis_title="Birth Year",
            yaxis_title="Number of Voters",
        )

        by_party = (
            queryset.values("party_affiliation")
            .annotate(total=Count("id"))
            .order_by("party_affiliation")
        )
        party_labels = [item["party_affiliation"].strip() or "(blank)" for item in by_party]
        party_values = [item["total"] for item in by_party]
        party_fig = go.Figure(data=[go.Pie(labels=party_labels, values=party_values)])
        party_fig.update_layout(title="Distribution of Voters by Party Affiliation")

        election_counts = queryset.aggregate(
            v20state_total=Count("id", filter=Q(v20state=True)),
            v21town_total=Count("id", filter=Q(v21town=True)),
            v21primary_total=Count("id", filter=Q(v21primary=True)),
            v22general_total=Count("id", filter=Q(v22general=True)),
            v23town_total=Count("id", filter=Q(v23town=True)),
        )
        election_names = ["v20state", "v21town", "v21primary", "v22general", "v23town"]
        election_totals = [
            election_counts["v20state_total"],
            election_counts["v21town_total"],
            election_counts["v21primary_total"],
            election_counts["v22general_total"],
            election_counts["v23town_total"],
        ]
        election_fig = go.Figure(data=[go.Bar(x=election_names, y=election_totals)])
        election_fig.update_layout(
            title="Voter Participation by Election",
            xaxis_title="Election",
            yaxis_title="Number of Voters",
        )

        return {
            "birth_year_graph": plot(birth_fig, output_type="div", include_plotlyjs=True),
            "party_graph": plot(party_fig, output_type="div", include_plotlyjs=False),
            "election_graph": plot(election_fig, output_type="div", include_plotlyjs=False),
        }

    def get_context_data(self, **kwargs):
        """
        Add filter metadata and graph divs to context.

        Parameters:
        kwargs (dict): Additional keyword arguments from Django.
        """

        context = super().get_context_data(**kwargs)
        context.update(self.get_filter_context())
        context.update(self._build_plotly_graphs(self.object_list))
        return context
