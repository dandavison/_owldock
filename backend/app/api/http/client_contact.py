import json
from uuid import UUID

from django.db.transaction import atomic
from django.http import (
    HttpRequest,
    HttpResponse,
)
from pydantic import ValidationError

from app.api.http.case_step_utils import (
    add_uploaded_files_to_case_step,
    perform_case_step_transition,
)
from app.api.http.client_or_provider_contact import (
    ClientOrProviderCaseListMixin,
    ClientOrProviderCaseViewMixin,
)
from app import api as app_api
from app import models as app_orm_models
from client import api as client_api
from client import models as client_orm_models
from owldock.api.http.base import BaseView
from owldock.http import (
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    OwldockJsonResponse,
)
from owldock.dev.db_utils import assert_max_queries


# TODO: Refactor to share implementation with _ProviderContactView
class _ClientContactView(BaseView):
    def setup(self, *args, **kwargs):
        self.client_contact: client_orm_models.ClientContact
        super().setup(*args, **kwargs)
        try:
            self.client_contact = client_orm_models.ClientContact.objects.get(
                user_uuid=self.request.user.uuid  # type: ignore
            )
        except client_orm_models.ClientContact.DoesNotExist:
            self.client_contact = None  # type: ignore

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not self.client_contact:
            return HttpResponseForbidden("User is not a client contact")
        else:
            return super().dispatch(request, *args, **kwargs)


class ApplicantList(_ClientContactView):
    def get(self, request: HttpRequest) -> HttpResponse:
        with assert_max_queries(5):
            applicant_orm_models = client_api.read.applicant.get_orm_models(
                self.client_contact
            )

        with assert_max_queries(5):
            applicant_list_api_model = client_api.models.ApplicantList.from_orm(
                applicant_orm_models
            )
            response = OwldockJsonResponse(applicant_list_api_model.dict()["__root__"])

        return response


class CaseView(ClientOrProviderCaseViewMixin, _ClientContactView):
    def get(self, request: HttpRequest, uuid: UUID) -> HttpResponse:
        return self._get(request, uuid, self.client_contact)


class CaseList(ClientOrProviderCaseListMixin, _ClientContactView):
    def get(self, request: HttpRequest) -> HttpResponse:
        return self._get(request, self.client_contact)


class CreateCase(_ClientContactView):
    @atomic
    def post(self, request: HttpRequest) -> HttpResponse:
        try:
            api_obj = client_api.models.Case(**json.loads(request.body))
        except ValidationError as e:
            return OwldockJsonResponse({"validation-errors": e.json()})
        else:
            client_api.write.case.create_for_client_contact(
                api_obj, client_contact=self.client_contact
            )
            return OwldockJsonResponse(None)


class EarmarkCaseStep(_ClientContactView):
    @atomic
    def post(self, request: HttpRequest, uuid: UUID) -> HttpResponse:
        return _perform_earmark_or_offer_case_step_transition(
            request, self.client_contact, uuid, "earmark"
        )


class OfferCaseStep(_ClientContactView):
    @atomic
    def post(self, request: HttpRequest, uuid: UUID) -> HttpResponse:
        return _perform_earmark_or_offer_case_step_transition(
            request, self.client_contact, uuid, "offer"
        )


def _perform_earmark_or_offer_case_step_transition(
    request, client_contact, case_step_uuid, transition: str
) -> HttpResponse:
    try:
        case_step_data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest(
            # TODO: handle non utf-8
            f"Request body could not be deserialized as JSON: {request.body.decode('utf-8')}"
        )
    try:
        provider_contact_uuid = case_step_data["active_contract"]["provider_contact"][
            "uuid"
        ]
    except (KeyError, TypeError):
        return HttpResponseBadRequest(
            "POST data must contain active_contract.provider_contact.uuid "
            "or active_contract.provider_contact_uuid"
        )

    try:
        provider_contact = app_orm_models.ProviderContact.objects.get(
            uuid=provider_contact_uuid
        )
    except app_orm_models.ProviderContact.DoesNotExist:
        return HttpResponseNotFound(
            f"ProviderContact {provider_contact_uuid} does not exist"
        )

    return perform_case_step_transition(
        transition,
        client_contact.case_steps(),
        "client_contact.case_steps()",
        query_kwargs={"uuid": case_step_uuid},
        transition_kwargs={"provider_contact": provider_contact},
    )


class RetractCaseStep(_ClientContactView):
    def post(self, request: HttpRequest, uuid: UUID) -> HttpResponse:
        return perform_case_step_transition(
            "retract",
            self.client_contact.case_steps(),
            "client_contact.case_steps()",
            query_kwargs={"uuid": uuid},
        )


class CaseStepUploadFiles(_ClientContactView):
    @atomic
    def post(self, request: HttpRequest, uuid: UUID) -> HttpResponse:
        return add_uploaded_files_to_case_step(self.client_contact, request, uuid)


class ClientProviderRelationshipList(_ClientContactView):
    def get(self, request: HttpRequest) -> HttpResponse:
        provider_relationships = self.client_contact.provider_relationships()
        api_obj = client_api.models.ClientProviderRelationshipList.from_orm(
            provider_relationships
        )
        return OwldockJsonResponse(api_obj.dict()["__root__"])


class ProviderContactList(_ClientContactView):
    primary_only = False

    def get(self, request: HttpRequest) -> HttpResponse:
        try:
            process_uuid = UUID(request.GET["process_uuid"])
        except (KeyError, ValueError, TypeError):
            return HttpResponseBadRequest(
                "process_uuid key of URL parameters must be a valid UUID"
            )
        orm_objs = list(
            self.client_contact.provider_primary_contacts_for_process(process_uuid)
            if self.primary_only
            else self.client_contact.provider_contacts_for_process(process_uuid)
        )
        api_obj = app_api.models.ProviderContactList.from_orm(orm_objs)
        return OwldockJsonResponse(api_obj.dict()["__root__"])


class PrimaryProviderContactList(ProviderContactList):
    primary_only = True
