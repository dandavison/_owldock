from django.contrib import admin

from app.models import (
    Activity,
    Country,
    Process,
    ProcessStep,
    Provider,
    ProviderContact,
    Service,
    Route,
    StoredFile,
)

admin.site.register(Activity)
admin.site.register(Country)
admin.site.register(Process)
admin.site.register(ProcessStep)
admin.site.register(Provider)
admin.site.register(ProviderContact)
admin.site.register(Service)
admin.site.register(Route)
admin.site.register(StoredFile)
