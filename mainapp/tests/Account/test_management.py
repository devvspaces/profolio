from io import StringIO
from django.core.management import call_command
import pytest
import os


@pytest.mark.django_db
class TestInitializeProject:
    @pytest.mark.usefixtures("use_dummy_base_path")
    def test_command_output(self, settings):
        out = StringIO()
        call_command('initialize', stdout=out)

        # If logs directory is created
        assert os.path.exists(settings.BASE_DIR / "logs")

        # If .env file is created
        assert os.path.exists(settings.BASE_DIR / ".env")

        assert 'Project initialized successfully\n' == out.getvalue()

    def test_error(self, mocker):
        # make sure create_logs raises an error
        mocker.patch(
            'Account.management.commands.initialize.create_logs',
            side_effect=Exception('Error')
        )
        out = StringIO()
        with pytest.raises(Exception):
            call_command('initialize', stdout=out)
