from django.contrib import admin
from django.db.models import QuerySet
from django.forms import ModelForm
from django.http import HttpRequest
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from nested_admin import (
    NestedStackedInline,
    NestedTabularInline,
    NestedModelAdmin,
)

from app.models import Bloc
from immigration.admin.bloc_choice_field import BlocChoiceFieldMixin  # type: ignore
from immigration.models import (
    IssuedDocument,
    ProcessRuleSet,
    ProcessRuleSetStep,
    ProcessStep,
    Route,
    ServiceItem,
)


class HasInlinesNestedModelAdmin(NestedModelAdmin):
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

    # For the second part of this, see the implementations of
    # formfield_for_foreignkey on Inline classes below, to which the following
    # comment applies:
    # Filter inline dropdowns part II.
    #
    # Pass filtered queryset to inline form constructors. It seems that
    # there's a case for Django providing an API for this. See
    # ProcessRuleSetAdmin.get_inline_instances for part I, and
    # https://stackoverflow.com/questions/9422735/accessing-parent-model-instance-from-modelform-of-admin-inline
    # https://groups.google.com/g/django-developers/c/10GP72w4aZs


class ProcessStepIssuedDocumentInline(NestedTabularInline):
    model = ProcessStep.issued_documents.through
    extra = 0
    readonly_fields = ["processstep"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # See HasInlinesNestedModelAdmin
        if getattr(self, "_parent_obj", None) and db_field.name == "issueddocument":
            kwargs["queryset"] = IssuedDocument.objects.filter(
                host_country=self._parent_obj.host_country
            ).order_by("name")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ServiceItemInline(NestedTabularInline):
    model = ServiceItem
    extra = 0


class ProcessStepAdminForm(BlocChoiceFieldMixin, ModelForm):
    required_only_if_nationalities_bloc = BlocChoiceFieldMixin.make_bloc_field()
    required_only_if_nationalities_bloc_include = (
        BlocChoiceFieldMixin.make_bloc_include_field()
    )

    _bloc_fields = ["required_only_if_nationalities"]


@admin.register(ProcessStep)
class ProcessStepAdmin(HasInlinesNestedModelAdmin):
    form = ProcessStepAdminForm
    filter_horizontal = ["required_only_if_nationalities"]
    extra = 0
    inlines = [ProcessStepIssuedDocumentInline, ServiceItemInline]
    _fields = [
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
    list_display = _fields + ["issued_documents_count"]
    list_filter = ["host_country"]
    ordering = ["host_country", "name"]
    fieldsets = [
        (
            None,
            {"fields": _fields},
        ),
        (
            None,
            {
                "fields": [
                    "required_only_if_nationalities_bloc",
                    "required_only_if_nationalities_bloc_include",
                    "required_only_if_nationalities",
                ],
            },
        ),
    ]

    @admin.display(description="Issued documents")
    def issued_documents_count(self, obj: ProcessStep) -> int:
        return len(obj.issued_documents.all())

    def get_queryset(self, request: HttpRequest) -> QuerySet[ProcessStep]:
        return (
            super()
            .get_queryset(request)
            .select_related(
                "host_country",
            )
            .prefetch_related("issued_documents")
            .order_by("host_country__name")
        )


@admin.register(IssuedDocument)
class IssuedDocumentAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "host_country",
        "proves_right_to_enter",
        "proves_right_to_reside",
        "proves_right_to_work",
        "process_steps_count",
    ]
    list_filter = ["host_country"]
    ordering = ["host_country", "name"]
    fields = [
        "name",
        "host_country",
        "proves_right_to_enter",
        "proves_right_to_reside",
        "proves_right_to_work",
    ]
    inlines = [ProcessStepIssuedDocumentInline]

    @admin.display(description="Process steps")
    def process_steps_count(self, obj: IssuedDocument) -> int:
        return len(obj.processstep_set.all())

    def get_queryset(self, request: HttpRequest) -> QuerySet[IssuedDocument]:
        return (
            super()
            .get_queryset(request)
            .select_related(
                "host_country",
            )
            .prefetch_related("processstep_set")
            .order_by("host_country__name")
        )


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "host_country"]
    list_display_links = ["id"]
    list_editable = ["name", "host_country"]


class ProcessRuleSetStepInline(NestedStackedInline):
    model = ProcessRuleSetStep
    sortable_field_name = "sequence_number"
    ordering = ["sequence_number"]
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # See HasInlinesNestedModelAdmin
        if getattr(self, "_parent_obj", None) and db_field.name == "process_step":
            kwargs["queryset"] = (
                ProcessStep.objects.filter(
                    host_country=self._parent_obj.route.host_country
                )
                .select_related("host_country")
                .order_by("name")
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ProcessRuleSetAdminForm(BlocChoiceFieldMixin, ModelForm):
    nationalities_bloc = BlocChoiceFieldMixin.make_bloc_field()
    nationalities_bloc_include = BlocChoiceFieldMixin.make_bloc_include_field()
    home_countries_bloc = BlocChoiceFieldMixin.make_bloc_field()
    home_countries_bloc_include = BlocChoiceFieldMixin.make_bloc_include_field()

    _bloc_fields = ["nationalities", "home_countries"]


@admin.register(ProcessRuleSet)
class ProcessRuleSetAdmin(HasInlinesNestedModelAdmin):
    form = ProcessRuleSetAdminForm
    list_display = [
        "route",
        "host_country",
        "available_to_nationalities",
        "available_to_home_countries",
        "contract_location",
        "payroll_location",
        "duration_min_days",
        "duration_max_days",
        "data_entry_status",
        "process_ruleset_steps_count",
    ]
    list_filter = ["route__host_country", "data_entry_status"]
    filter_horizontal = ["nationalities", "home_countries"]
    inlines = [ProcessRuleSetStepInline]
    readonly_fields = ["step_summary"]
    fieldsets = [
        (None, {"fields": ["route"]}),
        (
            None,
            {
                "fields": [
                    "nationalities_bloc",
                    "nationalities_bloc_include",
                    "nationalities",
                ],
            },
        ),
        (
            None,
            {
                "fields": [
                    "home_countries_bloc",
                    "home_countries_bloc_include",
                    "home_countries",
                ],
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
                    "step_summary",
                ]
            },
        ),
        (
            None,
            {
                "fields": [
                    "data_entry_status",
                ]
            },
        ),
    ]

    def get_sortable_by(self, request: HttpRequest):
        # This is a pretty random choice of method to use for the purpose, but
        # we need to recompute this on each request; __init__ is called once at
        # server start time.
        self.get_bloc_description_from_countries = (
            Bloc.objects.make_get_description_from_countries()
        )
        return super().get_sortable_by(request)

    @admin.display(description="Steps summary")
    def step_summary(self, obj: ProcessRuleSet) -> str:
        html = "<table><tbody>"
        html += (
            "<thead><tr>"
            "<th style='font-weight: bold'>Step</th>"
            "<th style='font-weight: bold; padding-left: 10px;'>Issued Document</th>"
            "</tr></thead>"
        )
        html += "<tr></tr>"
        for prss in (
            obj.process_steps.through.objects.filter(process_ruleset=obj)
            .prefetch_related("process_step__issued_documents")
            .order_by("sequence_number")
        ):
            first = True
            for id in prss.process_step.issued_documents.all():
                html += "<tr>"
                if first:
                    html += f"<td>{prss.sequence_number}. {prss.process_step.name}</td>"
                    first = False
                else:
                    html += "<td></td>"
                html += f"<td style='padding-left: 10px;'>{id.name}</td>"
                html += "</tr>"
        html += "</tbody></table>"
        return mark_safe(html)

    @admin.display(description="Process steps")
    def process_ruleset_steps_count(self, obj: ProcessRuleSet) -> int:
        return len(obj.processrulesetstep_set.all())

    @admin.display(description="Host country")
    def host_country(self, obj: ProcessRuleSet) -> str:
        return obj.route.host_country.name

    @admin.display(description="Available to nationalities")
    def available_to_nationalities(self, obj: ProcessRuleSet) -> str:
        nationalities = set(obj.nationalities.all())
        if not nationalities:
            return "any"
        else:
            return self.get_bloc_description_from_countries(nationalities)

    @admin.display(description="Available to home countries")
    def available_to_home_countries(self, obj: ProcessRuleSet) -> str:
        home_countries = set(obj.home_countries.all())
        if not home_countries:
            return "any"
        else:
            return self.get_bloc_description_from_countries(home_countries)

    def get_queryset(self, request: HttpRequest) -> QuerySet[ProcessRuleSet]:
        # FIXME: Prevent issuing many queries for host_country
        return (
            super()
            .get_queryset(request)
            .prefetch_related("process_steps__host_country")
            .prefetch_related("processrulesetstep_set__process_step__host_country")
            .order_by("route__host_country__name")
        )
