from django.contrib import admin

from immigration.models import (
    IssuedDocument,
    IssuedDocumentType,
    Process,
    ProcessStep,
)


class ProcessStepInline(admin.TabularInline):
    model = ProcessStep
    filter_horizontal = ["required_only_if_nationalities"]


class IssuedDocumentInline(admin.TabularInline):
    model = IssuedDocument


@admin.register(IssuedDocumentType)
class IssuedDocumentTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["id"]
    list_editable = ["name"]


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = ["name", "host_country"]
    filter_horizontal = ["nationalities", "home_countries", "issued_documents"]
    inlines = [ProcessStepInline, IssuedDocumentInline]

    if False:
        # DNW:
        search_fields = ["host_country__name"]
        autocomplete_fields = ["host_country"]
