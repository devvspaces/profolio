from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import (CreateView, DetailView, TemplateView,
                                  UpdateView)

from .forms import ProfileUpdateForm, UserRegisterForm
from .models import Profile

User = get_user_model()


class ViewMixin:
    """
    Mixin for adding common attributes to views.
    Getting the title attribute and adds it to the context
    """
    title: str = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.title:
            raise NotImplementedError("Title not set")

        context["title"] = self.title
        context["BRAND_NAME"] = settings.BRAND_NAME
        return context


class RegisterView(CreateView, ViewMixin):
    model = User
    template_name = "Account/register.html"
    form_class = UserRegisterForm
    title = "Register"

    def get_success_url(self) -> str:
        """
        Redirect to login page after successful registration

        :return: URL
        :rtype: str
        """
        return reverse("account:login")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Account created successfully")
        return super().form_valid(form)


class HomeView(LoginRequiredMixin, TemplateView, ViewMixin):
    template_name = "Account/home.html"
    title = "Home"


class ProfileView(LoginRequiredMixin, DetailView, ViewMixin):
    template_name = "Account/profile/detail.html"
    model = Profile
    context_object_name = "profile"
    title = "Your Profile"

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView, ViewMixin):
    template_name = "Account/profile/update.html"
    model = Profile
    form_class = ProfileUpdateForm
    context_object_name = "profile"
    title = "Update Profile"

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse("account:profile")
