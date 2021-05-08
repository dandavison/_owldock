from django.contrib import admin
from django.forms import ModelForm, ModelChoiceField

from app.models import (
    Bloc,
    Country,
    Provider,
    ProviderContact,
    StoredFile,
)
from immigration.admin.bloc_choice_field import BlocChoiceFieldMixin  # type: ignore


admin.site.register(Country)
admin.site.register(Provider)
admin.site.register(ProviderContact)
admin.site.register(StoredFile)


class BlocAdminForm(BlocChoiceFieldMixin, ModelForm):
    countries_bloc = ModelChoiceField(
        Bloc.objects.all(),
        required=False,
    )

    _bloc_fields = [
        ("countries", "countries_bloc"),
    ]


@admin.register(Bloc)
class BlocAdmin(admin.ModelAdmin):
    form = BlocAdminForm
    filter_horizontal = ["countries"]
    list_display = ["name", "number_of_countries"]
    fields = [
        "name",
        "countries_bloc",
        "countries",
    ]

    @admin.display(description="Number of countries")
    def number_of_countries(self, obj: Bloc) -> int:
        return obj.countries.count()
