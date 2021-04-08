import json
from uuid import UUID

from django.conf import settings
from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
    HttpResponseForbidden,
    JsonResponse,
)
from django.views import View

from app.http_api.serializers import (
    CaseSerializer,
    ClientProviderRelationshipSerializer,
    ApplicantSerializer,
    ProviderSerializer,
    ProviderContactSerializer,
)
from client.models import Case, ClientContact


# TODO: Refactor to share implementation with _ProviderContactView
class _ClientContactView(View):
    def setup(self, *args, **kwargs):
        self.client_contact: ClientContact
        super().setup(*args, **kwargs)
        try:
            self.client_contact = ClientContact.objects.get(
                user_id=self.request.user.id  # type: ignore
            )
        except ClientContact.DoesNotExist:
            self.client_contact = None  # type: ignore

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not self.client_contact:
            if settings.DEBUG:
                return HttpResponseForbidden("User is not a client contact")
            else:
                raise Http404
        else:
            return super().dispatch(request, *args, **kwargs)


class ApplicantsList(_ClientContactView):
    def get(self, request: HttpRequest) -> HttpResponse:
        # TODO: sorting
        applicants = self.client_contact.applicants()
        serializer = ApplicantSerializer(applicants, many=True)
        return JsonResponse(serializer.data, safe=False)


class CaseView(_ClientContactView):
    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        try:
            case = self.client_contact.cases_with_read_permission.get(id=id)
        except Case.DoesNotExist:
            if settings.DEBUG:
                raise Http404(
                    f"Case {id} does not exist "
                    f"or {self.client_contact} does not have read permission for it."
                )
            else:
                raise Http404
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
            serializer.create_for_client_contact(client_contact=self.client_contact)
            return JsonResponse({"errors": None})
        else:
            return JsonResponse({"errors": serializer.errors})


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
            process_id = UUID(request.GET["process_id"])
        except (KeyError, ValueError, TypeError):
            raise Http404("process_id key of URL parameters must be a valid UUID")
        provider_contacts = self.client_contact.provider_contacts_for_process(
            process_id
        )
        serializer = ProviderContactSerializer(provider_contacts, many=True)
        return JsonResponse(serializer.data, safe=False)
