"""
Author: Alvin Zhu
Email: alvinz@bu.edu
Description: Class-based views for listing, viewing, and creating mini_insta data.
"""

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView

from .forms import CreatePostForm
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


class PostDetailView(DetailView):
    """Display one Post record and its related photos."""

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
    """Display and process the form used to create a Post and first Photo."""

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
        Attach foreign keys before saving Post and create first Photo.

        Parameters:
        form (CreatePostForm): The validated form instance.
        """

        profile = get_object_or_404(Profile, pk=self.kwargs["pk"])
        form.instance.profile = profile
        response = super().form_valid(form)

        image_url = self.request.POST.get("image_url", "").strip()
        if image_url:
            Photo.objects.create(post=self.object, image_url=image_url)

        return response

    def get_success_url(self):
        """
        Return the redirect URL after a successful create.

        Parameters:
        self (CreatePostView): The current view instance.
        """

        return reverse("show_post", kwargs={"pk": self.object.pk})
