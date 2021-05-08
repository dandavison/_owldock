from django.contrib import admin
from django.db.models import QuerySet
from django.forms import ModelForm, ChoiceField
from django.http import HttpRequest
from nested_admin import (
    NestedStackedInline,
    NestedTabularInline,
    NestedModelAdmin,
)

from app.models.bloc import Blocs
from immigration.admin.bloc_choice_field import BlocChoiceFieldMixin  # type: ignore
from immigration.models import (
    IssuedDocument,
    IssuedDocumentType,
    ProcessRuleSet,
    ProcessRuleSetStep,
    ProcessStep,
    Route,
    ServiceItem,
)


class IssuedDocumentInline(NestedTabularInline):
    model = IssuedDocument
    extra = 1


class ServiceItemInline(NestedTabularInline):
    model = ServiceItem
    extra = 1


class ProcessStepAdminForm(BlocChoiceFieldMixin, ModelForm):
    required_only_if_nationalities_bloc = ChoiceField(
        choices=Blocs.choices() + [("", "")],
        required=False,
    )

    _bloc_fields = [
        ("required_only_if_nationalities", "required_only_if_nationalities_bloc"),
    ]


@admin.register(ProcessStep)
class ProcessStepAdmin(NestedModelAdmin):
    form = ProcessStepAdminForm
    filter_horizontal = ["required_only_if_nationalities"]
    extra = 0
    inlines = [IssuedDocumentInline, ServiceItemInline]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "host_country",
                    "government_fee",
                    "estimated_min_duration_days",
                    "estimated_max_duration_days",
                    "applicant_can_enter_host_country_after",
                    "applicant_can_work_in_host_country_after",
                    "required_only_if_payroll_location",
                    "required_only_if_duration_exceeds",
                ]
            },
        ),
        (
            None,
            {
                "fields": [
                    "required_only_if_nationalities_bloc",
                    "required_only_if_nationalities",
                ],
            },
        ),
    ]

    def get_queryset(self, request: HttpRequest) -> QuerySet[ProcessStep]:
        return (
            super()
            .get_queryset(request)
            .select_related(
                "host_country",
            )
            .order_by("host_country__name")
        )


@admin.register(IssuedDocumentType)
class IssuedDocumentTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["id"]
    list_editable = ["name"]


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "host_country"]
    list_display_links = ["id"]
    list_editable = ["name", "host_country"]


class ProcessRuleSetStepAdminForm(ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.instance.process_ruleset_id:
            self.fields["process_step"].queryset = ProcessStep.objects.filter(
                host_country=self.instance.process_ruleset.route.host_country
            ).order_by("name")
        else:
            # New, in-memory instance without FKs
            # TODO
            pass


class ProcessRuleSetStepInline(NestedStackedInline):
    model = ProcessRuleSetStep
    form = ProcessRuleSetStepAdminForm
    sortable_field_name = "sequence_number"
    extra = 0


class ProcessRuleSetAdminForm(BlocChoiceFieldMixin, ModelForm):
    nationalities_bloc = ChoiceField(
        choices=Blocs.choices() + [("", "")],
        required=False,
    )
    home_countries_bloc = ChoiceField(
        choices=Blocs.choices() + [("", "")],
        required=False,
    )

    _bloc_fields = [
        ("nationalities", "nationalities_bloc"),
        ("home_countries", "home_countries_bloc"),
    ]


@admin.register(ProcessRuleSet)
class ProcessRuleSetAdmin(NestedModelAdmin):
    form = ProcessRuleSetAdminForm
    list_display = ["route"]
    filter_horizontal = ["nationalities", "home_countries"]
    inlines = [ProcessRuleSetStepInline]
    fieldsets = [
        (None, {"fields": ["route"]}),
        (
            None,
            {
                "fields": ["nationalities_bloc", "nationalities"],
            },
        ),
        (
            None,
            {
                "fields": ["home_countries_bloc", "home_countries"],
            },
        ),
        (
            None,
            {
                "fields": [
                    "contract_location",
                    "payroll_location",
                    "minimum_salary",
                    "duration_min_days",
                    "duration_max_days",
                    "intra_company_moves_only",
                ]
            },
        ),
    ]

    def get_queryset(self, request: HttpRequest) -> QuerySet[ProcessRuleSet]:
        # FIXME: Prevent issuing many queries for host_country
        return (
            super()
            .get_queryset(request)
            .prefetch_related("process_steps__host_country")
            .prefetch_related("processrulesetstep_set__process_step__host_country")
            .order_by("route__host_country__name")
        )
