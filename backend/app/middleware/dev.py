import logging
import os
import sys
from typing import Callable, Optional

from django.conf import settings
from django.contrib.auth import login, get_user_model

from django.contrib.auth.models import User  # pylint: disable=imported-auth-user

from django.http import HttpRequest
from django.http import HttpResponse

logger = logging.getLogger(__file__)


Middleware = Callable[[HttpRequest], HttpResponse]


def assert_this_is_a_development_environment():
    from app.models import Provider

    assert settings.DEBUG
    assert sys.platform == "darwin"
    assert os.environ["USER"] == "dan"
    assert Provider.objects.filter(name="Acme").exists()
    assert Provider.objects.count() == 3


assert_this_is_a_development_environment()


def auto_authenticate_according_to_requested_endpoint(
    get_response: Middleware,
) -> Middleware:
    red = lambda s: __import__("clint").textui.colored.red(s, always=True, bold=True)
    blue = lambda s: __import__("clint").textui.colored.blue(s, always=True, bold=True)

    def middleware(request: HttpRequest) -> HttpResponse:
        print(
            blue(
                f"auto_authenticate_according_to_requested_endpoint: "
                f"{request} {request.user}"
            )
        )
        if not request.user.is_authenticated:
            if user := _get_user_according_to_requested_endpoint(request.path):
                login(request, user)
                print(red(f"request auto-logged in as {user}"))
        return get_response(request)

    return middleware


def _get_user_according_to_requested_endpoint(
    endpoint: str,
) -> Optional[User]:
    client_prefixes = ["/api/client-contact/"]
    provider_prefixes = ["/api/provider-contact/"]
    make_client_contact = any(endpoint.startswith(p) for p in client_prefixes)
    make_provider_contact = any(endpoint.startswith(p) for p in provider_prefixes)
    assert not (make_client_contact and make_provider_contact)
    if make_client_contact:
        return get_user_model().objects.get(email="petra@pepsi.com")
    elif make_provider_contact:
        return get_user_model().objects.get(email="dimitri@deloitte.com")
    else:
        return None
