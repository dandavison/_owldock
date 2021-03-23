from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include
from django.urls import path
from django.urls import re_path
from django.views.generic import TemplateView

from app.http_api import client_contact
from app.views import HomeView

# Note: every route defined here must set appropriate access controls

urlpatterns = [
    # Login and home page
    path("accounts/", include("django.contrib.auth.urls")),
    path("", login_required(HomeView.as_view())),
    # HTTP API
    path(
        "api/client-contact/employees/",
        login_required(client_contact.EmployeesList.as_view()),
    ),
    # Admin
    path("admin/", admin.site.urls),  # TODO: permission
    path("grappelli/", include("grappelli.urls")),
    # Assume anything else is a client-side route handled by Vue router
    # https://stackoverflow.com/questions/42864641/handling-single-page-application-url-and-django-url
    re_path(
        r"^.*$", login_required(TemplateView.as_view(template_name="app/index.html"))
    ),
]
