from typing import TypeVar
from uuid import UUID

from django.db.models import Model
from django.db.transaction import atomic
from django.http import (
    HttpRequest,
    HttpResponse,
    JsonResponse,
)

from app.exceptions import PermissionDenied
from app.models import ProviderContact
from app.http_api.base import BaseView
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
        return JsonResponse(serializer.data, safe=False)


class CaseView(_ProviderContactView):
    def get(self, request: HttpRequest, uuid: UUID) -> HttpResponse:
        qs = self.provider_contact.cases()
        kwargs = {"uuid": uuid}
        try:
            case = qs.get(**kwargs)
        except Case.DoesNotExist:
            return make_explanatory_http_response(
                qs, "provider_contact.cases()", **kwargs
            )
        serializer = CaseSerializer(case)
        return JsonResponse(serializer.data, safe=False)


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
        return JsonResponse(serializer.data, safe=False)


class CaseList(_ProviderContactView):
    def get(self, request: HttpRequest) -> HttpResponse:
        cases = self.provider_contact.cases().order_by("-created_at")
        serializer = CaseSerializer(data=cases, many=True)
        serializer.is_valid()
        return JsonResponse(serializer.data, safe=False)


class CaseStepUploadFiles(_ProviderContactView):
    @atomic
    def post(self, request: HttpRequest, uuid: UUID) -> HttpResponse:
        try:
            self.provider_contact.add_uploaded_files_to_case_step(
                request.FILES.getlist("file"), step_uuid=uuid
            )
        except PermissionDenied:
            return HttpResponseForbidden(
                (
                    f"User {request.user} does not have permission to upload files to "
                    f"case step {uuid}"
                )
            )
        except CaseStep.DoesNotExist:
            try:
                case_step = self.provider_contact.cases_steps_with_read_permission.get(
                    uuid=uuid
                )
            except CaseStep.DoesNotExist:
                return HttpResponseNotFound(f"Case step {uuid} does not exist")
            else:
                return JsonResponse(
                    {
                        "errors": [
                            (
                                f"You don't currently have permission to upload files to this "
                                f"step. The status of this step is {case_step.state.value}."
                            )
                        ]
                    }
                )
        else:
            return JsonResponse({"errors": []})


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
