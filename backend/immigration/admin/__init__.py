from django.contrib import admin
from django.db.models import QuerySet
from django.forms import ModelForm
from django.http import HttpRequest
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
    required_only_if_home_country_bloc = BlocChoiceFieldMixin.make_bloc_field()
    required_only_if_home_country_bloc_include = (
        BlocChoiceFieldMixin.make_bloc_include_field()
    )

    _bloc_fields = ["required_only_if_nationalities", "required_only_if_home_country"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["depends_on"].queryset = ProcessStep.objects.filter(
            host_country=self.instance.host_country
        ).order_by("name")


@admin.register(ProcessStep)
class ProcessStepAdmin(HasInlinesNestedModelAdmin):
    form = ProcessStepAdminForm
    filter_horizontal = [
        "required_only_if_nationalities",
        "required_only_if_home_country",
        "depends_on",
    ]
    extra = 0
    inlines = [ProcessStepIssuedDocumentInline, ServiceItemInline]
    list_display = [
        "name",
        "host_country",
        "government_fee",
        "estimated_min_duration_days",
        "estimated_max_duration_days",
        "applicant_can_enter_host_country_on",
        "applicant_can_work_in_host_country_on",
        "required_only_if_contract_location",
        "required_only_if_payroll_location",
        "required_only_if_duration_greater_than",
        "required_only_if_duration_less_than",
        "issued_documents_count",
    ]
    list_editable = [
        "estimated_min_duration_days",
        "estimated_max_duration_days",
    ]
    list_filter = ["host_country"]
    ordering = ["host_country", "name"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "host_country",
                ]
            },
        ),
        (
            None,
            {
                "fields": [
                    "estimated_min_duration_days",
                    "estimated_max_duration_days",
                    "government_fee",
                ]
            },
        ),
        (
            None,
            {
                "fields": [
                    "applicant_can_enter_host_country_on",
                    "applicant_can_work_in_host_country_on",
                ]
            },
        ),
        (
            None,
            {
                "fields": [
                    "required_only_if_contract_location",
                    "required_only_if_payroll_location",
                ]
            },
        ),
        (
            None,
            {
                "fields": [
                    "required_only_if_duration_greater_than",
                    "required_only_if_duration_less_than",
                ]
            },
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
        (
            None,
            {
                "fields": [
                    "required_only_if_home_country_bloc",
                    "required_only_if_home_country_bloc_include",
                    "required_only_if_home_country",
                ],
            },
        ),
        (
            None,
            {
                "fields": ["depends_on"],
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


class IssuedDocumentAdminForm(BlocChoiceFieldMixin, ModelForm):
    proves_right_to_travel_in_bloc = BlocChoiceFieldMixin.make_bloc_field()
    proves_right_to_travel_in_bloc_include = (
        BlocChoiceFieldMixin.make_bloc_include_field()
    )

    _bloc_fields = ["proves_right_to_travel_in"]


@admin.register(IssuedDocument)
class IssuedDocumentAdmin(admin.ModelAdmin):
    form = IssuedDocumentAdminForm
    list_display = [
        "name",
        "host_country",
        "proves_right_to_enter",
        "proves_right_to_reside",
        "proves_right_to_work",
        "proves_right_to_travel_in_count",
        "process_steps_count",
    ]
    list_filter = ["host_country"]
    ordering = ["host_country", "name"]
    _fields = [
        "name",
        "host_country",
        "proves_right_to_enter",
        "proves_right_to_reside",
        "proves_right_to_work",
    ]
    inlines = [ProcessStepIssuedDocumentInline]
    filter_horizontal = ["proves_right_to_travel_in"]
    fieldsets = [
        (
            None,
            {"fields": _fields},
        ),
        (
            None,
            {
                "fields": [
                    "proves_right_to_travel_in_bloc",
                    "proves_right_to_travel_in_bloc_include",
                    "proves_right_to_travel_in",
                ],
            },
        ),
    ]

    @admin.display(description="Proves right to travel in")
    def proves_right_to_travel_in_count(self, obj: IssuedDocument) -> int:
        return len(obj.proves_right_to_travel_in.all())

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
            .prefetch_related("processstep_set", "proves_right_to_travel_in")
            .order_by("host_country__name")
        )


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ["name", "host_country", "processruleset"]


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
        "data_entry_status",
        "route",
        "available_to_nationalities",
        "available_to_home_countries",
        "contract_location",
        "payroll_location",
        "duration_min_days",
        "duration_max_days",
        "process_ruleset_steps_count",
    ]
    list_display_links = ["route"]
    list_filter = ["route__host_country", "data_entry_status"]
    filter_horizontal = ["nationalities", "home_countries"]
    inlines = [ProcessRuleSetStepInline]
    readonly_fields = ["steps_summary", "steps_gantt"]
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
                    "steps_summary",
                    "steps_gantt",
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
    def steps_summary(self, obj: ProcessRuleSet) -> str:
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
            issued_documents = prss.process_step.issued_documents.all()
            if issued_documents:
                for id in issued_documents:
                    html += "<tr>"
                    if first:
                        html += (
                            f"<td>{prss.sequence_number}. {prss.process_step.name}</td>"
                        )
                        first = False
                    else:
                        html += "<td></td>"
                    html += f"<td style='padding-left: 10px;'>{id.name}</td>"
                    html += "</tr>"
            else:
                html += "<tr>"
                html += f"<td>{prss.sequence_number}. {prss.process_step.name}</td>"
                html += "<td></td>"
                html += "</tr>"

        html += "</tbody></table>"
        return mark_safe(html)

    @admin.display(description="Gantt chart")
    def steps_gantt(self, obj: ProcessRuleSet) -> str:
        return mark_safe(
            f"<iframe src='/portal/process/{obj.id}/steps/' style='height: 500px; width: 1000px'></iframe>"
        )

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
        return (
            super()
            .get_queryset(request)
            .prefetch_related("home_countries", "nationalities", "process_steps")
            .order_by("route__host_country__name")
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "route":
            kwargs["queryset"] = Route.objects.select_related("host_country").order_by(
                "host_country__name", "name"
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
