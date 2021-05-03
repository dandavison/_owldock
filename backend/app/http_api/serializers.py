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
import logging
from collections import defaultdict
from operator import attrgetter
from typing import List, Union

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import Prefetch, QuerySet
from django.db.transaction import atomic
from django_countries.serializers import CountryFieldMixin
from django_typomatic import ts_interface
from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    IntegerField,
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
)
from client.models.case_step import (
    CaseStep,
    CaseStepContract,
)


logger = logging.getLogger(__file__)


@ts_interface()
class EnumSerializer(Serializer):
    name = CharField()
    value = CharField()


@ts_interface()
class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ["uuid", "name", "code", "unicode_flag"]


@ts_interface()
class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = ["uuid", "name"]


@ts_interface()
class RouteSerializer(ModelSerializer):
    host_country = CountrySerializer()

    class Meta:
        model = Route
        fields = ["uuid", "name", "host_country"]


@ts_interface()
class ProcessStepSerializer(ModelSerializer):
    # See module docstring for explanation of read_only and allow_null
    uuid = UUIDField(read_only=False, allow_null=True, required=False)
    service = ServiceSerializer()

    class Meta:
        model = ProcessStep
        fields = ["uuid", "sequence_number", "service"]
        ordering = ["sequence_number"]


@ts_interface()
class ProcessSerializer(ModelSerializer):
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
class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["uuid", "first_name", "last_name", "email"]
        depth = 2


@ts_interface()
class StoredFileSerializer(ModelSerializer):
    created_by = UserSerializer()

    class Meta:
        model = StoredFile
        fields = ["created_by", "uuid", "media_type", "name", "size"]


@ts_interface()
class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ["uuid", "name"]


@ts_interface()
class ApplicantSerializer(CountryFieldMixin, ModelSerializer):
    # See module docstring for explanation of read_only and allow_null
    id = IntegerField(read_only=False, allow_null=True, required=False, min_value=1)
    uuid = UUIDField(read_only=False, allow_null=True, required=False)
    user = UserSerializer()
    employer = ClientSerializer()
    home_country = CountrySerializer()
    nationalities = CountrySerializer(many=True)

    class Meta:
        model = Applicant
        fields = ["id", "uuid", "user", "employer", "home_country", "nationalities"]


@ts_interface()
class ClientContactSerializer(CountryFieldMixin, ModelSerializer):
    user = UserSerializer()
    client = ClientSerializer()

    class Meta:
        model = ClientContact
        fields = ["uuid", "user", "client"]


@ts_interface()
class ProviderSerializer(ModelSerializer):
    class Meta:
        model = Provider
        fields = ["uuid", "logo_url", "name"]


@ts_interface()
class ClientProviderRelationshipSerializer(ModelSerializer):
    # See module docstring for explanation of read_only and allow_null
    uuid = UUIDField(read_only=False, allow_null=True, required=False)
    client = ClientSerializer()
    provider = ProviderSerializer()

    class Meta:
        model = ClientProviderRelationship
        fields = ["uuid", "client", "provider", "preferred"]


@ts_interface()
class ProviderContactSerializer(CountryFieldMixin, ModelSerializer):
    # See module docstring for explanation of read_only and allow_null
    uuid = UUIDField(read_only=False, allow_null=True, required=False)
    user = UserSerializer()
    provider = ProviderSerializer()

    class Meta:
        model = ProviderContact
        fields = ["uuid", "user", "provider"]


@ts_interface()
class CaseStepContractSerializer(ModelSerializer):
    # See module docstring for explanation of read_only and allow_null
    id = IntegerField(read_only=False, allow_null=True, required=False, min_value=1)
    # The case FK will never be null, but we have to set required=False here
    # because we sometimes validate the data before creating a
    # case-with-its-case-steps-and-contracts in one go.
    case_step_uuid = CharField(source="case_step.uuid", required=False)
    provider_contact = ProviderContactSerializer()
    # TODO: cannot serialize case_step due to cycle in foreign key dependency graph

    class Meta:
        model = CaseStepContract
        fields = [
            "id",
            "case_step_uuid",
            "provider_contact",
            "accepted_at",
            "rejected_at",
        ]


@ts_interface()
class CaseStepSerializer(ModelSerializer):
    # See module docstring for explanation of read_only and allow_null
    uuid = UUIDField(read_only=False, allow_null=True, required=False)
    actions = ActionSerializer(many=True, source="get_actions")
    active_contract = CaseStepContractSerializer()
    process_step = ProcessStepSerializer()
    state = EnumSerializer()
    stored_files = StoredFileSerializer(many=True)

    class Meta:
        model = CaseStep
        fields = [
            "uuid",
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
class CaseSerializer(ModelSerializer):
    # See module docstring for explanation of read_only and allow_null
    uuid = UUIDField(read_only=False, allow_null=True, required=False)
    applicant = ApplicantSerializer()
    process = ProcessSerializer()
    steps = CaseStepSerializer(many=True)

    class Meta:
        model = Case
        fields = [
            "id",
            "uuid",
            "applicant",
            "process",
            "steps",
            "created_at",
            "target_entry_date",
            "target_exit_date",
        ]

    @classmethod
    def get_cases_for_client_or_provider_contact(
        cls, client_or_provider_contact: Union[ClientContact, ProviderContact]
    ) -> List[Case]:
        return cls.prefetch_cases(
            client_or_provider_contact.cases(), client_or_provider_contact
        )

    @classmethod
    def prefetch_cases(
        cls,
        cases: QuerySet[Case],
        client_or_provider_contact: Union[ClientContact, ProviderContact],
    ) -> List[Case]:

        # Cache along lineages rooted at Case, in the client DB.
        _cases = list(
            cases.prefetch_related(
                "applicant__applicantnationality_set",
                Prefetch(
                    "steps",
                    queryset=(
                        client_or_provider_contact.case_steps().select_related(
                            "active_contract__case_step"
                        )
                    ),
                ),
            )
            .select_related(
                "applicant__employer",
            )
            .order_by("-created_at")
        )
        cls._cache_prefetched_data_on_case_objects(_cases)
        return _cases

    @classmethod
    def _cache_prefetched_data_on_case_objects(cls, cases: List[Case]) -> None:
        # Fetch processes in default DB
        process_uuids = {c.process_uuid for c in cases}
        processes = (
            Process.objects.filter(uuid__in=process_uuids)
            .select_related(
                "route__host_country",
                "nationality",
                "home_country",
            )
            .prefetch_related("steps__service")
        )
        uuid2process = {p.uuid: p for p in processes}
        uuid2process_step = {s.uuid: s for p in processes for s in p.steps.all()}

        # Fetch stored files in default DB
        case_step_uuids = {s.uuid for c in cases for s in c.steps.all()}
        stored_files = StoredFile.objects.filter(
            associated_object_uuid__in=case_step_uuids,
            associated_object_content_type=ContentType.objects.get_for_model(CaseStep),
        ).select_related("created_by")
        case_step_uuid2stored_files = defaultdict(set)
        for f in stored_files:
            case_step_uuid2stored_files[f.associated_object_uuid].add(f)

        # Fetch provider contacts in default DB
        provider_contact_uuids = {
            s.active_contract.provider_contact_uuid
            for c in cases
            for s in c.steps.all()
            if s.active_contract
        }
        uuid2provider_contact = {
            pc.uuid: pc
            for pc in ProviderContact.objects.filter(
                uuid__in=provider_contact_uuids
            ).select_related("user", "provider")
        }

        # Fetch countries in default DB
        applicant_country_uuids = set()
        applicant_user_uuids = set()
        applicant_uuid2nationality_uuids = defaultdict(set)
        for c in cases:
            a = c.applicant
            applicant_country_uuids.add(a.home_country_uuid)
            applicant_user_uuids.add(a.user_uuid)
            for an in a.applicantnationality_set.all():
                applicant_country_uuids.add(an.country_uuid)
                applicant_uuid2nationality_uuids[a.uuid].add(an.country_uuid)
        uuid2country = {
            c.uuid: c for c in Country.objects.filter(uuid__in=applicant_country_uuids)
        }
        uuid2user = {
            u.uuid: u
            for u in get_user_model().objects.filter(uuid__in=applicant_user_uuids)
        }

        # Attach objects from the default DB to the instances generated by the
        # queries in the client DB.
        for c in cases:
            setattr(c, "process", uuid2process[c.process_uuid])
            for s in c.steps.all():
                setattr(s, "process_step", uuid2process_step[s.process_step_uuid])
                setattr(
                    s,
                    "_prefetched_stored_files",
                    sorted(case_step_uuid2stored_files[s.uuid], key=attrgetter("name")),
                )
                if s.active_contract:
                    setattr(
                        s.active_contract,
                        "provider_contact",
                        uuid2provider_contact[s.active_contract.provider_contact_uuid],
                    )
            a = c.applicant
            setattr(a, "home_country", uuid2country[a.home_country_uuid])
            setattr(
                a,
                "_prefetched_nationalities",
                sorted(
                    (
                        uuid2country[uuid]
                        for uuid in applicant_uuid2nationality_uuids[a.uuid]
                    ),
                    key=attrgetter("name"),
                ),
            )
            setattr(a, "user", uuid2user[a.user_uuid])

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
            case_step = case.steps.create(
                process_step_uuid=case_step_data["process_step"]["uuid"],
                sequence_number=case_step_data["sequence_number"],
            )
            provider_contact = ProviderContact.objects.get(
                uuid=case_step_data["active_contract"]["provider_contact"]["uuid"]
            )
            case_step.earmark(provider_contact)
            case_step.save()

        return case
