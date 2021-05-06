from django.contrib import admin

from app.models import (
    Country,
    Provider,
    ProviderContact,
    StoredFile,
)

admin.site.register(Country)
admin.site.register(Provider)
admin.site.register(ProviderContact)
admin.site.register(StoredFile)
