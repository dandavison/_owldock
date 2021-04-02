from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include
from django.urls import path
from django.urls import re_path
from django.views.generic import TemplateView

from app.http_api import client_contact
from app.http_api import countries
from app.http_api import provider_contact
from app.http_api import processes
from app.views import HomeView

# Note: every route defined here must set appropriate access controls

urlpatterns = [
    # Login and home page
    path("accounts/", include("django.contrib.auth.urls")),
    path("", login_required(HomeView.as_view())),
    # HTTP API
    path(
        "api/client-contact/applicants/",
        login_required(client_contact.ApplicantsList.as_view()),
    ),
    path(
        "api/client-contact/create-case/",
        login_required(client_contact.CreateCase.as_view()),
    ),
    path(
        "api/client-contact/case/<int:id>/",
        login_required(client_contact.Case.as_view()),
    ),
    path(
        "api/client-contact/list-cases/",
        login_required(client_contact.CaseList.as_view()),
    ),
    path(
        "api/client-contact/list-provider-contacts/",
        login_required(client_contact.ProviderContactList.as_view()),
    ),
    path("api/countries/", login_required(countries.CountriesList.as_view())),
    path(
        "api/provider-contact/list-cases/",
        login_required(provider_contact.CaseList.as_view()),
    ),
    path(
        "api/case-step/<int:step_id>/upload-files/",
        login_required(provider_contact.CaseStepUploadFiles.as_view()),
    ),
    path("api/processes/", login_required(processes.ProcessList.as_view())),
    # Admin
    path("admin/", admin.site.urls),  # TODO: permission
    path("grappelli/", include("grappelli.urls")),
    # client-side routes handled by Vue router
    # https://stackoverflow.com/questions/42864641/handling-single-page-application-url-and-django-url
    re_path(
        r"^portal(/.*)?$",
        login_required(TemplateView.as_view(template_name="app/index.html")),
    ),
]
