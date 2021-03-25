"""
Django Rest Framework Serializer classes used by the HTTP API.

Note that there is a connection to the javascript codebase here:
When we run `make serve` and `make build` in the ui/ directory, the first
thing that happens is they generate typescript interface definitions from
these serializer classes. Thus, there will be typescript compiler error messages
if the backend and frontend code have got out of sync.
"""
from django.contrib.auth.models import User  # pylint: disable=imported-auth-user
from django_countries.serializers import CountryFieldMixin
from django_typomatic import ts_interface
from rest_framework.serializers import ModelSerializer

from app.models import Case
from app.models import (
    Client,
    ClientContact,
    Country,
    Employee,
    Route,
    Process,
    ProcessStep,
    Provider,
    ProviderContact,
    Service,
)


@ts_interface()
class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ["name", "code", "unicode_flag"]


@ts_interface()
class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = ["name"]


@ts_interface()
class RouteSerializer(ModelSerializer):
    host_country = CountrySerializer()

    class Meta:
        model = Route
        fields = ["name", "host_country"]


@ts_interface()
class ProcessStepSerializer(ModelSerializer):
    service = ServiceSerializer()

    class Meta:
        model = ProcessStep
        fields = ["sequence_number", "service"]
        ordering = ["sequence_number"]


@ts_interface()
class ProcessSerializer(ModelSerializer):
    nationality = CountrySerializer()
    home_country = CountrySerializer()
    steps = ProcessStepSerializer(many=True)

    class Meta:
        model = Process
        fields = ["nationality", "home_country", "steps"]


@ts_interface()
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        depth = 2


@ts_interface()
class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ["name"]


@ts_interface()
class EmployeeSerializer(CountryFieldMixin, ModelSerializer):
    user = UserSerializer()
    employer = ClientSerializer()
    home_country = CountrySerializer()
    nationalities = CountrySerializer(many=True)

    class Meta:
        model = Employee
        fields = ["user", "employer", "home_country", "nationalities"]


@ts_interface()
class ClientContactSerializer(CountryFieldMixin, ModelSerializer):
    user = UserSerializer()
    client = ClientSerializer()

    class Meta:
        model = ClientContact
        fields = ["user", "client"]


@ts_interface()
class ProviderSerializer(ModelSerializer):
    class Meta:
        model = Provider
        fields = ["name"]


@ts_interface()
class ProviderContactSerializer(CountryFieldMixin, ModelSerializer):
    user = UserSerializer()
    provider = ProviderSerializer()

    class Meta:
        model = ProviderContact
        fields = ["user", "provider"]


@ts_interface()
class CaseSerializer(ModelSerializer):
    client_contact = ClientContactSerializer()
    employee = EmployeeSerializer()
    route = RouteSerializer()
    host_country = CountrySerializer()
    provider_contact = ProviderContactSerializer()

    class Meta:
        model = Case
        fields = [
            "id",
            "client_contact",
            "employee",
            "route",
            "host_country",
            "target_entry_date",
            "provider_contact",
        ]
