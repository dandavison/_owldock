import json

from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404

from app.exceptions import PermissionDenied
from app.models import CaseStep, ProviderContact
from app.http_api.serializers import (
    CaseSerializer,
    ApplicantSerializer,
    ProviderContactSerializer,
)


class _ProviderContactView(View):
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        try:
            self.provider_contact = ProviderContact.objects.get(  # pylint: disable=attribute-defined-outside-init
                user=self.request.user  # type: ignore
            )
        except ProviderContact.DoesNotExist as exc:
            raise Http404 from exc


class Case(_ProviderContactView):
    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        case = self.provider_contact.get_case_with_read_permissions(case_id=id)
        serializer = CaseSerializer(case)
        return JsonResponse(serializer.data, safe=False)


class CaseList(_ProviderContactView):
    def get(self, request: HttpRequest) -> HttpResponse:
        cases = self.provider_contact.case_set.all()
        serializer = CaseSerializer(data=cases, many=True)
        serializer.is_valid()
        return JsonResponse(serializer.data, safe=False)


class CaseStepUploadFiles(_ProviderContactView):
    def post(self, request: HttpRequest, step_id: int) -> HttpResponse:
        try:
            self.provider_contact.add_uploaded_files_to_case_step(
                request.FILES.getlist("file"), step_id=step_id
            )
        except (PermissionDenied, CaseStep.DoesNotExist) as exc:
            raise Http404
        else:
            return JsonResponse({"errors": None})