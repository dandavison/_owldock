from django.contrib import admin
from django.db.models import QuerySet
from django.forms import ModelForm, ModelChoiceField
from django.http import HttpRequest
from nested_admin import (
    NestedStackedInline,
    NestedTabularInline,
    NestedModelAdmin,
)

from app.models.bloc import Bloc
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
    required_only_if_nationalities_bloc = ModelChoiceField(
        Bloc.objects.all(),
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


class ProcessRuleSetStepInline(NestedStackedInline):
    model = ProcessRuleSetStep
    sortable_field_name = "sequence_number"
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Filter inline dropdowns part II.
        #
        # Pass filtered queryset to inline form constructors. It seems that
        # there's a case for Django providing an API for this. See
        # ProcessRuleSetAdmin.get_inline_instances for part I, and
        # https://stackoverflow.com/questions/9422735/accessing-parent-model-instance-from-modelform-of-admin-inline
        # https://groups.google.com/g/django-developers/c/10GP72w4aZs
        if db_field.name == "process_step":
            kwargs["queryset"] = (
                ProcessStep.objects.filter(
                    host_country=self._parent_obj.route.host_country
                )
                .select_related("host_country")
                .order_by("name")
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ProcessRuleSetAdminForm(BlocChoiceFieldMixin, ModelForm):
    nationalities_bloc = ModelChoiceField(
        Bloc.objects.all(),
        required=False,
    )
    home_countries_bloc = ModelChoiceField(
        Bloc.objects.all(),
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

    def get_inline_instances(self, request, obj=None):
        # Filter inline dropdowns part I.
        # Stash parent model instance on inline admin instances, so that they
        # can make it available to their forms, so that dropdown querysets can
        # depend on the parent model instance. It seems that there's a case for
        # Django providing an API for this. See
        # ProcessRuleSetStepInline.formfield_for_foreignkey above for part II,
        # and
        # https://stackoverflow.com/questions/9422735/accessing-parent-model-instance-from-modelform-of-admin-inline
        # https://groups.google.com/g/django-developers/c/10GP72w4aZs
        inlines = super().get_inline_instances(request, obj)
        for inline in inlines:
            inline._parent_obj = obj
        return inlines
