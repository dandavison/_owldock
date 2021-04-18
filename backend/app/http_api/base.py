import json

from django.conf import settings
from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.views import View

from clint.textui import colored


class BaseView(View):
    if settings.DEV:

        def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
            print(colored.black(request, bold=True))
            if request.body:
                print(json.dumps(json.loads(request.body), indent=2, sort_keys=True))
            return super().dispatch(request, *args, **kwargs)
