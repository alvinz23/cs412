"""
Author: Alvin Zhu
Email: alvinz@bu.edu
Description: Class-based views for the mini_insta application.
"""

from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CreatePostForm, UpdatePostForm, UpdateProfileForm
from .models import Photo, Post, Profile


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


class ShowFollowersDetailView(DetailView):
    """Display the follower list for one Profile."""

    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"


class ShowFollowingDetailView(DetailView):
    """Display the following list for one Profile."""

    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"


class PostDetailView(DetailView):
    """Display one Post record and its related content."""

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        """
        Add the related Profile into context for shared navigation.

        Parameters:
        kwargs (dict): Additional keyword arguments from Django.
        """

        context = super().get_context_data(**kwargs)
        context["profile"] = self.object.profile
        return context


class CreatePostView(CreateView):
    """Display and process the form used to create a Post and Photos."""

    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self, **kwargs):
        """
        Add the target Profile to template context using URL parameter pk.

        Parameters:
        kwargs (dict): Additional keyword arguments from Django.
        """

        context = super().get_context_data(**kwargs)
        context["profile"] = get_object_or_404(Profile, pk=self.kwargs["pk"])
        return context

    def form_valid(self, form):
        """
        Attach the Profile, save the Post, and create Photo records.

        Parameters:
        form (CreatePostForm): The validated form instance.
        """

        profile = get_object_or_404(Profile, pk=self.kwargs["pk"])
        form.instance.profile = profile
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


class UpdateProfileView(UpdateView):
    """Display and process the form used to update a Profile."""

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"
    context_object_name = "profile"


class DeletePostView(DeleteView):
    """Display and process the confirmation form for deleting a Post."""

    model = Post
    template_name = "mini_insta/delete_post_form.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        """
        Add the post and profile objects required by the template.

        Parameters:
        kwargs (dict): Additional keyword arguments from Django.
        """

        context = super().get_context_data(**kwargs)
        context["post"] = self.object
        context["profile"] = self.object.profile
        return context

    def get_success_url(self):
        """
        Return the Profile page after deleting the Post.

        Parameters:
        self (DeletePostView): The current view instance.
        """

        return reverse("show_profile", kwargs={"pk": self.object.profile.pk})


class UpdatePostView(UpdateView):
    """Display and process the form used to update a Post caption."""

    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        """
        Add the related Profile for shared navigation and cancel links.

        Parameters:
        kwargs (dict): Additional keyword arguments from Django.
        """

        context = super().get_context_data(**kwargs)
        context["profile"] = self.object.profile
        return context


class PostFeedListView(ListView):
    """Display the feed of posts for one Profile."""

    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        """
        Return feed posts for the Profile identified by the URL.

        Parameters:
        self (PostFeedListView): The current view instance.
        """

        self.profile = get_object_or_404(Profile, pk=self.kwargs["pk"])
        return self.profile.get_post_feed()

    def get_context_data(self, **kwargs):
        """
        Add the Profile to template context.

        Parameters:
        kwargs (dict): Additional keyword arguments from Django.
        """

        context = super().get_context_data(**kwargs)
        context["profile"] = self.profile
        return context


class SearchView(ListView):
    """Display the search form or matching Profile and Post results."""

    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        """
        Render the search form when there is no query string.

        Parameters:
        request (HttpRequest): The current request object.
        args (tuple): Additional positional arguments from Django.
        kwargs (dict): Additional keyword arguments from Django.
        """

        self.profile = get_object_or_404(Profile, pk=self.kwargs["pk"])
        if "query" not in self.request.GET:
            return render(
                request,
                "mini_insta/search.html",
                {"profile": self.profile},
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
        Add the Profile, query, Posts, and matching Profiles to context.

        Parameters:
        kwargs (dict): Additional keyword arguments from Django.
        """

        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query", "").strip()
        context["profile"] = self.profile
        context["query"] = query
        context["posts"] = self.get_queryset()
        context["profiles"] = Profile.objects.filter(
            Q(username__icontains=query)
            | Q(display_name__icontains=query)
            | Q(bio_text__icontains=query)
        ).order_by("display_name")
        return context
