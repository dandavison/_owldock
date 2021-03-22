from typing import Callable, Union

from django.contrib.auth.models import (  # pylint: disable=imported-auth-user
    AnonymousUser,
    User,
)

from django.http import HttpRequest
from django.http import HttpResponse

Middleware = Callable[[HttpRequest], HttpResponse]


def set_user_data_cookies(get_response: Middleware) -> Middleware:
    def middleware(request: HttpRequest) -> HttpResponse:
        response = get_response(request)
        if request.user:
            _set_user_attribute_cookie("first_name", request.user, response)
            _set_user_attribute_cookie("username", request.user, response)
        return response

    return middleware


def _set_user_attribute_cookie(
    attr: str, user: Union[User, AnonymousUser], response: HttpResponse
) -> None:
    try:
        value = getattr(user, attr)
    except AttributeError:
        pass
    else:
        if value:
            response.set_cookie(attr, value)
