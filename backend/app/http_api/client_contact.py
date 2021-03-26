from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.views import View

from app.models import ClientContact
from .serializers import CaseSerializer, EmployeeSerializer


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
