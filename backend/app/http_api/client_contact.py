from django.contrib.auth import get_user_model
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.views import View
from django_countries.serializers import CountryFieldMixin
from django_typomatic import ts_interface
from rest_framework import serializers

from app.models import Case, ClientContact
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


class CaseList(_ClientContactView):
    def get(self, request: HttpRequest) -> HttpResponse:
        cases = self.client_contact.case_set.all()
        serializer = CaseSerializer(data=cases, many=True)
        serializer.is_valid()
        return JsonResponse(serializer.data, safe=False)


# FIXME: These serializers are sending the user.password hash


@ts_interface()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"
        depth = 2


@ts_interface()
class EmployeeSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
        depth = 1


@ts_interface()
class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = "__all__"
        depth = 2
