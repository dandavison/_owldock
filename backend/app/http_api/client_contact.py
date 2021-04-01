import json
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404

from app.http_api.serializers import (
    CaseSerializer,
    ApplicantSerializer,
    ProviderContactSerializer,
)
from app.models import ClientContact, ProviderContact


class _ClientContactView(View):
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        try:
            self.client_contact = ClientContact.objects.get(  # pylint: disable=attribute-defined-outside-init
                user=self.request.user  # type: ignore
            )
        except ClientContact.DoesNotExist as exc:
            raise Http404 from exc


class ApplicantsList(_ClientContactView):
    def get(self, request: HttpRequest) -> HttpResponse:
        applicants = self.client_contact.applicants().order_by("user__last_name")
        serializer = ApplicantSerializer(applicants, many=True)
        return JsonResponse(serializer.data, safe=False)


class Case(_ClientContactView):
    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        case = get_object_or_404(self.client_contact.case_set.all(), id=id)
        serializer = CaseSerializer(case)
        return JsonResponse(serializer.data, safe=False)


class CaseList(_ClientContactView):
    def get(self, request: HttpRequest) -> HttpResponse:
        cases = self.client_contact.case_set.all()
        serializer = CaseSerializer(cases, many=True)
        return JsonResponse(serializer.data, safe=False)


class CreateCase(_ClientContactView):
    def post(self, request: HttpRequest) -> HttpResponse:
        serializer = CaseSerializer(data=json.loads(request.body))
        if serializer.is_valid():
            serializer.create_for_client_contact(
                serializer.validated_data, client_contact=self.client_contact
            )
            return JsonResponse({"errors": None})
        else:
            return JsonResponse({"errors": serializer.errors})


class ProviderContactList(_ClientContactView):
    def get(self, request: HttpRequest) -> HttpResponse:
        try:
            process_id = int(request.GET["process_id"])
        except (KeyError, ValueError, TypeError):
            raise Http404("process_id must be supplied in URL parameters")
        provider_contacts = self.client_contact.provider_contacts(process_id)
        serializer = ProviderContactSerializer(provider_contacts, many=True)
        return JsonResponse(serializer.data, safe=False)
