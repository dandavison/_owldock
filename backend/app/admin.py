from django.contrib import admin

from app.models import (
    Bloc,
    Country,
    Provider,
    ProviderContact,
    StoredFile,
)

admin.site.register(Country)
admin.site.register(Provider)
admin.site.register(ProviderContact)
admin.site.register(StoredFile)


@admin.register(Bloc)
class BlocAdmin(admin.ModelAdmin):
    filter_horizontal = ["countries"]
    list_display = ["name", "number_of_countries"]

    @admin.display(description="Number of countries")
    def number_of_countries(self, obj: Bloc) -> int:
        return obj.countries.count()
