from typing import List

from django.http import JsonResponse
from django_tools.middlewares.ThreadLocal import _thread_locals

_ERROR_MESSAGES_ATTR_NAME = "_error_messages_to_be_sent_with_response"
_NON_ERROR_MESSAGES_ATTR_NAME = "_non_error_messages_to_be_sent_with_response"


def add_error(error: str) -> None:
    _extend(_ERROR_MESSAGES_ATTR_NAME, [error])


def add_message(message: str) -> None:
    _extend(_NON_ERROR_MESSAGES_ATTR_NAME, [message])


def _extend(attr_name: str, messages: List[str]) -> None:
    if not hasattr(_thread_locals, attr_name):
        setattr(_thread_locals, attr_name, [])
    getattr(_thread_locals, attr_name).extend(messages)


class OwldockJsonResponse(JsonResponse):
    """
    All owldock JSON responses must have the format defined here.
    """

    def __init__(self, data, errors=None, messages=None, **kwargs):
        _extend(_ERROR_MESSAGES_ATTR_NAME, errors or [])
        _extend(_NON_ERROR_MESSAGES_ATTR_NAME, messages or [])

        errors = getattr(_thread_locals, _ERROR_MESSAGES_ATTR_NAME)
        messages = getattr(_thread_locals, _NON_ERROR_MESSAGES_ATTR_NAME)

        payload = {
            "data": data,
            "errors": errors,
            "messages": messages,
        }
        super().__init__(payload, **kwargs)
