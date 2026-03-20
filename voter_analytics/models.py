"""
Author: Alvin Zhu
Email: alvinz@bu.edu
Description: Models and CSV data loading utilities for voter_analytics.
"""

import csv
from datetime import datetime
from pathlib import Path

from django.db import models


class Voter(models.Model):
    """Represent one Newton voter record."""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=20)
    street_name = models.CharField(max_length=200)
    apartment_number = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.IntegerField()
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    voter_score = models.IntegerField(default=0)

    def __str__(self):
        """
        Return a compact string representation for one voter.

        Parameters:
        self (Voter): The current voter instance.
        """

        return f"{self.last_name}, {self.first_name} ({self.party_affiliation.strip()})"

    def get_street_address(self):
        """
        Return a single-line street address.

        Parameters:
        self (Voter): The current voter instance.
        """

        parts = [self.street_number, self.street_name]
        if self.apartment_number:
            parts.append(f"Apt {self.apartment_number}")
        parts.append(self.zip_code)
        return ", ".join(parts)

    def get_google_maps_url(self):
        """
        Return the Google Maps URL for this voter's street address.

        Parameters:
        self (Voter): The current voter instance.
        """

        query = f"{self.street_number} {self.street_name} Newton MA {self.zip_code}"
        query = "+".join(query.split())
        return f"https://www.google.com/maps/search/?api=1&query={query}"


def _parse_date(value):
    """
    Parse a CSV date string in common formats to a Python date.

    Parameters:
    value (str): The input date text.
    """

    value = (value or "").strip()
    if not value:
        return None

    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def _parse_bool(value):
    """
    Parse a CSV yes/no field to a Python boolean.

    Parameters:
    value (str): The input text to parse.
    """

    normalized = (value or "").strip().upper()
    return normalized in {"1", "Y", "YES", "TRUE", "T"}


def _get_row_value(row, *keys):
    """
    Return the first matching key value from one CSV row dictionary.

    Parameters:
    row (dict): One row of data from csv.DictReader.
    keys (tuple[str]): Candidate column names to search.
    """

    for key in keys:
        if key in row:
            return row[key]
    return ""


def load_data(csv_file_path="newton_voters.csv", clear_existing=False):
    """
    Load voter records from a CSV file into the database.

    Parameters:
    csv_file_path (str): Path to the CSV file to import.
    clear_existing (bool): Whether to delete existing Voter rows first.
    """

    csv_path = Path(csv_file_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    if clear_existing:
        Voter.objects.all().delete()

    created_count = 0
    with csv_path.open(newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            dob = _parse_date(_get_row_value(row, "Date of Birth"))
            reg_date = _parse_date(_get_row_value(row, "Date of Registration"))
            if dob is None or reg_date is None:
                continue

            voter, created = Voter.objects.get_or_create(
                first_name=_get_row_value(row, "First Name").strip(),
                last_name=_get_row_value(row, "Last Name").strip(),
                street_number=_get_row_value(
                    row,
                    "Residential Address - Street Number",
                    "Residential Address - House Number",
                ).strip(),
                street_name=_get_row_value(row, "Residential Address - Street Name").strip(),
                apartment_number=_get_row_value(
                    row,
                    "Residential Address - Apartment Number",
                ).strip(),
                zip_code=_get_row_value(row, "Residential Address - Zip Code").strip(),
                defaults={
                    "date_of_birth": dob,
                    "date_of_registration": reg_date,
                    "party_affiliation": _get_row_value(
                        row,
                        "Party Affiliation",
                    )[:2],
                    "precinct_number": int(
                        _get_row_value(row, "Precinct Number").strip() or 0
                    ),
                    "v20state": _parse_bool(_get_row_value(row, "v20state")),
                    "v21town": _parse_bool(_get_row_value(row, "v21town")),
                    "v21primary": _parse_bool(_get_row_value(row, "v21primary")),
                    "v22general": _parse_bool(_get_row_value(row, "v22general")),
                    "v23town": _parse_bool(_get_row_value(row, "v23town")),
                    "voter_score": int(_get_row_value(row, "voter_score").strip() or 0),
                },
            )
            if created:
                created_count += 1
            else:
                voter.date_of_birth = dob
                voter.date_of_registration = reg_date
                voter.party_affiliation = _get_row_value(row, "Party Affiliation")[:2]
                voter.precinct_number = int(
                    _get_row_value(row, "Precinct Number").strip() or 0
                )
                voter.v20state = _parse_bool(_get_row_value(row, "v20state"))
                voter.v21town = _parse_bool(_get_row_value(row, "v21town"))
                voter.v21primary = _parse_bool(_get_row_value(row, "v21primary"))
                voter.v22general = _parse_bool(_get_row_value(row, "v22general"))
                voter.v23town = _parse_bool(_get_row_value(row, "v23town"))
                voter.voter_score = int(_get_row_value(row, "voter_score").strip() or 0)
                voter.save()

    return created_count

# Create your models here.
