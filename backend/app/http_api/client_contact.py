from django.http import Http404, HttpRequest, HttpResponse, JsonResponse

from django.views import View
from django_typomatic import ts_interface
from rest_framework import serializers

from app.models import ClientContact
from app.models import Employee


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
        employees = self.client_contact.employees()
        serializer = EmployeeSerializer(data=employees, many=True)
        serializer.is_valid()
        return JsonResponse(serializer.data, safe=False)


@ts_interface()
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
        depth = 1
