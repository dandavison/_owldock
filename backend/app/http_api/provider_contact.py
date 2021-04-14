from typing import TypeVar
from uuid import UUID

from django.db.models import Model
from django.db.transaction import atomic
from django.http import (
    HttpRequest,
    HttpResponse,
    JsonResponse,
)
from django.views import View

from app.exceptions import PermissionDenied
from app.models import ProviderContact
from app.http_api.serializers import (
    ApplicantSerializer,
    CaseSerializer,
    CaseStepSerializer,
)
from client.models.case_step import Case, CaseStep
from owldock.api.http import (
    HttpResponseForbidden,
    HttpResponseNotFound,
    make_explanatory_http_response,
)
from app.http_api.case_step_utils import perform_case_step_transition


M = TypeVar("M", bound=Model)


# TODO: Refactor to share implementation with _ClientContactView
class _ProviderContactView(View):
    def setup(self, *args, **kwargs):
        self.provider_contact: ProviderContact

        super().setup(*args, **kwargs)
        try:
            self.provider_contact = ProviderContact.objects.get(
                user_id=self.request.user.uuid  # type: ignore
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
        return JsonResponse(serializer.data, safe=False)


class CaseView(_ProviderContactView):
    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        qs = self.provider_contact.cases()
        try:
            case = qs.get(id=id)
        except Case.DoesNotExist:
            return make_explanatory_http_response(qs, "provider_contact.cases()", id=id)
        serializer = CaseSerializer(case)
        return JsonResponse(serializer.data, safe=False)


class CaseStepView(_ProviderContactView):
    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        qs = self.provider_contact.case_steps()
        try:
            case_step = qs.get(id=id)
        except CaseStep.DoesNotExist:
            return make_explanatory_http_response(
                qs, "provider_contact.case_steps()", id=id
            )
        serializer = CaseStepSerializer(case_step)
        return JsonResponse(serializer.data, safe=False)


class CaseList(_ProviderContactView):
    def get(self, request: HttpRequest) -> HttpResponse:
        cases = self.provider_contact.cases().order_by("-created_at")
        serializer = CaseSerializer(data=cases, many=True)
        serializer.is_valid()
        return JsonResponse(serializer.data, safe=False)


class CaseStepUploadFiles(_ProviderContactView):
    @atomic
    def post(self, request: HttpRequest, id: UUID) -> HttpResponse:
        try:
            self.provider_contact.add_uploaded_files_to_case_step(
                request.FILES.getlist("file"), step_id=id
            )
        except PermissionDenied:
            return HttpResponseForbidden(
                (
                    f"User {request.user} does not have permission to upload files to "
                    f"case step {id}"
                )
            )
        except CaseStep.DoesNotExist:
            return HttpResponseNotFound(f"Case step {id} does not exist")
        else:
            return JsonResponse({"errors": None})


class AcceptCaseStep(_ProviderContactView):
    def post(self, request: HttpRequest, id: UUID) -> HttpResponse:
        return perform_case_step_transition(
            "accept",
            self.provider_contact.case_steps(),
            "provider_contact.case_steps()",
            id=id,
        )


class RejectCaseStep(_ProviderContactView):
    def post(self, request: HttpRequest, id: UUID) -> HttpResponse:
        return perform_case_step_transition(
            "reject",
            self.provider_contact.case_steps(),
            "provider_contact.case_steps()",
            id=id,
        )


class CompleteCaseStep(_ProviderContactView):
    def post(self, request: HttpRequest, id: UUID) -> HttpResponse:
        return perform_case_step_transition(
            "complete",
            self.provider_contact.case_steps(),
            "provider_contact.case_steps()",
            id=id,
        )
