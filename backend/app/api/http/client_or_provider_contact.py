from typing import Union
from uuid import UUID

from django.http import HttpRequest, HttpResponse

from app.models import ProviderContact
from app.api.serializers import CaseSerializer
from client.models import ClientContact
from owldock.dev.db_utils import assert_max_queries, print_queries
from owldock.state_machine.role import get_role_from_http_request
from owldock.http import make_explanatory_http_response, OwldockJsonResponse


class ClientOrProviderCaseViewMixin:
    def _get(
        self,
        request: HttpRequest,
        uuid: UUID,
        client_or_provider_contact: Union[ClientContact, ProviderContact],
    ) -> HttpResponse:
        kwargs = {"uuid": uuid}
        qs = client_or_provider_contact.cases().filter(**kwargs)
        print("Pre-serialization queries")
        with print_queries():
            cases = CaseSerializer.prefetch_cases(qs, client_or_provider_contact)
        if not cases:
            return make_explanatory_http_response(
                qs, "client_or_provider_contact.cases()", **kwargs
            )
        [case] = cases

        get_role_from_http_request(request)  # cache it

        with assert_max_queries(19):  # TODO: should be <=2
            serializer = CaseSerializer(case)
            response = OwldockJsonResponse(serializer.data)

        return response


class ClientOrProviderCaseListMixin:
    def _get(
        self,
        request: HttpRequest,
        client_or_provider_contact: Union[ClientContact, ProviderContact],
    ) -> HttpResponse:

        print("Pre-serialization queries")
        with print_queries():
            cases = CaseSerializer.get_cases_for_client_or_provider_contact(
                client_or_provider_contact
            )

        get_role_from_http_request(request)  # cache it

        # TODO: O(1) query assertion
        serializer = CaseSerializer(cases, many=True)
        response = OwldockJsonResponse(serializer.data)

        return response
