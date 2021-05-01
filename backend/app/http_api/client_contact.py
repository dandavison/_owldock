import json
from uuid import UUID

from django.db.transaction import atomic
from django.http import (
    HttpRequest,
    HttpResponse,
)

from app.http_api.base import BaseView
from app.http_api.case_step_utils import (
    add_uploaded_files_to_case_step,
    perform_case_step_transition,
)
from app.http_api.client_or_provider_contact import ClientOrProviderCaseListMixin
from app.http_api.serializers import (
    CaseSerializer,
    ClientProviderRelationshipSerializer,
    ApplicantSerializer,
    ProviderContactSerializer,
)
from app.models import ProviderContact
from client.models import Case, ClientContact
from owldock.http import (
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    make_explanatory_http_response,
    OwldockJsonResponse,
)


# TODO: Refactor to share implementation with _ProviderContactView
class _ClientContactView(BaseView):
    def setup(self, *args, **kwargs):
        self.client_contact: ClientContact
        super().setup(*args, **kwargs)
        try:
            self.client_contact = ClientContact.objects.get(
                user_uuid=self.request.user.uuid  # type: ignore
            )
        except ClientContact.DoesNotExist:
            self.client_contact = None  # type: ignore

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not self.client_contact:
            return HttpResponseForbidden("User is not a client contact")
        else:
            return super().dispatch(request, *args, **kwargs)


class ApplicantsList(_ClientContactView):
    def get(self, request: HttpRequest) -> HttpResponse:
        # TODO: sorting
        applicants = self.client_contact.applicants()
        serializer = ApplicantSerializer(applicants, many=True)
        return OwldockJsonResponse(serializer.data)


class CaseView(_ClientContactView):
    def get(self, request: HttpRequest, uuid: UUID) -> HttpResponse:
        qs = self.client_contact.cases()
        kwargs = {"uuid": uuid}
        try:
            case = qs.get(**kwargs)
        except Case.DoesNotExist:
            return make_explanatory_http_response(
                qs, "client_contact.cases()", **kwargs
            )
        serializer = CaseSerializer(case)
        return OwldockJsonResponse(serializer.data)


class ApplicantList(_ClientContactView):
    def get(self, request: HttpRequest) -> HttpResponse:
        applicants = self.client_contact.applicants().all()
        serializer = ApplicantSerializer(applicants, many=True)
        return OwldockJsonResponse(serializer.data)


class CaseList(ClientOrProviderCaseListMixin, _ClientContactView):
    def get(self, request: HttpRequest) -> HttpResponse:
        return self._get(self.client_contact, request)


class CreateCase(_ClientContactView):
    @atomic
    def post(self, request: HttpRequest) -> HttpResponse:
        serializer = CaseSerializer(data=json.loads(request.body))
        if serializer.is_valid():
            serializer.create_for_client_contact(client_contact=self.client_contact)
            return OwldockJsonResponse(None)
        else:
            return OwldockJsonResponse({"validation-errors": serializer.errors})


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
        provider_contact = ProviderContact.objects.get(uuid=provider_contact_uuid)
    except ProviderContact.DoesNotExist:
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
        serializer = ClientProviderRelationshipSerializer(
            provider_relationships, many=True
        )
        return OwldockJsonResponse(serializer.data)


class ProviderContactList(_ClientContactView):
    primary_only = False

    def get(self, request: HttpRequest) -> HttpResponse:
        try:
            process_uuid = UUID(request.GET["process_uuid"])
        except (KeyError, ValueError, TypeError):
            return HttpResponseBadRequest(
                "process_uuid key of URL parameters must be a valid UUID"
            )
        provider_contacts = (
            self.client_contact.provider_primary_contacts_for_process(process_uuid)
            if self.primary_only
            else self.client_contact.provider_contacts_for_process(process_uuid)
        )
        serializer = ProviderContactSerializer(provider_contacts, many=True)
        return OwldockJsonResponse(serializer.data)


class PrimaryProviderContactList(ProviderContactList):
    primary_only = True
