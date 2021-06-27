from typing import Union
from uuid import UUID

from django.http import HttpRequest, HttpResponse

from app import models as app_orm_models
from client import api as client_api
from client import models as client_orm_models
from owldock.dev.db_utils import assert_max_queries
from owldock.state_machine.role import get_role_from_http_request
from owldock.http import make_explanatory_http_response, OwldockJsonResponse


class ClientOrProviderCaseViewMixin:
    def _get(
        self,
        request: HttpRequest,
        uuid: UUID,
        client_or_provider_contact: Union[
            client_orm_models.ClientContact, app_orm_models.ProviderContact
        ],
    ) -> HttpResponse:
        kwargs = {"uuid": uuid}
        qs = client_or_provider_contact.cases().filter(**kwargs)
        print("Pre-serialization queries")
        cases = client_api.read.case.prefetch_cases(qs, client_or_provider_contact)
        if not cases:
            return make_explanatory_http_response(
                qs, "client_or_provider_contact.cases()", **kwargs
            )
        [case] = cases

        get_role_from_http_request(request)  # cache it

        with assert_max_queries(25):  # TODO: should be <=2
            api_obj = client_api.models.Case.from_orm(case)
            response = OwldockJsonResponse(api_obj.dict())

        return response


class ClientOrProviderCaseListMixin:
    def _get(
        self,
        request: HttpRequest,
        client_or_provider_contact: Union[
            client_orm_models.ClientContact, app_orm_models.ProviderContact
        ],
    ) -> HttpResponse:

        orm_models = client_api.read.case.get_cases_for_client_or_provider_contact(
            client_or_provider_contact
        )

        get_role_from_http_request(request)  # cache it

        # TODO: O(1) query assertion
        api_obj = client_api.models.CaseList.from_orm(orm_models)
        response = OwldockJsonResponse(api_obj.dict()["__root__"])

        return response
