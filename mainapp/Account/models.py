from typing import TypeVar
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from utils.logger import err_logger, logger  # noqa


T = TypeVar('T', bound=AbstractBaseUser)


class UserManager(BaseUserManager):
    def create_base_user(
        self, is_active=True,
        is_staff=False, is_admin=False
    ) -> T:
        user: User = self.model()
        user.active = is_active
        user.admin = is_admin
        user.staff = is_staff
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user(
        self, , password=None, is_active=True,
        is_staff=False, is_admin=False
    ) -> T:
        user = self.create_base_user(, is_active, is_staff, is_admin)
        if not password:
            raise ValueError("User must provide a password")
        user.set_password(password)
        user.save()
        return user

    def create_staff(self, , password=None) -> T:
        user = self.create_user(=, password=password, is_staff=True)
        return user

    def create_superuser(self, , password=None) -> T:
        user = self.create_user(
            =, password=password, is_staff=True, is_admin=True)
        return user

    def get_staffs(self):
        return self.filter(staff=True)

    def get_admins(self):
        return self.filter(admin=True)


class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length=14, blank=True)
    home_address = models.CharField(max_length=255, blank=True)

    # Admin fields
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "username"

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def username(self) -> str:
        return self.profile.username

    @property
    def get_name(self) -> str:
        """Return the x part of an  e.g [x]@gmail.com"""
        return self..split('@')[0]

    def __str__(self) -> str:
        return self.

    def _user(self, subject, message):
        val = send_(subject=subject, message=message, =self.)
        return True if val else False

    @property
    def first_name(self) -> str:
        return self.profile.first_name

    @property
    def last_name(self) -> str:
        return self.profile.last_name

    @property
    def is_active(self) -> bool:
        return self.active

    @property
    def is_staff(self) -> bool:
        return self.staff

    @property
    def is_admin(self) -> bool:
        return self.admin

    def save(self, *args, **kwargs) -> None:
        created = not self.id
        data = super().save(*args, **kwargs)
        self.refresh_from_db()

        try:
            if created:
                Profile.objects.create(
                    user=self,
                    username=get_name_from_(self.get_name))
        except Exception as e:
            self.delete()
            raise e

        return data


class Profile(models.Model):
    ACCOUNT_TYPES = [
        ('logistics', 'Logistics',),
        ('transportation', 'Transportation',),
        ('driver', 'Driver',),
    ]

    account_type = models.CharField(
        choices=ACCOUNT_TYPES, max_length=30, blank=True)
    approved = models.BooleanField(default=False)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(
        max_length=60, unique=True, validators=[validate_special_char])
    created = models.DateTimeField(auto_now=True)

    first_name = models.CharField(
        max_length=30, validators=[validate_special_char])
    last_name = models.CharField(
        max_length=30, validators=[validate_special_char])

    phone = models.CharField(max_length=20, validators=[validate_phone])
    image = models.ImageField(
        upload_to='accounts/profiles', null=True, blank=True)

    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=60, blank=True)
    state = models.CharField(max_length=60, blank=True)
    zip = models.CharField(max_length=6, blank=True)

    about = models.TextField(max_length=2500, blank=True)

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.get_fullname

    @property
    def get_fullname(self) -> str:
        return self.fullname.title()

    def get_user_name_with_id(self) -> str:
        user_name = self.first_name + self.last_name
        return f"{user_name}-{self.user.id}"


class NewsletterSubscriber(models.Model):
     = models.Field()
    created = models.DateTimeField(auto_now_add=True)

    active = models.BooleanField(default=True)

    """This is used to store reason for users
    unsubscribing from the website  newsletter"""
    reason = models.TextField(blank=True)

    def __str__(self):
        return self.


class UsedResetToken(models.Model):
    """
    Model for used tokens
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.user.profile.fullname
