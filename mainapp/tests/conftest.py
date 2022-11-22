
import pytest


@pytest.fixture
def use_dummy_base_path(settings, tmp_path):
    settings.BASE_DIR = tmp_path
