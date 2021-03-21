from typing import Callable

from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.http import HttpResponse

Middleware = Callable[[HttpRequest], HttpResponse]
User = get_user_model()


def set_user_data_cookies(get_response: Middleware) -> Middleware:
    def middleware(request: HttpRequest) -> HttpResponse:
        response = get_response(request)
        if request.user:
            _set_user_attribute_cookie("first_name", request.user, response)
            _set_user_attribute_cookie("username", request.user, response)
        return response

    return middleware


def _set_user_attribute_cookie(attr: str, user: User, response: HttpResponse) -> None:
    # Note: mypy reports the type of User to be Union[AbstractBaseUser, AnonymousUser],
    # and that this type does not have, for example 'user_name'.
    try:
        value = getattr(user, attr)
    except AttributeError:
        pass
    else:
        if value:
            response.set_cookie(attr, value)
