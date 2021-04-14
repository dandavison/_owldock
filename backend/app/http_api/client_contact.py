import json
from uuid import UUID

from django.db.transaction import atomic
from django.http import (
    HttpRequest,
    HttpResponse,
    JsonResponse,
)
from django.views import View

from app.http_api.case_step_utils import perform_case_step_transition
from app.http_api.serializers import (
    CaseSerializer,
    CaseStepSerializer,
    ClientProviderRelationshipSerializer,
    ApplicantSerializer,
    ProviderContactSerializer,
)
from app.models import ProviderContact
from client.models import Case, ClientContact
from client.models.case_step import CaseStep
from owldock.api.http import (
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    make_explanatory_http_response,
)
from owldock.state_machine.django_fsm_utils import can_proceed, why_cant_proceed


# TODO: Refactor to share implementation with _ProviderContactView
class _ClientContactView(View):
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
        return JsonResponse(serializer.data, safe=False)


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
        return JsonResponse(serializer.data, safe=False)


class ApplicantList(_ClientContactView):
    def get(self, request: HttpRequest) -> HttpResponse:
        applicants = self.client_contact.applicants().all()
        serializer = ApplicantSerializer(applicants, many=True)
        return JsonResponse(serializer.data, safe=False)


class CaseList(_ClientContactView):
    def get(self, request: HttpRequest) -> HttpResponse:
        cases = self.client_contact.case_set.all()
        serializer = CaseSerializer(cases, many=True)
        return JsonResponse(serializer.data, safe=False)


class CreateCase(_ClientContactView):
    @atomic
    def post(self, request: HttpRequest) -> HttpResponse:
        serializer = CaseSerializer(data=json.loads(request.body))
        if serializer.is_valid():
            serializer.create_for_client_contact(client_contact=self.client_contact)
            return JsonResponse({"errors": None})
        else:
            return JsonResponse({"errors": serializer.errors})


class OfferCaseStep(_ClientContactView):
    @atomic
    def post(self, request: HttpRequest, uuid: UUID) -> HttpResponse:
        try:
            case_step_data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest(
                # TODO: handle non utf-8
                f"Request body could not be deserialized as JSON: {request.body.decode('utf-8')}"
            )
        try:
            provider_contact_uuid = case_step_data["active_contract"][
                "provider_contact_uuid"
            ]
        except (KeyError, TypeError):
            return HttpResponseBadRequest(
                "POST data must contain active_contract.provider_contact_uuid"
            )

        try:
            provider_contact = ProviderContact.objects.get(uuid=provider_contact_uuid)
        except ProviderContact.DoesNotExist:
            return HttpResponseNotFound(
                f"ProviderContact {provider_contact_uuid} does not exist"
            )

        qs = self.client_contact.case_steps()
        kwargs = {"uuid": uuid}
        try:
            case_step = qs.get(uuid=uuid)
        except CaseStep.DoesNotExist:
            return make_explanatory_http_response(
                qs, "client_contact.case_steps()", **kwargs
            )

        transition = case_step.offer
        if not can_proceed(transition):
            return HttpResponseForbidden(
                f"Case step {case_step} cannot do transition: {transition.__name__}:\n"
                f"{why_cant_proceed(transition)}"
            )
        transition(provider_contact=provider_contact)
        case_step.save()
        serializer = CaseStepSerializer(case_step)
        return JsonResponse(serializer.data, safe=False)


class RetractCaseStep(_ClientContactView):
    def post(self, request: HttpRequest, uuid: UUID) -> HttpResponse:
        return perform_case_step_transition(
            "reject",
            self.client_contact.case_steps(),
            "client_contact.case_steps()",
            uuid=uuid,
        )


class ClientProviderRelationshipList(_ClientContactView):
    def get(self, request: HttpRequest) -> HttpResponse:
        provider_relationships = self.client_contact.provider_relationships()
        serializer = ClientProviderRelationshipSerializer(
            provider_relationships, many=True
        )
        return JsonResponse(serializer.data, safe=False)


class ProviderContactList(_ClientContactView):
    def get(self, request: HttpRequest) -> HttpResponse:
        try:
            process_uuid = UUID(request.GET["process_uuid"])
        except (KeyError, ValueError, TypeError):
            raise HttpResponseBadRequest(
                "process_uuid key of URL parameters must be a valid UUID"
            )
        provider_contacts = self.client_contact.provider_contacts_for_process(
            process_uuid
        )
        serializer = ProviderContactSerializer(provider_contacts, many=True)
        return JsonResponse(serializer.data, safe=False)
