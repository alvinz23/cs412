"""
Author: Alvin Zhu
Email: alvinz@bu.edu
Description: URL patterns for the mini_insta application.
"""

from django.contrib.auth import views as auth_views
from django.urls import path

from . import api_views
from .views import (
    CreatePostView,
    CreateProfileView,
    DeleteFollowProfileView,
    DeleteLikePostView,
    DeletePostView,
    FollowProfileView,
    LikePostView,
    LogoutConfirmationView,
    MyProfileDetailView,
    PostDetailView,
    PostFeedListView,
    ProfileDetailView,
    ProfileListView,
    SearchView,
    ShowFollowersDetailView,
    ShowFollowingDetailView,
    UpdatePostView,
    UpdateProfileView,
)

urlpatterns = [
    # API routes used by the React Native app.
    path("api/login", api_views.api_login, name="api_login"),
    path("api/profiles", api_views.api_profiles, name="api_profiles"),
    path("api/profile/<int:pk>", api_views.api_profile, name="api_profile"),
    path("api/profile/<int:pk>/posts", api_views.api_profile_posts, name="api_profile_posts"),
    path("api/profile/<int:pk>/feed", api_views.api_profile_feed, name="api_profile_feed"),
    path("api/posts", api_views.api_create_post, name="api_create_post"),
    path("", ProfileListView.as_view(), name="show_all_profiles"),
    path("create_profile", CreateProfileView.as_view(), name="create_profile"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="mini_insta/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="logout_confirmation"),
        name="logout",
    ),
    path(
        "logout_confirmation",
        LogoutConfirmationView.as_view(),
        name="logout_confirmation",
    ),
    path("profile", MyProfileDetailView.as_view(), name="show_my_profile"),
    path("profile/<int:pk>", ProfileDetailView.as_view(), name="show_profile"),
    path("profile/update", UpdateProfileView.as_view(), name="update_profile"),
    path("profile/<int:pk>/followers", ShowFollowersDetailView.as_view(), name="show_followers"),
    path("profile/<int:pk>/following", ShowFollowingDetailView.as_view(), name="show_following"),
    path("profile/feed", PostFeedListView.as_view(), name="show_feed"),
    path("profile/search", SearchView.as_view(), name="search"),
    path("profile/create_post", CreatePostView.as_view(), name="create_post"),
    path("profile/<int:pk>/follow", FollowProfileView.as_view(), name="follow_profile"),
    path(
        "profile/<int:pk>/delete_follow",
        DeleteFollowProfileView.as_view(),
        name="delete_follow_profile",
    ),
    path("post/<int:pk>", PostDetailView.as_view(), name="show_post"),
    path("post/<int:pk>/delete", DeletePostView.as_view(), name="delete_post"),
    path("post/<int:pk>/update", UpdatePostView.as_view(), name="update_post"),
    path("post/<int:pk>/like", LikePostView.as_view(), name="like_post"),
    path("post/<int:pk>/delete_like", DeleteLikePostView.as_view(), name="delete_like_post"),
]
