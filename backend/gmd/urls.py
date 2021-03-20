from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include
from django.urls import path
from django.urls import re_path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

from app.http_api import employee as employee_api
from app.http_api import case as case_api
from app.http_api import case_list as case_list_api
from app.views import HomeView

# Note: every route defined here must set appropriate access controls

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("", login_required(HomeView.as_view())),
    path("admin/", admin.site.urls),  # TODO: permission
    path("grappelli/", include("grappelli.urls")),
    path("api/employees/", employee_api.EmployeeAPIView.as_view()),  # TODO: permission
    path(
        "api/cases/",
        case_api.CaseAPIView.as_view(),
    ),  # TODO: permission
    path(
        "api/case-list/",
        case_list_api.CaseListAPIView.as_view(),
    ),  # TODO: permission
    path(
        "api/",
        get_schema_view(title="GMD", version="0.0.1"),
        name="openapi-schema",
    ),
    # Assume anything else is a client-side route handled by Vue router
    # https://stackoverflow.com/questions/42864641/handling-single-page-application-url-and-django-url
    re_path(
        r"^.*$", login_required(TemplateView.as_view(template_name="app/index.html"))
    ),
]
