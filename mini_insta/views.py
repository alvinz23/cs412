"""
Author: Alvin Zhu
Email: alvinz@bu.edu
Description: Class-based views for the mini_insta application.
"""

from datetime import date

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import CreatePostForm, CreateProfileForm, UpdatePostForm, UpdateProfileForm
from .models import Follow, Like, Photo, Post, Profile


class UserProfileContextMixin:
    """Provide helpers for retrieving the Profile of request.user."""

    def get_user_profile(self):
        """
        Return the first Profile for request.user or None.

        Parameters:
        self (UserProfileContextMixin): The current view instance.
        """

        if not self.request.user.is_authenticated:
            return None
        return Profile.objects.filter(user=self.request.user).order_by("id").first()

    def add_user_profile_context(self, context):
        """
        Add user_profile to the template context dictionary.

        Parameters:
        self (UserProfileContextMixin): The current view instance.
        context (dict): The context dictionary to modify.
        """

        context["user_profile"] = self.get_user_profile()
        return context


class MiniInstaLoginRequiredMixin(LoginRequiredMixin, UserProfileContextMixin):
    """Require auth and use the mini_insta login URL."""

    def get_login_url(self):
        """
        Return the login URL for mini_insta.

        Parameters:
        self (MiniInstaLoginRequiredMixin): The current view instance.
        """

        return reverse("login")


class OwnedProfileRequiredMixin(MiniInstaLoginRequiredMixin, UserPassesTestMixin):
    """Allow access only when request.user owns the target Profile."""

    def test_func(self):
        """
        Return True when the target Profile belongs to request.user.

        Parameters:
        self (OwnedProfileRequiredMixin): The current view instance.
        """

        profile = self.get_object()
        return profile.user == self.request.user


class OwnedPostRequiredMixin(MiniInstaLoginRequiredMixin, UserPassesTestMixin):
    """Allow access only when request.user owns the target Post."""

    def test_func(self):
        """
        Return True when the target Post belongs to request.user.

        Parameters:
        self (OwnedPostRequiredMixin): The current view instance.
        """

        post = self.get_object()
        return post.profile.user == self.request.user


class ProfileListView(UserProfileContextMixin, ListView):
    """Display all Profile records on one page."""

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

    def get_context_data(self, **kwargs):
        """
        Add user_profile to context.

        Parameters:
        kwargs (dict): Additional keyword arguments from Django.
        """

        context = super().get_context_data(**kwargs)
        return self.add_user_profile_context(context)


class ProfileDetailView(UserProfileContextMixin, DetailView):
    """Display one Profile record using its primary key."""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        """
        Add user_profile to context.

        Parameters:
        kwargs (dict): Additional keyword arguments from Django.
        """

        context = super().get_context_data(**kwargs)
        return self.add_user_profile_context(context)


class MyProfileDetailView(MiniInstaLoginRequiredMixin, DetailView):
    """Display the Profile associated with request.user."""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def dispatch(self, request, *args, **kwargs):
        """
        Redirect to profile creation when request.user has no Profile.

        Parameters:
        request (HttpRequest): The current request object.
        args (tuple): Additional positional arguments from Django.
        kwargs (dict): Additional keyword arguments from Django.
        """

        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not Profile.objects.filter(user=request.user).exists():
            return redirect("create_profile")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """
        Return request.user's Profile.

        Parameters:
        self (MyProfileDetailView): The current view instance.
        queryset (QuerySet): Optional queryset parameter from Django.
        """

        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        """
        Add user_profile to context.

        Parameters:
        kwargs (dict): Additional keyword arguments from Django.
        """

        context = super().get_context_data(**kwargs)
        return self.add_user_profile_context(context)


class ShowFollowersDetailView(UserProfileContextMixin, DetailView):
    """Display the follower list for one Profile."""

    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        """
        Add user_profile to context.

        Parameters:
        kwargs (dict): Additional keyword arguments from Django.
        """

        context = super().get_context_data(**kwargs)
        return self.add_user_profile_context(context)


class ShowFollowingDetailView(UserProfileContextMixin, DetailView):
    """Display the following list for one Profile."""

    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        """
        Add user_profile to context.

        Parameters:
        kwargs (dict): Additional keyword arguments from Django.
        """

        context = super().get_context_data(**kwargs)
        return self.add_user_profile_context(context)


class PostDetailView(UserProfileContextMixin, DetailView):
    """Display one Post record and its related content."""

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        """
        Add post owner and user_profile into context.

        Parameters:
        kwargs (dict): Additional keyword arguments from Django.
        """

        context = super().get_context_data(**kwargs)
        context["profile"] = self.object.profile
        return self.add_user_profile_context(context)


class CreatePostView(MiniInstaLoginRequiredMixin, CreateView):
    """Display and process the form used to create a Post and Photos."""

    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def dispatch(self, request, *args, **kwargs):
        """
        Ensure request.user has an associated Profile.

        Parameters:
        request (HttpRequest): The current request object.
        args (tuple): Additional positional arguments from Django.
        kwargs (dict): Additional keyword arguments from Django.
        """

        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        self.profile = Profile.objects.filter(user=request.user).order_by("id").first()
        if self.profile is None:
            return redirect("create_profile")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Add the target and user profiles to template context.

        Parameters:
        kwargs (dict): Additional keyword arguments from Django.
        """

        context = super().get_context_data(**kwargs)
        context["profile"] = self.profile
        context["user_profile"] = self.profile
        return context

    def form_valid(self, form):
        """
        Attach the Profile, save the Post, and create Photo records.

        Parameters:
        form (CreatePostForm): The validated form instance.
        """

        form.instance.profile = self.profile
        response = super().form_valid(form)

        files = self.request.FILES.getlist("files")
        for image_file in files:
            Photo.objects.create(post=self.object, image_file=image_file)

        return response

    def get_success_url(self):
        """
        Return the redirect URL after a successful create.

        Parameters:
        self (CreatePostView): The current view instance.
        """

        return reverse("show_post", kwargs={"pk": self.object.pk})


class UpdateProfileView(OwnedProfileRequiredMixin, UpdateView):
    """Display and process the form used to update request.user's Profile."""

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"
    context_object_name = "profile"

    def dispatch(self, request, *args, **kwargs):
        """
        Redirect to profile creation when request.user has no Profile.

        Parameters:
        request (HttpRequest): The current request object.
        args (tuple): Additional positional arguments from Django.
        kwargs (dict): Additional keyword arguments from Django.
        """

        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not Profile.objects.filter(user=request.user).exists():
            return redirect("create_profile")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """
        Return request.user's Profile.

        Parameters:
        self (UpdateProfileView): The current view instance.
        queryset (QuerySet): Optional queryset parameter from Django.
        """

        return Profile.objects.filter(user=self.request.user).order_by("id").first()

    def get_context_data(self, **kwargs):
        """
        Add user_profile to context.

        Parameters:
        kwargs (dict): Additional keyword arguments from Django.
        """

        context = super().get_context_data(**kwargs)
        return self.add_user_profile_context(context)


class DeletePostView(OwnedPostRequiredMixin, DeleteView):
    """Display and process the confirmation form for deleting a Post."""

    model = Post
    template_name = "mini_insta/delete_post_form.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        """
        Add the post, post owner profile, and user_profile to context.

        Parameters:
        kwargs (dict): Additional keyword arguments from Django.
        """

        context = super().get_context_data(**kwargs)
        context["post"] = self.object
        context["profile"] = self.object.profile
        return self.add_user_profile_context(context)

    def get_success_url(self):
        """
        Return the post owner's Profile page after deleting.

        Parameters:
        self (DeletePostView): The current view instance.
        """

        return reverse("show_profile", kwargs={"pk": self.object.profile.pk})


class UpdatePostView(OwnedPostRequiredMixin, UpdateView):
    """Display and process the form used to update a Post caption."""

    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        """
        Add the post owner profile and user_profile to context.

        Parameters:
        kwargs (dict): Additional keyword arguments from Django.
        """

        context = super().get_context_data(**kwargs)
        context["profile"] = self.object.profile
        return self.add_user_profile_context(context)


class PostFeedListView(MiniInstaLoginRequiredMixin, ListView):
    """Display the feed of posts for request.user's Profile."""

    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        """
        Resolve request.user's Profile for all handler methods.

        Parameters:
        request (HttpRequest): The current request object.
        args (tuple): Additional positional arguments from Django.
        kwargs (dict): Additional keyword arguments from Django.
        """

        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        self.profile = Profile.objects.filter(user=request.user).order_by("id").first()
        if self.profile is None:
            return redirect("create_profile")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        Return feed posts for request.user's Profile.

        Parameters:
        self (PostFeedListView): The current view instance.
        """

        return self.profile.get_post_feed()

    def get_context_data(self, **kwargs):
        """
        Add profile and user_profile to context.

        Parameters:
        kwargs (dict): Additional keyword arguments from Django.
        """

        context = super().get_context_data(**kwargs)
        context["profile"] = self.profile
        context["user_profile"] = self.profile
        return context


class SearchView(MiniInstaLoginRequiredMixin, ListView):
    """Display the search form or matching Profile and Post results."""

    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        """
        Render search form when query is absent.

        Parameters:
        request (HttpRequest): The current request object.
        args (tuple): Additional positional arguments from Django.
        kwargs (dict): Additional keyword arguments from Django.
        """

        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        self.profile = Profile.objects.filter(user=request.user).order_by("id").first()
        if self.profile is None:
            return redirect("create_profile")
        if "query" not in self.request.GET:
            return render(
                request,
                "mini_insta/search.html",
                {"profile": self.profile, "user_profile": self.profile},
            )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        Return Posts whose captions contain the submitted query text.

        Parameters:
        self (SearchView): The current view instance.
        """

        query = self.request.GET.get("query", "").strip()
        if not query:
            return Post.objects.none()
        return Post.objects.filter(caption__icontains=query).order_by("-timestamp")

    def get_context_data(self, **kwargs):
        """
        Add profile, query, posts, profiles, and user_profile to context.

        Parameters:
        kwargs (dict): Additional keyword arguments from Django.
        """

        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query", "").strip()
        context["profile"] = self.profile
        context["user_profile"] = self.profile
        context["query"] = query
        context["posts"] = self.get_queryset()
        context["profiles"] = Profile.objects.filter(
            Q(username__icontains=query)
            | Q(display_name__icontains=query)
            | Q(bio_text__icontains=query)
        ).order_by("display_name")
        return context


class CreateProfileView(CreateView):
    """Display and process registration + profile creation forms."""

    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"

    def get_context_data(self, **kwargs):
        """
        Add UserCreationForm to context for the registration fields.

        Parameters:
        kwargs (dict): Additional keyword arguments from Django.
        """

        context = super().get_context_data(**kwargs)
        context["user_creation_form"] = UserCreationForm()
        if self.request.user.is_authenticated:
            context["user_profile"] = Profile.objects.filter(
                user=self.request.user
            ).order_by("id").first()
        return context

    def form_valid(self, form):
        """
        Save User, log them in, attach user to Profile, and save Profile.

        Parameters:
        form (CreateProfileForm): The validated model form instance.
        """

        user_creation_form = UserCreationForm(self.request.POST)
        if not user_creation_form.is_valid():
            return self.form_invalid(form)

        user = user_creation_form.save()
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
        form.instance.user = user
        form.instance.join_date = date.today()
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Re-render both forms when either one fails validation.

        Parameters:
        form (CreateProfileForm): The invalid profile model form instance.
        """

        context = self.get_context_data(form=form)
        context["user_creation_form"] = UserCreationForm(self.request.POST)
        return self.render_to_response(context)

    def get_success_url(self):
        """
        Return URL for the newly created Profile.

        Parameters:
        self (CreateProfileView): The current view instance.
        """

        return reverse("show_profile", kwargs={"pk": self.object.pk})


class LogoutConfirmationView(UserProfileContextMixin, TemplateView):
    """Display a custom post-logout confirmation page."""

    template_name = "mini_insta/logged_out.html"

    def get_context_data(self, **kwargs):
        """
        Add user_profile to context.

        Parameters:
        kwargs (dict): Additional keyword arguments from Django.
        """

        context = super().get_context_data(**kwargs)
        return self.add_user_profile_context(context)


class FollowProfileView(MiniInstaLoginRequiredMixin, View):
    """Create a Follow where request.user follows the profile in URL pk."""

    def post(self, request, *args, **kwargs):
        """
        Create Follow record if the relationship is allowed.

        Parameters:
        request (HttpRequest): The current request object.
        args (tuple): Additional positional arguments from Django.
        kwargs (dict): Additional keyword arguments from Django.
        """

        target_profile = get_object_or_404(Profile, pk=self.kwargs["pk"])
        user_profile = get_object_or_404(Profile, user=request.user)
        if user_profile != target_profile:
            Follow.objects.get_or_create(
                profile=target_profile,
                follower_profile=user_profile,
            )
        return redirect("show_profile", pk=target_profile.pk)


class DeleteFollowProfileView(MiniInstaLoginRequiredMixin, View):
    """Delete a Follow where request.user unfollows the profile in URL pk."""

    def post(self, request, *args, **kwargs):
        """
        Delete Follow record if present.

        Parameters:
        request (HttpRequest): The current request object.
        args (tuple): Additional positional arguments from Django.
        kwargs (dict): Additional keyword arguments from Django.
        """

        target_profile = get_object_or_404(Profile, pk=self.kwargs["pk"])
        user_profile = get_object_or_404(Profile, user=request.user)
        Follow.objects.filter(
            profile=target_profile,
            follower_profile=user_profile,
        ).delete()
        return redirect("show_profile", pk=target_profile.pk)


class LikePostView(MiniInstaLoginRequiredMixin, View):
    """Create a Like where request.user likes the post in URL pk."""

    def post(self, request, *args, **kwargs):
        """
        Create Like record if the relationship is allowed.

        Parameters:
        request (HttpRequest): The current request object.
        args (tuple): Additional positional arguments from Django.
        kwargs (dict): Additional keyword arguments from Django.
        """

        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        user_profile = get_object_or_404(Profile, user=request.user)
        if post.profile != user_profile:
            Like.objects.get_or_create(post=post, profile=user_profile)
        return redirect("show_post", pk=post.pk)


class DeleteLikePostView(MiniInstaLoginRequiredMixin, View):
    """Delete a Like where request.user unlikes the post in URL pk."""

    def post(self, request, *args, **kwargs):
        """
        Delete Like record if present.

        Parameters:
        request (HttpRequest): The current request object.
        args (tuple): Additional positional arguments from Django.
        kwargs (dict): Additional keyword arguments from Django.
        """

        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        user_profile = get_object_or_404(Profile, user=request.user)
        Like.objects.filter(post=post, profile=user_profile).delete()
        return redirect("show_post", pk=post.pk)
