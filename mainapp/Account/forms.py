from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from .validators import validate_phone
from .models import Profile
from django.contrib.gis.geos import fromstr

User = get_user_model()


class FormMixin:
    """This is a custom validation method for location.
    Mixin class is used to avoid code duplication.
    """
    def clean_location(self):
        """
        Validate location. This is a custom validation method
        Location is a string of coordinates in the format
        "lat,lng" where lat and lng are floats

        :raises forms.ValidationError: If location is not valid
        :return: The location as a Point object
        :rtype: Point
        """

        location = self.cleaned_data.get("location")
        try:
            lat, lng = location.split(",")
            lat = float(lat)
            lng = float(lng)
        except ValueError:
            raise forms.ValidationError("Invalid location")

        if lat < -90 or lat > 90:
            raise forms.ValidationError("Invalid latitude")

        if lng < -180 or lng > 180:
            raise forms.ValidationError("Invalid longitude")

        return fromstr(f"POINT({lng} {lat})", srid=4326)


class UserRegisterForm(forms.ModelForm, FormMixin):
    """
    Form for registering a user
    """

    name = forms.CharField(max_length=100, help_text="Enter your full name")
    address = forms.CharField(
        max_length=200, help_text="Your home address")

    location = forms.CharField(help_text="Your home location")
    phone = forms.CharField(
        max_length=20, validators=[validate_phone],
        help_text="Your Phone number")

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        min_length=8,
        help_text=password_validation.password_validators_help_text_html())

    confirm_password = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput,
        help_text='Enter the same password as before, for verification.')

    class Meta:
        model = User
        fields = ["username", "password", "name",
                  "phone", "address", "location", "confirm_password"]

    def clean_password(self):
        """
        Cleaning password one to check if all validations are met
        """
        ps1 = self.cleaned_data.get("password")
        password_validation.validate_password(ps1, None)
        return ps1

    def clean_confirm_password(self):
        """
        Cleaning confirm_password to check if it matches password
        """
        ps1 = self.cleaned_data.get("password")
        ps2 = self.cleaned_data.get("confirm_password")
        if (ps1 and ps2) and (ps1 != ps2):
            raise forms.ValidationError("Passwords don't match")
        return ps2

    def save(self, commit=True):
        """
        Saving the user and profile

        :param commit: if model should be commited to db, defaults to True
        :type commit: bool, optional
        :return: The user object
        :rtype: User
        """
        user: User = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))

        if commit:
            user.save()

            # Profile is already created, update values with data in form
            profile = user.profile
            profile.name = self.cleaned_data.get("name")
            profile.phone = self.cleaned_data.get("phone")
            profile.address = self.cleaned_data.get("address")
            profile.location = self.cleaned_data.get("location")
            profile.save()

        return user


class ProfileUpdateForm(forms.ModelForm, FormMixin):
    """
    Form for updating user profile
    """

    name = forms.CharField(max_length=100, help_text="Enter your full name")
    address = forms.CharField(
        max_length=200, help_text="Your home address")

    location = forms.CharField(help_text="Your home location")
    phone = forms.CharField(
        max_length=20, validators=[validate_phone],
        help_text="Your Phone number")

    class Meta:
        model = Profile
        fields = ["name", "phone", "address", "location"]
