import pytest
from django.urls import reverse
from django.test.client import Client
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestRegisterView:
    url = reverse("account:register")

    def test_get(self, client):
        response = client.get(self.url)
        assert response.status_code == 200

    def test_post(self, client: Client):
        response = client.post(self.url, {
            "username": "testuser",
            "password": "testpassword",
            "confirm_password": "testpassword",
            "name": "Test User",
            "phone": "1234567890",
            "address": "Test Address",
            "location": "12.345678,98.765432",
        })
        assert response.status_code == 302
        assert response.url == reverse("account:login")

    def test_post_invalid(self, client: Client):
        response = client.post(self.url, {
            "username": "testuser",
            "password": "testpassword",
            "confirm_password": "testpassword",
            "name": "Test User",
            "phone": "1234567890",
            "address": "Test Address",
            "location": "92.345678, 98.765432",
        })
        assert response.status_code == 200
        assert response.context["form"].errors["location"]


@pytest.mark.django_db
class TestLoginView:
    url = reverse("account:login")

    def test_get(self, client):
        response = client.get(self.url)
        assert response.status_code == 200

    def test_post(self, client: Client):
        User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        response = client.post(self.url, {
            "username": "testuser",
            "password": "testpassword",
        })
        assert response.status_code == 302
        assert response.url == reverse("account:home")

    def test_post_invalid(self, client: Client):
        response = client.post(self.url, {
            "username": "testuser",
            "password": "testpassword",
        })
        assert response.status_code == 200
        assert response.context["form"].errors["__all__"]


@pytest.mark.django_db
class TestLogoutView:
    url = reverse("account:logout")

    def test_get(self, client):
        response = client.get(self.url)
        assert response.status_code == 302
        assert response.url == reverse("account:login")

    def test_post(self, client):
        response = client.post(self.url)
        assert response.status_code == 302
        assert response.url == reverse("account:login")


@pytest.mark.django_db
class TestProfileView:
    url = reverse("account:profile")

    def test_get(self, client):
        response = client.get(self.url)
        assert response.status_code == 302
        assert response.url == reverse("account:login") + "?next=" + self.url

    def test_get_authenticated(self, client):
        User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        client.login(username="testuser", password="testpassword")
        response = client.get(self.url)
        assert response.status_code == 200
        assert response.context["profile"].user.username == "testuser"


@pytest.mark.django_db
class TestProfileUpdate:
    url = reverse("account:profile-update")

    def test_get(self, client):
        response = client.get(self.url)
        assert response.status_code == 302
        assert response.url == reverse("account:login") + "?next=" + self.url

    def test_get_authenticated(self, client):
        User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        client.login(username="testuser", password="testpassword")
        response = client.get(self.url)
        assert response.status_code == 200
        assert response.context["profile"].user.username == "testuser"

    def test_post(self, client):
        User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        client.login(username="testuser", password="testpassword")
        response = client.post(self.url, {
            "name": "Test User",
            "phone": "1234567890",
            "address": "Test Address",
            "location": "12.345678,98.765432",
        })
        assert response.status_code == 302
        assert response.url == reverse("account:profile")

    def test_post_invalid(self, client):
        User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        client.login(username="testuser", password="testpassword")
        response = client.post(self.url, {
            "name": "Test User",
            "phone": "1234567890",
            "address": "Test Address",
            "location": "92.345678,98.765432",
        })
        assert response.status_code == 200
        assert response.context["form"].errors["location"]
