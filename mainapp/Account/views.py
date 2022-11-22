import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.serializers import serialize
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import (CreateView, DetailView, TemplateView,
                                  UpdateView)
from utils.logger import LOGIN, LOGOUT, log_user_action

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
        page_name = slugify(self.title).lower().replace('-', '_')
        context[page_name] = 'active'
        return context


class UserLoginView(ViewMixin, LoginView):
    """
    Login view
    """
    template_name: str = "Account/login.html"
    title: str = "Login"

    def form_valid(self, form):
        """
        Log user login action
        """
        res = super().form_valid(form)
        log_user_action(self.request, LOGIN)
        return res


class UserLogoutView(LogoutView):
    """
    Login view
    """
    template_name: str = "Account/login.html"
    title: str = "Login"

    def dispatch(self, request, *args, **kwargs):
        """
        Log user logout action
        """
        if request.user.is_authenticated:
            log_user_action(request, LOGOUT)
        return super().dispatch(request, *args, **kwargs)


class RegisterView(ViewMixin, CreateView):
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


class HomeView(ViewMixin, LoginRequiredMixin, TemplateView):
    template_name = "Account/home.html"
    title = "Home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get users that have location
        profiles = Profile.objects.exclude(location__isnull=True)

        # Serialize the data to geojson
        context["locations"] = json.loads(serialize('geojson', profiles))

        return context


class ProfileView(ViewMixin, LoginRequiredMixin, DetailView):
    template_name = "Account/profile/detail.html"
    model = Profile
    context_object_name = "profile"
    title = "Your Profile"

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProfileUpdateView(ViewMixin, LoginRequiredMixin, UpdateView):
    template_name = "Account/profile/update.html"
    model = Profile
    form_class = ProfileUpdateForm
    context_object_name = "profile"
    title = "Update Profile"

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse("account:profile")
