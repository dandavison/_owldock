from typing import List

from django.http import HttpRequest, JsonResponse
from django_tools.middlewares.ThreadLocal import get_current_request

_ERROR_MESSAGES_ATTR_NAME = "_error_messages_to_be_sent_with_response"
_NON_ERROR_MESSAGES_ATTR_NAME = "_non_error_messages_to_be_sent_with_response"


def add_error(error: str) -> None:
    request = get_current_request()
    _extend(request, _ERROR_MESSAGES_ATTR_NAME, [error])


def add_message(message: str) -> None:
    request = get_current_request()
    _extend(request, _NON_ERROR_MESSAGES_ATTR_NAME, [message])


def _extend(request: HttpRequest, attr_name: str, messages: List[str]) -> None:
    if not hasattr(request, attr_name):
        setattr(request, attr_name, [])
    getattr(request, attr_name).extend(messages)


class OwldockJsonResponse(JsonResponse):
    """
    All owldock JSON responses must have the format defined here.
    """

    def __init__(self, data, errors=None, messages=None, **kwargs):
        request = get_current_request()
        _extend(request, _ERROR_MESSAGES_ATTR_NAME, errors or [])
        _extend(request, _NON_ERROR_MESSAGES_ATTR_NAME, messages or [])

        errors = getattr(request, _ERROR_MESSAGES_ATTR_NAME)
        messages = getattr(request, _NON_ERROR_MESSAGES_ATTR_NAME)

        payload = {
            "data": data,
            "errors": errors,
            "messages": messages,
        }
        super().__init__(payload, **kwargs)
