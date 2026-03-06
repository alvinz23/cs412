"""
Author: Alvin Zhu
Email: alvinz@bu.edu
Description: Smoke tests for mini_insta authentication and core features.
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Comment, Follow, Like, Photo, Post, Profile


class MiniInstaTests(TestCase):
    """Verify core mini_insta model and auth-backed view behaviors."""

    def setUp(self):
        """
        Create a small data set shared across the smoke tests.

        Parameters:
        self (MiniInstaTests): The current test case instance.
        """

        self.alice_user = User.objects.create_user(
            username="alice_user",
            password="pass12345",
        )
        self.bob_user = User.objects.create_user(
            username="bob_user",
            password="pass12345",
        )
        self.alice = Profile.objects.create(
            user=self.alice_user,
            username="alice",
            display_name="Alice",
            profile_image_url="https://example.com/alice.jpg",
            bio_text="Photographer",
            join_date="2026-01-01",
        )
        self.bob = Profile.objects.create(
            user=self.bob_user,
            username="bob",
            display_name="Bob",
            profile_image_url="https://example.com/bob.jpg",
            bio_text="Traveler",
            join_date="2026-01-02",
        )
        self.post = Post.objects.create(profile=self.alice, caption="Trip to Boston")
        Photo.objects.create(
            post=self.post,
            image_url="https://example.com/post.jpg",
        )
        Comment.objects.create(post=self.post, profile=self.bob, text="Nice photo")
        Like.objects.create(post=self.post, profile=self.bob)
        Follow.objects.create(profile=self.alice, follower_profile=self.bob)

    def test_photo_get_image_url_prefers_stored_url(self):
        """
        Verify Photo returns the legacy image_url when present.

        Parameters:
        self (MiniInstaTests): The current test case instance.
        """

        photo = self.post.get_all_photos().first()
        self.assertEqual(photo.get_image_url(), "https://example.com/post.jpg")

    def test_profile_follow_accessors(self):
        """
        Verify follower and following helper methods return Profiles.

        Parameters:
        self (MiniInstaTests): The current test case instance.
        """

        self.assertEqual(self.alice.get_num_followers(), 1)
        self.assertEqual(self.bob.get_num_following(), 1)
        self.assertEqual(self.alice.get_followers()[0], self.bob)
        self.assertEqual(self.bob.get_following()[0], self.alice)

    def test_profile_feed_contains_followed_profile_posts(self):
        """
        Verify the feed includes posts from followed Profiles.

        Parameters:
        self (MiniInstaTests): The current test case instance.
        """

        feed_posts = list(self.bob.get_post_feed())
        self.assertEqual(feed_posts, [self.post])

    def test_search_view_returns_matching_post_and_profile(self):
        """
        Verify the search results page includes both result groups.

        Parameters:
        self (MiniInstaTests): The current test case instance.
        """

        self.assertEqual(self.client.login(username="bob_user", password="pass12345"), True)
        response = self.client.get(reverse("search"), {"query": "Boston"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Trip to Boston")
        self.assertContains(response, "Matching Profiles")

    def test_create_post_requires_login(self):
        """
        Verify unauthenticated requests redirect to login for create post.

        Parameters:
        self (MiniInstaTests): The current test case instance.
        """

        response = self.client.get(reverse("create_post"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_like_post_for_other_profile(self):
        """
        Verify a logged-in profile can like another profile's post.

        Parameters:
        self (MiniInstaTests): The current test case instance.
        """

        self.assertEqual(self.client.login(username="bob_user", password="pass12345"), True)
        response = self.client.post(reverse("like_post", kwargs={"pk": self.post.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Like.objects.filter(post=self.post, profile=self.bob).exists())
