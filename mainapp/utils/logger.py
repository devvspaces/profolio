import logging

from django.http import HttpRequest
from django.utils.encoding import force_text
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, CHANGE
from datetime import datetime

# Create the logger and set the logging level
logger = logging.getLogger('basic')
err_logger = logging.getLogger('basic.error')


LOGIN = 1
LOGOUT = 2

ACTION_CHOICES = {
    LOGIN: 'logged in',
    LOGOUT: 'logged out'
}


def get_change_message(action: int, username: str):
    """Create the message to log

    :param action: action performed
    :type action: int
    """

    action_text = ACTION_CHOICES[action]

    date_now = datetime.now()
    date = date_now.strftime("%Y-%m-%d %H:%M%p").lower()

    return f"{username} {action_text} at {date}"


def log_user_action(request: HttpRequest, action: int) -> LogEntry:
    """Log user login and logout activity

    :param request: http request
    :type request: HttpRequest
    :param action: action performed
    :type action: int
    :return: Log entry created
    :rtype: LogEntry
    """

    object = request.user

    return LogEntry.objects.log_action(
        user_id=object.id,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.id,
        object_repr=force_text(object),
        action_flag=CHANGE,
        change_message=get_change_message(action, object.username)
    )
