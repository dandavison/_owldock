from django.contrib import admin
from django.db import models as django_orm_models
from django.forms import ModelForm
from django.http import HttpRequest
from martor.widgets import AdminMartorWidget

from app.models import (
    Bloc,
    Country,
    Provider,
    ProviderContact,
    StoredFile,
)
from immigration.admin.bloc_choice_field import BlocChoiceFieldMixin  # type: ignore


admin.site.register(Provider)
admin.site.register(ProviderContact)
admin.site.register(StoredFile)


class BlocAdminForm(BlocChoiceFieldMixin, ModelForm):
    countries_bloc = BlocChoiceFieldMixin.make_bloc_field()
    countries_bloc_include = BlocChoiceFieldMixin.make_bloc_include_field()

    _bloc_fields = ["countries"]


@admin.register(Bloc)
class BlocAdmin(admin.ModelAdmin):
    form = BlocAdminForm
    filter_horizontal = ["countries"]
    list_display = ["name", "number_of_countries"]
    fields = [
        "name",
        "countries_bloc",
        "countries_bloc_include",
        "countries",
    ]

    @admin.display(description="Countries")
    def number_of_countries(self, obj: Bloc) -> int:
        return obj.countries.count()


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "code",
        "unicode_flag",
        "get_blocs",
        "immigration_summary_status",
        "is_active",
    ]
    list_filter = ["is_active", "immigration_summary_status"]
    list_editable = ["is_active", "immigration_summary_status"]
    ordering = ["name"]
    fields = [
        "name",
        "code",
        "unicode_flag",
        "immigration_summary",
        "immigration_summary_status",
        "is_active",
    ]
    formfield_overrides = {
        django_orm_models.TextField: {"widget": AdminMartorWidget},
    }

    def get_sortable_by(self, request: HttpRequest):
        # This is a pretty random choice of method to use for the purpose, but
        # we need to recompute this on each request; __init__ is called once at
        # server start time.
        self.country_ids_2containing_blocs = (
            Bloc.objects.get_country_id2containing_blocs()
        )
        return super().get_sortable_by(request)

    @admin.display(description="Blocs")
    def get_blocs(self, obj: Country) -> str:
        return ", ".join(
            sorted(b.name for b in self.country_ids_2containing_blocs.get(obj.id, []))
        )

    @admin.display(description="Has immigration summary text?")
    def has_immigration_summary_text(self, obj: Country) -> str:
        return "Yes" if obj.immigration_summary else "No"
