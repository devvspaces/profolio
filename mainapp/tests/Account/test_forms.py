from Account.forms import UserRegisterForm
import pytest
from django.contrib.gis.geos import fromstr


@pytest.mark.django_db
class TestUserRegisterForm:

    form_data = {
        "username": "testuser",
        "password": "testpassword",
        "confirm_password": "testpassword",
        "name": "Test User",
        "phone": "1234567890",
        "address": "Test Address",
        "location": "12.345678,98.765432",
    }

    def test_user_register_form(self):
        form_data = self.form_data
        form = UserRegisterForm(data=form_data)
        assert form.is_valid()

        user = form.save(False)
        assert user.check_password(form_data["password"])

        with pytest.raises(Exception):
            user.profile

        user = form.save()
        assert user.profile.id
        assert user.profile.name == form_data["name"]
        assert user.profile.phone == form_data["phone"]
        assert user.profile.address == form_data["address"]
        assert user.profile.location == fromstr(
            "POINT(98.765432 12.345678)", srid=4326)

    @pytest.mark.parametrize("location", [
        "92.345678, 98.765432",
        "12.345678, 198.765432",
        "12.345678, 98.765432, 12.345678, 98.765432",
    ])
    def test_form_location_validation_error(self, location):
        form_data = self.form_data
        form_data["location"] = location
        form = UserRegisterForm(data=form_data)
        assert not form.is_valid()

    def test_form_password_validation_error(self):
        form_data = self.form_data
        form_data["password"] = "123"
        form = UserRegisterForm(data=form_data)
        assert not form.is_valid()

    def test_form_confirm_password_validation_error(self):
        form_data = self.form_data
        form_data["confirm_password"] = "123"
        form = UserRegisterForm(data=form_data)
        assert not form.is_valid()
