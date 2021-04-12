import logging
from typing import Callable

from django.http import HttpRequest
from django.http import HttpResponse

from client.models import Client
from app.models import Provider


logger = logging.getLogger(__file__)

Middleware = Callable[[HttpRequest], HttpResponse]


def set_user_data_cookies(get_response: Middleware) -> Middleware:
    def middleware(request: HttpRequest) -> HttpResponse:
        response = get_response(request)
        if request.user.is_authenticated:
            _set_user_attribute_cookie("first_name", request.user, response)
            _set_user_attribute_cookie("username", request.user, response)
            logger.info(
                "request.user: username=%s, email=%s, id=%s"
                % (
                    request.user.username,
                    getattr(request.user, "email", "<no email>"),
                    getattr(request.user, "id", "<no id>"),
                ),
            )
            if not (
                _set_client_cookies(request.user, response)
                or _set_provider_cookies(request.user, response)
            ):
                logger.error(
                    "request %s %s is neither client nor provider",
                    request,
                    request.user,
                )

        return response

    return middleware


def _set_user_attribute_cookie(attr: str, user, response: HttpResponse) -> None:
    try:
        value = getattr(user, attr)
    except AttributeError:
        pass
    else:
        if value:
            response.set_cookie(attr, value)


def _set_client_cookies(user, response: HttpResponse) -> bool:
    try:
        client = Client.objects.get(clientcontact__user_id=user.uuid)
    except Client.DoesNotExist:
        return False
    else:
        response.set_cookie("logo_url", client.logo_url)
        response.set_cookie("role", "client-contact")
        return True


def _set_provider_cookies(user, response: HttpResponse) -> bool:
    try:
        provider = Provider.objects.get(providercontact__user_id=user.uuid)
    except Provider.DoesNotExist:
        return False
    else:
        response.set_cookie("logo_url", provider.logo_url)
        response.set_cookie("role", "provider-contact")
        return True
