from django.contrib import admin
from nested_admin import (
    NestedStackedInline,
    NestedTabularInline,
    NestedModelAdmin,
)

from immigration.models import (
    IssuedDocument,
    IssuedDocumentType,
    ProcessRuleSet,
    ProcessStep,
    Route,
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


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "host_country"]
    list_display_links = ["id"]
    list_editable = ["name", "host_country"]


@admin.register(ProcessRuleSet)
class ProcessRuleSetAdmin(NestedModelAdmin):
    list_display = ["route"]
    filter_horizontal = ["nationalities", "home_countries"]
    inlines = [ProcessStepInline]
