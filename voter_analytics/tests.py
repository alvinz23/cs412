"""
Author: Alvin Zhu
Email: alvinz@bu.edu
Description: Smoke tests for voter_analytics filtering and detail routes.
"""

from django.test import TestCase
from django.urls import reverse

from .models import Voter


class VoterAnalyticsTests(TestCase):
    """Verify voter listing, filtering, detail, and graph pages load correctly."""

    def setUp(self):
        """
        Create a small voter dataset used by test methods.

        Parameters:
        self (VoterAnalyticsTests): The current test case instance.
        """

        Voter.objects.create(
            first_name="Alice",
            last_name="Smith",
            street_number="10",
            street_name="Beacon St",
            apartment_number="",
            zip_code="02458",
            date_of_birth="1980-05-10",
            date_of_registration="2000-06-01",
            party_affiliation="D ",
            precinct_number=1,
            v20state=True,
            v21town=True,
            v21primary=False,
            v22general=True,
            v23town=True,
            voter_score=4,
        )
        Voter.objects.create(
            first_name="Bob",
            last_name="Jones",
            street_number="99",
            street_name="Washington St",
            apartment_number="2A",
            zip_code="02459",
            date_of_birth="1995-01-20",
            date_of_registration="2015-04-01",
            party_affiliation="U ",
            precinct_number=2,
            v20state=False,
            v21town=False,
            v21primary=False,
            v22general=True,
            v23town=False,
            voter_score=1,
        )

    def test_voters_page_loads(self):
        """
        Verify the voter list route returns HTTP 200.

        Parameters:
        self (VoterAnalyticsTests): The current test case instance.
        """

        response = self.client.get(reverse("voters"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice Smith")
        self.assertContains(response, "Bob Jones")

    def test_voters_filter_by_party(self):
        """
        Verify filtering by party affiliation narrows list results.

        Parameters:
        self (VoterAnalyticsTests): The current test case instance.
        """

        response = self.client.get(reverse("voters"), {"party": "D "})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice Smith")
        self.assertNotContains(response, "Bob Jones")

    def test_voter_detail_page_loads(self):
        """
        Verify the voter detail route returns HTTP 200.

        Parameters:
        self (VoterAnalyticsTests): The current test case instance.
        """

        voter = Voter.objects.first()
        response = self.client.get(reverse("voter", kwargs={"pk": voter.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Open in Google Maps")

    def test_graphs_page_loads(self):
        """
        Verify graphs route returns HTTP 200.

        Parameters:
        self (VoterAnalyticsTests): The current test case instance.
        """

        response = self.client.get(reverse("graphs"))
        self.assertEqual(response.status_code, 200)

# Create your tests here.
