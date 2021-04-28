from django.contrib import admin

from client.models import (
    Applicant,
    ApplicantNationality,
    Case,
    CaseStep,
    CaseStepContract,
    Client,
    ClientContact,
    ClientProviderRelationship,
)

admin.site.register(Applicant)
admin.site.register(ApplicantNationality)
admin.site.register(Case)
admin.site.register(CaseStep)
admin.site.register(CaseStepContract)
admin.site.register(Client)
admin.site.register(ClientContact)
admin.site.register(ClientProviderRelationship)
