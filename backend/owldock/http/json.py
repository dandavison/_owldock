from typing import List

from django.http import JsonResponse
from django_tools.middlewares.ThreadLocal import get_current_request

_ERROR_MESSAGES_ATTR_NAME = "_error_messages_to_be_sent_with_response"
_NON_ERROR_MESSAGES_ATTR_NAME = "_non_error_messages_to_be_sent_with_response"


def add_error(error: str) -> None:
    _extend_messages(_ERROR_MESSAGES_ATTR_NAME, [error])


def add_message(message: str) -> None:
    _extend_messages(_NON_ERROR_MESSAGES_ATTR_NAME, [message])


def _extend_messages(attr_name: str, messages: List[str]) -> None:
    request = get_current_request()
    if not request:
        # During tests etc
        return
    if not hasattr(request, attr_name):
        setattr(request, attr_name, [])
    getattr(request, attr_name).extend(messages)


def _get_messages(attr_name: str) -> List[str]:
    request = get_current_request()
    return getattr(request, attr_name, [])


class OwldockJsonResponse(JsonResponse):
    """
    All owldock JSON responses must have the format defined here.
    """

    def __init__(self, data, errors=None, messages=None, **kwargs):
        _extend_messages(_ERROR_MESSAGES_ATTR_NAME, errors or [])
        _extend_messages(_NON_ERROR_MESSAGES_ATTR_NAME, messages or [])

        errors = _get_messages(_ERROR_MESSAGES_ATTR_NAME)
        messages = _get_messages(_NON_ERROR_MESSAGES_ATTR_NAME)

        payload = {
            "data": data,
            "errors": errors,
            "messages": messages,
        }
        super().__init__(payload, **kwargs)
