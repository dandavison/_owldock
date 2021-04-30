from django.contrib import admin

from immigration.models import (
    IssuedDocument,
    IssuedDocumentType,
    Process,
    ProcessStep,
)

admin.site.register(IssuedDocument)
admin.site.register(IssuedDocumentType)
admin.site.register(Process)
admin.site.register(ProcessStep)
