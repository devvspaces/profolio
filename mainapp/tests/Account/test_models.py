import pytest
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import fromstr
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

    def test_password_required(self):
        with pytest.raises(ValueError):
            User.objects.create_user("testuser")

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

    def test_lat(self):
        user = baker.make(User, username="testuser")
        user.profile.location = fromstr("POINT(10.2 12.4)", srid=4326)
        user.profile.save()
        assert user.profile.lat == 12.4

    def test_lon(self):
        user = baker.make(User, username="testuser")
        user.profile.location = fromstr("POINT(10.2 12.4)", srid=4326)
        user.profile.save()
        assert user.profile.lng == 10.2
