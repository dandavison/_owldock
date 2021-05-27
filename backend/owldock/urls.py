from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include
from django.urls import path
from django.urls import re_path
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from app.api.http import client_contact
from app.api.http import countries
from app.api.http import provider_contact
from app.api.http import processes
from app.views import HomeView, StatusView
from immigration.api.http import occupations, process_query, process_ruleset

# Note: every route defined here must set appropriate access controls

urlpatterns = [
    # TODO: Currently unprotected
    path("status/", StatusView.as_view()),
    # Login and home page
    path("accounts/", include("django.contrib.auth.urls")),
    path("", login_required(HomeView.as_view())),
    # HTTP API
    path(
        "api/client-contact/applicants/",
        login_required(client_contact.ApplicantList.as_view()),
    ),
    path(
        "api/client-contact/create-case/",
        login_required(client_contact.CreateCase.as_view()),
    ),
    path(
        "api/client-contact/case/<uuid:uuid>/",
        login_required(client_contact.CaseView.as_view()),
    ),
    path(
        "api/client-contact/list-applicants/",
        login_required(client_contact.ApplicantList.as_view()),
    ),
    path(
        "api/client-contact/list-cases/",
        login_required(client_contact.CaseList.as_view()),
    ),
    path(
        "api/client-contact/earmark-case-step/<uuid:uuid>",
        login_required(client_contact.EarmarkCaseStep.as_view()),
        name="client_contact_earmark_case_step",
    ),
    path(
        "api/client-contact/offer-case-step/<uuid:uuid>",
        login_required(client_contact.OfferCaseStep.as_view()),
        name="client_contact_offer_case_step",
    ),
    path(
        "api/client-contact/retract-case-step-contract/<uuid:uuid>",
        login_required(client_contact.RetractCaseStep.as_view()),
        name="client_contact_retract_case_step",
    ),
    path(
        "api/client-contact/case-step-upload-files/<uuid:uuid>/",
        login_required(client_contact.CaseStepUploadFiles.as_view()),
    ),
    path(
        "api/client-contact/list-provider-contacts/",
        login_required(client_contact.ProviderContactList.as_view()),
    ),
    path(
        "api/client-contact/list-primary-provider-contacts/",
        login_required(client_contact.PrimaryProviderContactList.as_view()),
    ),
    path(
        "api/client-contact/list-provider-relationships/",
        login_required(client_contact.ClientProviderRelationshipList.as_view()),
    ),
    path(
        "api/countries/",
        login_required(cache_page(0xFFFFFFFF)(countries.CountriesList.as_view())),
    ),
    path("api/occupations/", login_required(occupations.OccupationsList.as_view())),
    path("api/process/query/", login_required(process_query.ProcessQuery.as_view())),
    path(
        "api/processruleset/<str:country_code>/",
        login_required(process_ruleset.ProcessRuleSetQuery.as_view()),
    ),
    path(
        "api/process/<int:id>/",
        login_required(process_ruleset.ProcessRuleSet.as_view()),
    ),
    path(
        "api/provider-contact/case/<uuid:uuid>/",
        login_required(provider_contact.CaseView.as_view()),
    ),
    path(
        "api/provider-contact/case-step/<uuid:uuid>/",
        login_required(provider_contact.CaseStepView.as_view()),
    ),
    path(
        "api/provider-contact/list-applicants/",
        login_required(provider_contact.ApplicantList.as_view()),
    ),
    path(
        "api/provider-contact/list-cases/",
        login_required(provider_contact.CaseList.as_view()),
    ),
    path(
        "api/provider-contact/accept-case-step/<uuid:uuid>",
        login_required(provider_contact.AcceptCaseStep.as_view()),
        name="provider_contact_accept_case_step",
    ),
    path(
        "api/provider-contact/reject-case-step-contract/<uuid:uuid>",
        login_required(provider_contact.RejectCaseStep.as_view()),
        name="provider_contact_reject_case_step",
    ),
    path(
        "api/provider-contact/complete-case-step-contract/<uuid:uuid>",
        login_required(provider_contact.CompleteCaseStep.as_view()),
        name="provider_contact_complete_case_step",
    ),
    path(
        "api/provider-contact/case-step-upload-files/<uuid:uuid>/",
        login_required(provider_contact.CaseStepUploadFiles.as_view()),
    ),
    path("api/processes/", login_required(processes.ProcessList.as_view())),
    # Admin
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),  # TODO: permission
    path("grappelli/", include("grappelli.urls")),
    path("_nested_admin/", include("nested_admin.urls")),
]

if settings.DEV:
    import debug_toolbar

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))

if not getattr(settings, "UI_DEV_MODE", False):
    # client-side routes handled by Vue router
    # https://stackoverflow.com/questions/42864641/handling-single-page-application-url-and-django-url
    urlpatterns.append(
        re_path(
            r"^portal(/.*)?$",
            login_required(TemplateView.as_view(template_name="app/index.html")),
        )
    )
