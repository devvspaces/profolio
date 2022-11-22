from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import (
    HomeView, ProfileView, ProfileUpdateView, RegisterView
)

app_name = "account"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),

    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(
        template_name="Account/login.html"
    ), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("profile/", ProfileView.as_view(), name="profile"),
    path(
        "profile/update/",
        ProfileUpdateView.as_view(), name="profile-update"),
]
