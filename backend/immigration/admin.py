from django.contrib import admin
from nested_inline.admin import (
    NestedStackedInline,
    NestedTabularInline,
    NestedModelAdmin,
)

from immigration.models import (
    IssuedDocument,
    IssuedDocumentType,
    Process,
    ProcessStep,
)


class IssuedDocumentInline(NestedTabularInline):
    model = IssuedDocument
    extra = 1


class ProcessStepInline(NestedStackedInline):
    model = ProcessStep
    filter_horizontal = ["required_only_if_nationalities"]
    extra = 1
    inlines = [IssuedDocumentInline]


@admin.register(IssuedDocumentType)
class IssuedDocumentTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["id"]
    list_editable = ["name"]


@admin.register(Process)
class ProcessAdmin(NestedModelAdmin):
    list_display = ["name", "host_country"]
    filter_horizontal = ["nationalities", "home_countries"]
    inlines = [ProcessStepInline]

    if False:
        # DNW:
        search_fields = ["host_country__name"]
        autocomplete_fields = ["host_country"]
