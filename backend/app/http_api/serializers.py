"""
Django Rest Framework Serializer classes used by the HTTP API.

Note that there is a connection to the javascript codebase here:
When we run `make serve` and `make build` in the ui/ directory, the first
thing that happens is they generate typescript interface definitions from
these serializer classes. Thus, there will be typescript compiler error messages
if the backend and frontend code have got out of sync.

By default, DRF will not make 'id' available in serializer.validated_data,
because it is a read-only field. But we need it when handling a POST to
create a case, in order to look up the process.

allow_null is supplied on some serializer fields in order for client-side
objects without to type-check.
"""
from django.contrib.auth.models import User  # pylint: disable=imported-auth-user
from django_countries.serializers import CountryFieldMixin
from django_typomatic import ts_interface
from rest_framework.serializers import ModelSerializer, IntegerField

from app.models import (
    Applicant,
    Case,
    CaseStep,
    Client,
    ClientContact,
    Country,
    Process,
    ProcessStep,
    Provider,
    ProviderContact,
    Route,
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
    # See module docstring for explanation of read_only and allow_null
    id = IntegerField(read_only=False, allow_null=True, required=False)
    service = ServiceSerializer()

    class Meta:
        model = ProcessStep
        fields = ["id", "sequence_number", "service"]
        ordering = ["sequence_number"]


@ts_interface()
class ProcessSerializer(ModelSerializer):
    # See module docstring for explanation of read_only and allow_null
    id = IntegerField(read_only=False, allow_null=True, required=False)
    route = RouteSerializer()
    nationality = CountrySerializer()
    home_country = CountrySerializer(allow_null=True, required=False)
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
class ApplicantSerializer(CountryFieldMixin, ModelSerializer):
    # See module docstring for explanation of read_only and allow_null
    id = IntegerField(read_only=False, allow_null=True, required=False)
    user = UserSerializer()
    employer = ClientSerializer()
    home_country = CountrySerializer()
    nationalities = CountrySerializer(many=True)

    class Meta:
        model = Applicant
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
    # See module docstring for explanation of read_only and allow_null
    id = IntegerField(read_only=False, allow_null=True, required=False)
    user = UserSerializer()
    provider = ProviderSerializer()

    class Meta:
        model = ProviderContact
        fields = ["id", "user", "provider"]


@ts_interface()
class CaseStepSerializer(ModelSerializer):
    process_step = ProcessStepSerializer()

    class Meta:
        model = CaseStep
        fields = ["id", "process_step", "sequence_number"]
        ordering = ["sequence_number"]


@ts_interface()
class CaseSerializer(ModelSerializer):
    applicant = ApplicantSerializer()
    provider_contact = ProviderContactSerializer()
    process = ProcessSerializer()
    steps = CaseStepSerializer(many=True)

    class Meta:
        model = Case
        fields = [
            "id",
            "applicant",
            "provider_contact",
            "process",
            "steps",
            "created_at",
            "target_entry_date",
            "target_exit_date",
        ]

    def create_for_client_contact(
        self, validated_data: dict, client_contact: ClientContact
    ):
        applicant = validated_data.pop("applicant")
        provider_contact = validated_data.pop("provider_contact")
        process = validated_data.pop("process")
        case_steps = validated_data.pop("steps")
        case = Case.objects.create(
            client_contact=client_contact,
            applicant_id=applicant["id"],
            process_id=process["id"],
            provider_contact_id=provider_contact["id"],
            **validated_data,
        )
        for case_step in case_steps:
            case.steps.create(
                process_step_id=case_step["process_step"]["id"],
                sequence_number=case_step["sequence_number"],
            )
