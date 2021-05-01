from typing import TypeVar
from uuid import UUID

from django.db.models import Model
from django.db.transaction import atomic
from django.http import (
    HttpRequest,
    HttpResponse,
)

from app.models import ProviderContact
from app.http_api.base import BaseView
from app.http_api.case_step_utils import (
    add_uploaded_files_to_case_step,
    perform_case_step_transition,
)
from app.http_api.client_or_provider_contact import (
    ClientOrProviderCaseListMixin,
    ClientOrProviderCaseViewMixin,
)
from app.http_api.serializers import (
    ApplicantSerializer,
    CaseSerializer,
    CaseStepSerializer,
)
from client.models.case_step import Case, CaseStep
from owldock.http import (
    HttpResponseForbidden,
    make_explanatory_http_response,
    OwldockJsonResponse,
)


M = TypeVar("M", bound=Model)


# TODO: Refactor to share implementation with _ClientContactView
class _ProviderContactView(BaseView):
    def setup(self, *args, **kwargs):
        self.provider_contact: ProviderContact

        super().setup(*args, **kwargs)
        try:
            self.provider_contact = ProviderContact.objects.get(
                user=self.request.user  # type: ignore
            )
        except ProviderContact.DoesNotExist:
            self.provider_contact = None  # type: ignore

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not self.provider_contact:
            return HttpResponseForbidden("User is not a provider contact")
        else:
            return super().dispatch(request, *args, **kwargs)


class ApplicantList(_ProviderContactView):
    def get(self, request: HttpRequest) -> HttpResponse:
        applicants = self.provider_contact.applicants().all()
        serializer = ApplicantSerializer(applicants, many=True)
        return OwldockJsonResponse(serializer.data)


class CaseView(ClientOrProviderCaseViewMixin, _ProviderContactView):
    def get(self, request: HttpRequest, uuid: UUID) -> HttpResponse:
        return self._get(request, uuid, self.provider_contact)


class CaseStepView(_ProviderContactView):
    def get(self, request: HttpRequest, uuid: UUID) -> HttpResponse:
        qs = self.provider_contact.case_steps()
        kwargs = {"uuid": uuid}
        try:
            case_step = qs.get(**kwargs)
        except CaseStep.DoesNotExist:
            return make_explanatory_http_response(
                qs, "provider_contact.case_steps()", **kwargs
            )
        serializer = CaseStepSerializer(case_step)
        return OwldockJsonResponse(serializer.data)


class CaseList(ClientOrProviderCaseListMixin, _ProviderContactView):
    def get(self, request: HttpRequest) -> HttpResponse:
        return self._get(request, self.provider_contact)


class CaseStepUploadFiles(_ProviderContactView):
    @atomic
    def post(self, request: HttpRequest, uuid: UUID) -> HttpResponse:
        return add_uploaded_files_to_case_step(self.provider_contact, request, uuid)


class AcceptCaseStep(_ProviderContactView):
    def post(self, request: HttpRequest, uuid: UUID) -> HttpResponse:
        return perform_case_step_transition(
            "accept",
            self.provider_contact.case_steps(),
            "provider_contact.case_steps()",
            query_kwargs={"uuid": uuid},
        )


class RejectCaseStep(_ProviderContactView):
    def post(self, request: HttpRequest, uuid: UUID) -> HttpResponse:
        return perform_case_step_transition(
            "reject",
            self.provider_contact.case_steps(),
            "provider_contact.case_steps()",
            query_kwargs={"uuid": uuid},
        )


class CompleteCaseStep(_ProviderContactView):
    def post(self, request: HttpRequest, uuid: UUID) -> HttpResponse:
        return perform_case_step_transition(
            "complete",
            self.provider_contact.case_steps(),
            "provider_contact.case_steps()",
            query_kwargs={"uuid": uuid},
        )
