import json
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.views import View

from app.models import ClientContact, ProviderContact
from .serializers import CaseSerializer, EmployeeSerializer, ProviderContactSerializer


class _ClientContactView(View):
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        try:
            self.client_contact = ClientContact.objects.get(  # pylint: disable=attribute-defined-outside-init
                user=self.request.user  # type: ignore
            )
        except ClientContact.DoesNotExist as exc:
            raise Http404 from exc


class EmployeesList(_ClientContactView):
    def get(self, request: HttpRequest) -> HttpResponse:
        employees = self.client_contact.employees().order_by("user__last_name")
        serializer = EmployeeSerializer(data=employees, many=True)
        serializer.is_valid()
        return JsonResponse(serializer.data, safe=False)


class CaseList(_ClientContactView):
    def get(self, request: HttpRequest) -> HttpResponse:
        cases = self.client_contact.case_set.all()
        serializer = CaseSerializer(data=cases, many=True)
        serializer.is_valid()
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
        serializer = ProviderContactSerializer(data=provider_contacts, many=True)
        serializer.is_valid()
        return JsonResponse(serializer.data, safe=False)
