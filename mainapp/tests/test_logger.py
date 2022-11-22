from datetime import datetime

import pytest
from django.contrib.auth import get_user_model
from django.test.client import RequestFactory
from model_bakery import baker
from utils.logger import LOGIN, get_change_message, log_user_action

User = get_user_model()


def test_get_change_message(monkeypatch):

    date = datetime(2014, 2, 12, 7, 45)

    class mydatetime:
        @classmethod
        def now(cls):
            return date

    monkeypatch.setattr('utils.logger.datetime', mydatetime)
    message = get_change_message(LOGIN, "test")
    expected = 'test logged in at 2014-02-12 07:45am'
    assert message == expected


@pytest.mark.django_db
def test_log_user_action(mocker):
    mocker.patch(
        'utils.logger.get_change_message',
        return_value="test"
    )

    user = baker.make(User, username="testuser")

    request = RequestFactory().get('/')
    request.user = user

    log = log_user_action(request, LOGIN)

    assert log.id
    assert log.user == user
