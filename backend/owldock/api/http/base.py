import json

from clint.textui import colored
from django.conf import settings
from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.views import View

from owldock.dev.db_utils import print_query_counts


class BaseView(View):
    if settings.DEV:

        def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
            print(colored.black(request, bold=True))
            if (
                request.headers.get("Content-Type", "").startswith("text/")
                and request.body
            ):
                print(json.dumps(json.loads(request.body), indent=2, sort_keys=True))
            with print_query_counts():
                return super().dispatch(request, *args, **kwargs)

    else:

        def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
            with print_query_counts():
                return super().dispatch(request, *args, **kwargs)
