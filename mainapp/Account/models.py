from typing import Type

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.gis.db import models
from utils.logger import err_logger, logger  # noqa
from django.db.models.signals import post_save
from django.dispatch import receiver

from .validators import validate_phone


class UserManager(BaseUserManager):
    def create_user(
        self, username: str, password: str = None, is_active=True,
        is_staff=False, is_admin=False
    ) -> Type["User"]:
        """Create a user with the given username and password

        :param username: The username of the user
        :type username: str
        :param password: The password of the user, defaults to None
        :type password: str, optional
        :param is_active: value for user being active, defaults to True
        :type is_active: bool, optional
        :param is_staff: value for user being a staff, defaults to False
        :type is_staff: bool, optional
        :param is_admin: value for user being an admin, defaults to False
        :type is_admin: bool, optional
        :raises ValueError: If password is not provided
        :return: The created user
        :rtype: Type["User"]
        """
        if not password:
            raise ValueError("Password is required")

        user: User = self.model(
            username=username,
            active=is_active,
            staff=is_staff,
            admin=is_admin
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, username: str, password: str):
        """Create a staff user

        :param password: staff's password, defaults to None
        :type password: str, optional
        :return: The created staff user
        :rtype: Type["User"]
        """
        user = self.create_user(username, password=password, is_staff=True)
        return user

    def create_superuser(self, username: str, password: str):
        """Create a superuser

        :param password: admin's password, defaults to None
        :type password: str, optional
        :return: The created superuser
        :rtype: Type["User"]
        """
        user = self.create_user(
            username, password=password, is_staff=True, is_admin=True
        )
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)

    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'

    objects = UserManager()

    def has_perm(self, perm, obj=None):  # pragma: no cover
        return True

    def has_module_perms(self, app_label):  # pragma: no cover
        return True

    def __str__(self) -> str:
        return self.name

    @property
    def name(self) -> str:
        """Get the name of the user or the username if name is not set

        :return: The name of the user
        :rtype: str
        """
        return self.profile.name or self.username

    @property
    def is_active(self) -> bool:
        """Return True if the user is active."""
        return self.active

    @property
    def is_staff(self) -> bool:
        """Return True if the user is staff."""
        return self.staff

    @property
    def is_admin(self) -> bool:
        """Return True if the user is admin."""
        return self.admin


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=30, help_text="Enter your full name")
    phone = models.CharField(
        max_length=20, validators=[validate_phone],
        help_text="Your Phone number")
    address = models.CharField(
        max_length=200, blank=True, help_text="Your home address")
    location = models.PointField(
        null=True, blank=True, help_text="Your home location")

    def __str__(self) -> str:
        return self.name

    @property
    def lat(self):
        return self.location.y

    @property
    def lng(self):
        return self.location.x


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, name=instance.username)
