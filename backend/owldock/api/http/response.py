from typing import Type, TypeVar

from django import http
from django.conf import settings
from django.db.models import QuerySet
from django_tools.middlewares.ThreadLocal import get_current_request


class _OwldockHttpErrorResponse(Exception):
    pass


def HttpResponseBadRequest(msg: str) -> http.HttpResponseBadRequest:
    return _error_response(http.HttpResponseBadRequest, msg)


def HttpResponseForbidden(msg: str) -> http.HttpResponseForbidden:
    return _error_response(http.HttpResponseForbidden, msg)


def HttpResponseNotFound(msg: str) -> http.HttpResponseNotFound:
    return _error_response(http.HttpResponseNotFound, msg)


def make_explanatory_http_response(
    queryset: QuerySet, queryset_name: str, **kwargs
) -> http.HttpResponse:
    assert not queryset.filter(**kwargs).exists(), "Expected empty query results"
    if queryset.model.objects.filter(**kwargs).exists():
        return HttpResponseForbidden(
            f"{queryset.model.__name__} {kwargs} not in {queryset_name} ({queryset.count()})"
        )
    else:
        return HttpResponseNotFound(
            f"{queryset.model.__name__} {kwargs} does not exist"
        )


R = TypeVar("R", bound=http.HttpResponse)


def _error_response(response_cls: Type[R], msg: str) -> R:
    """
    Return HTTP response in prod or raise exception in dev.
    """
    if settings.DEBUG or not get_current_request():
        # Cause a traceback to be generated in dev and tests.
        raise _OwldockHttpErrorResponse(msg)
    else:
        # Do not give the message to an http client in production.
        return response_cls()
