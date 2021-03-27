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
from rest_framework.serializers import ModelSerializer, IntegerField

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
        fields = ["id", "name", "code", "unicode_flag"]


@ts_interface()
class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "name"]


@ts_interface()
class RouteSerializer(ModelSerializer):
    host_country = CountrySerializer()

    class Meta:
        model = Route
        fields = ["id", "name", "host_country"]


@ts_interface()
class ProcessStepSerializer(ModelSerializer):
    service = ServiceSerializer()

    class Meta:
        model = ProcessStep
        fields = ["id", "sequence_number", "service"]
        ordering = ["sequence_number"]


@ts_interface()
class ProcessSerializer(ModelSerializer):
    # By default, DRF will not make 'id' available in serializer.validated_data,
    # because it is a read-only field. But we need it when handling a POST to
    # create a case, in order to look up the process.
    id = IntegerField(read_only=False)
    route = RouteSerializer()
    nationality = CountrySerializer()
    home_country = CountrySerializer(allow_null=True)
    steps = ProcessStepSerializer(many=True)

    class Meta:
        model = Process
        fields = ["id", "route", "nationality", "home_country", "steps"]


@ts_interface()
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email"]
        depth = 2


@ts_interface()
class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name"]


@ts_interface()
class EmployeeSerializer(CountryFieldMixin, ModelSerializer):
    # By default, DRF will not make 'id' available in serializer.validated_data,
    # because it is a read-only field. But we need it when handling a POST to
    # create a case, in order to look up the employee.
    id = IntegerField(read_only=False)
    user = UserSerializer()
    employer = ClientSerializer()
    home_country = CountrySerializer()
    nationalities = CountrySerializer(many=True)

    class Meta:
        model = Employee
        fields = ["id", "user", "employer", "home_country", "nationalities"]


@ts_interface()
class ClientContactSerializer(CountryFieldMixin, ModelSerializer):
    user = UserSerializer()
    client = ClientSerializer()

    class Meta:
        model = ClientContact
        fields = ["id", "user", "client"]


@ts_interface()
class ProviderSerializer(ModelSerializer):
    class Meta:
        model = Provider
        fields = ["id", "name"]


@ts_interface()
class ProviderContactSerializer(CountryFieldMixin, ModelSerializer):
    user = UserSerializer()
    provider = ProviderSerializer()

    class Meta:
        model = ProviderContact
        fields = ["id", "user", "provider"]


@ts_interface()
class CaseSerializer(ModelSerializer):
    employee = EmployeeSerializer()
    process = ProcessSerializer()

    class Meta:
        model = Case
        fields = [
            "id",
            "employee",
            "process",
            "target_entry_date",
            "target_exit_date",
            "provider_contact",
        ]

    def create(self, validated_data: dict, client_contact: ClientContact):
        employee = validated_data.pop("employee")
        process = validated_data.pop("process")
        Case.objects.create(
            client_contact=client_contact,
            employee_id=employee["id"],
            process_id=process["id"],
            **validated_data,
        )
