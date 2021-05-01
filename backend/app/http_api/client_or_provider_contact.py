from typing import Union

from django.http import HttpRequest, HttpResponse

from app.models import ProviderContact
from app.http_api.serializers import CaseSerializer
from client.models import ClientContact
from owldock.dev.db_utils import assert_n_queries, print_queries
from owldock.state_machine.role import get_role_from_http_request
from owldock.http import OwldockJsonResponse


class ClientOrProviderCaseListMixin:
    def _get(
        self,
        client_or_provider_contact: Union[ClientContact, ProviderContact],
        request: HttpRequest,
    ) -> HttpResponse:

        print("Pre-serialization queries")
        with print_queries():
            cases = CaseSerializer.get_cases_for_client_or_provider_contact(
                client_or_provider_contact
            )

        get_role_from_http_request(request)  # cache it

        with assert_n_queries(0):
            serializer = CaseSerializer(cases, many=True)
            response = OwldockJsonResponse(serializer.data)

        return response