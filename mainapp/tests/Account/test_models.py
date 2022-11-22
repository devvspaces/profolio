import pytest
from django.contrib.auth import get_user_model
from Account.models import AuthActivityLog
from model_bakery import baker


User = get_user_model()


@pytest.mark.django_db
class TestUserManager:
    def test_create_user(self):
        user = User.objects.create_user(
            "testuser", password="testpassword"
        )
        assert user.username == "testuser"
        assert user.check_password("testpassword")
        assert user.is_active
        assert user.is_staff is False
        assert user.is_admin is False

    def test_create_staff(self):
        user = User.objects.create_staff(
            "staff", password="testpassword")
        assert user.username == "staff"
        assert user.check_password("testpassword")
        assert user.is_active
        assert user.is_staff
        assert user.is_admin is False

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            "admin", password="testpassword")
        assert user.username == "admin"
        assert user.check_password("testpassword")
        assert user.is_active
        assert user.is_staff
        assert user.is_admin


@pytest.mark.django_db
class TestUser:
    def test_user_str(self):
        user = baker.make(User, username="testuser")
        assert str(user) == "testuser"


@pytest.mark.django_db
class TestProfile:
    def test_profile_str(self):
        user = baker.make(User, username="testuser")
        assert str(user.profile) == "testuser"

        profile = user.profile
        profile.name = "Test User"
        assert str(profile) == "Test User"


@pytest.mark.django_db
class TestAuthActivityLog:
    def test_auth_activity_log_str(self):
        user = baker.make(User, username="testuser")
        auth_activity_log = baker.make(
            AuthActivityLog, user=user
        )
        assert str(auth_activity_log) == "testuser"
