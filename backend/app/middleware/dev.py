import logging
import os
import sys
from typing import Callable

import clint
from django.conf import settings
from django.contrib.auth import login, get_user_model

from django.http import HttpRequest
from django.http import HttpResponse

logger = logging.getLogger(__file__)


Middleware = Callable[[HttpRequest], HttpResponse]


def red(s: str):
    return clint.textui.colored.red(s, always=True, bold=True)


def blue(s: str):
    return clint.textui.colored.blue(s, always=True, bold=True)


def auto_authenticate_according_to_requested_endpoint(
    get_response: Middleware,
) -> Middleware:
    def middleware(request: HttpRequest) -> HttpResponse:
        print(
            blue(
                f"auto_authenticate_according_to_requested_endpoint: "
                f"{request} {request.user}"
            )
        )
        if not request.user.is_authenticated:
            username = request.GET.get("username")
            if username:
                user_model = get_user_model()
                try:
                    user = user_model.objects.get(username=username)
                except user_model.DoesNotExist:
                    logger.warning(f"No user exists for username: {username}")
                else:
                    login(request, user)
                    print(
                        red(
                            f"UI dev mode: request {request} insecurely authenticated as {user}"
                        )
                    )
        return get_response(request)

    return middleware


def assert_this_is_a_development_environment():
    assert settings.DEBUG
    assert sys.platform == "darwin"
    assert os.environ["USER"] == "dan"


assert_this_is_a_development_environment()
