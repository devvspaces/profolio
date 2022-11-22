import os

import pytest
from Account.management.commands.initialize import (create_env, create_logs,
                                                    create_strong_secret_key)


def test_create_strong_secret_key():
    key = create_strong_secret_key()
    assert len(key) == 50


@pytest.mark.usefixtures("use_dummy_base_path")
def test_create_logs(settings):
    create_logs()
    assert os.path.exists(settings.BASE_DIR / "logs")


@pytest.mark.usefixtures("use_dummy_base_path")
def test_create_env(settings):
    create_env()
    assert os.path.exists(settings.BASE_DIR / ".env")

    with open(settings.BASE_DIR / ".env", "r") as env_file:
        text = env_file.read()
        assert text.startswith("SECRET_KEY=")
