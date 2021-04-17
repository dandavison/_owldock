"""
Django Rest Framework Serializer classes used by the HTTP API.

Note that there is a connection to the javascript codebase here:
When we run `make serve` and `make build` in the ui/ directory, the first
thing that happens is they generate typescript interface definitions from
these serializer classes. Thus, there will be typescript compiler error messages
if the backend and frontend code have got out of sync.

By default, DRF will not make 'uuid' available in serializer.validated_data,
because it is a read-only field. But we need it when handling a POST to
create a case, in order to look up the process.

allow_null is supplied on some serializer fields in order for client-side
objects without to type-check.
"""
from typing import List

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.db.transaction import atomic
from django_countries.serializers import CountryFieldMixin
from django_typomatic import ts_interface
from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    Serializer,
    UUIDField,
    URLField,
)

from app.models import (
    Country,
    StoredFile,
    Process,
    ProcessStep,
    Provider,
    ProviderContact,
    Route,
    Service,
)
from client.models import (
    Applicant,
    Case,
    Client,
    ClientContact,
    ClientProviderRelationship,
    State as CaseStepState,
)
from client.models.case_step import (
    CaseStep,
    CaseStepContract,
)


class BaseModelSerializer(ModelSerializer):
    @classmethod
    def get_select_related_fields(cls):
        for f in cls.Meta.fields:

            if f in ["user", "process", "home_country", "nationalities"]:
                continue

            # TODO: Is _declared_fields the right thing to be accessing here?
            if f in cls._declared_fields and isinstance(
                cls._declared_fields[f], BaseModelSerializer
            ):
                serializer: BaseModelSerializer = cls._declared_fields[f]
                has_nested = False
                for ff in serializer.get_select_related_fields():
                    yield f"{f}__{ff}"
                    has_nested = True
                if not has_nested:
                    yield f


@ts_interface()
class TextChoicesSerializer(Serializer):
    """
    A serializer class for django.models.TextChoices.

    (Which inherit from enum.Enum)
    """

    class Meta:
        abstract = True

    name = CharField()
    value = CharField()

    def to_internal_value(self, data):
        return getattr(self.Meta.enum_cls, data["name"])

    def to_representation(self, instance):
        enum_element = getattr(self.Meta.enum_cls, instance, instance)
        return super().to_representation(enum_element)


class CaseStepStateSerializer(TextChoicesSerializer):
    class Meta:
        enum_cls = CaseStepState


@ts_interface()
class CountrySerializer(BaseModelSerializer):
    class Meta:
        model = Country
        fields = ["uuid", "name", "code", "unicode_flag"]


@ts_interface()
class ServiceSerializer(BaseModelSerializer):
    class Meta:
        model = Service
        fields = ["uuid", "name"]


@ts_interface()
class RouteSerializer(BaseModelSerializer):
    host_country = CountrySerializer()

    class Meta:
        model = Route
        fields = ["uuid", "name", "host_country"]


@ts_interface()
class ProcessStepSerializer(BaseModelSerializer):
    # See module docstring for explanation of read_only and allow_null
    uuid = UUIDField(read_only=False, allow_null=True, required=False)
    service = ServiceSerializer()

    class Meta:
        model = ProcessStep
        fields = ["uuid", "sequence_number", "service"]
        ordering = ["sequence_number"]


@ts_interface()
class ProcessSerializer(BaseModelSerializer):
    # See module docstring for explanation of read_only and allow_null
    uuid = UUIDField(read_only=False, allow_null=True, required=False)
    route = RouteSerializer()
    nationality = CountrySerializer()
    home_country = CountrySerializer(allow_null=True, required=False)
    steps = ProcessStepSerializer(many=True)

    class Meta:
        model = Process
        fields = ["uuid", "route", "nationality", "home_country", "steps"]


@ts_interface()
class ActionSerializer(Serializer):
    display_name = CharField()
    name = CharField()
    url = URLField()


@ts_interface()
class UserSerializer(BaseModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["uuid", "first_name", "last_name", "email"]
        depth = 2


@ts_interface()
class StoredFileSerializer(BaseModelSerializer):
    created_by = UserSerializer()

    class Meta:
        model = StoredFile
        fields = ["created_by", "uuid", "media_type", "name", "size"]


@ts_interface()
class ClientSerializer(BaseModelSerializer):
    class Meta:
        model = Client
        fields = ["uuid", "name"]


@ts_interface()
class ApplicantSerializer(CountryFieldMixin, BaseModelSerializer):
    # See module docstring for explanation of read_only and allow_null
    uuid = UUIDField(read_only=False, allow_null=True, required=False)
    user = UserSerializer()
    employer = ClientSerializer()
    home_country = CountrySerializer()
    nationalities = CountrySerializer(many=True)

    class Meta:
        model = Applicant
        fields = ["uuid", "user", "employer", "home_country", "nationalities"]


@ts_interface()
class ClientContactSerializer(CountryFieldMixin, BaseModelSerializer):
    user = UserSerializer()
    client = ClientSerializer()

    class Meta:
        model = ClientContact
        fields = ["uuid", "user", "client"]


@ts_interface()
class ProviderSerializer(BaseModelSerializer):
    class Meta:
        model = Provider
        fields = ["uuid", "logo_url", "name"]


@ts_interface()
class ClientProviderRelationshipSerializer(BaseModelSerializer):
    # See module docstring for explanation of read_only and allow_null
    uuid = UUIDField(read_only=False, allow_null=True, required=False)
    client = ClientSerializer()
    provider = ProviderSerializer()

    class Meta:
        model = ClientProviderRelationship
        fields = ["uuid", "client", "provider", "preferred"]


@ts_interface()
class ProviderContactSerializer(CountryFieldMixin, BaseModelSerializer):
    # See module docstring for explanation of read_only and allow_null
    uuid = UUIDField(read_only=False, allow_null=True, required=False)
    user = UserSerializer()
    provider = ProviderSerializer()

    class Meta:
        model = ProviderContact
        fields = ["uuid", "user", "provider"]


@ts_interface()
class CaseStepContractSerializer(BaseModelSerializer):
    # The case FK will never be null, but we have to set required=False here
    # because we sometimes validate the data before creating a
    # case-with-its-case-steps-and-contracts in one go.
    case_step_uuid = CharField(source="case_step.uuid", required=False)
    provider_contact = ProviderContactSerializer()
    # TODO: cannot serialize case_step due to cycle in foreign key dependency graph

    class Meta:
        model = CaseStepContract

        fields = ["case_step_uuid", "provider_contact", "accepted_at", "rejected_at"]


@ts_interface()
class CaseStepSerializer(BaseModelSerializer):
    actions = ActionSerializer(many=True, source="get_actions")
    active_contract = CaseStepContractSerializer()
    process_step = ProcessStepSerializer()
    state = CaseStepStateSerializer()
    stored_files = StoredFileSerializer(many=True)

    class Meta:
        model = CaseStep
        fields = [
            "actions",
            "active_contract",
            "uuid",
            "process_step",
            "sequence_number",
            "state",
            "stored_files",
        ]
        ordering = ["sequence_number"]


@ts_interface()
class CaseSerializer(BaseModelSerializer):
    applicant = ApplicantSerializer()
    process = ProcessSerializer()
    steps = CaseStepSerializer(many=True)

    class Meta:
        model = Case
        fields = [
            "uuid",
            "applicant",
            "process",
            "steps",
            "created_at",
            "target_entry_date",
            "target_exit_date",
        ]

    @classmethod
    def get_queryset_for_client_contact_case_list_view(
        cls, client_contact: ClientContact
    ) -> QuerySet[Case]:
        return client_contact.cases().select_related(*cls.get_select_related_fields())

    @atomic
    def create_for_client_contact(self, client_contact: ClientContact) -> Case:
        applicant_data = self.validated_data.pop("applicant")
        process_data = self.validated_data.pop("process")
        case_steps_data = self.validated_data.pop("steps")
        case = Case.objects.create(
            client_contact=client_contact,
            applicant=Applicant.objects.get(uuid=applicant_data["uuid"]),
            process_uuid=process_data["uuid"],
            **self.validated_data,
        )
        for case_step_data in case_steps_data:
            case_step = case.casestep_set.create(
                process_step_uuid=case_step_data["process_step"]["uuid"],
                sequence_number=case_step_data["sequence_number"],
            )
            provider_contact = ProviderContact.objects.get(
                uuid=case_step_data["active_contract"]["provider_contact"]["uuid"]
            )
            case_step.earmark(provider_contact)
            case_step.save()

        return case
