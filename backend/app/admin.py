from django.contrib import admin
from django.forms import ChoiceField, ModelForm, ModelChoiceField, RadioSelect

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
