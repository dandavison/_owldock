from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include
from django.urls import path
from django.urls import re_path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

from app.views import employee as employee_views
from app.views import immigration_task as immigration_task_views
from app.views import immigration_task_list as immigration_task_list_views

# Note: every route defined here must set appropriate access controls

urlpatterns = [
    re_path("accounts/?", include("django.contrib.auth.urls")),
    path("", login_required(TemplateView.as_view(template_name="app/index.html"))),
    re_path("admin/?", admin.site.urls),  # TODO: permission
    re_path("grappelli/?", include("grappelli.urls")),
    re_path(
        "api/employees/?", employee_views.EmployeeAPIView.as_view()
    ),  # TODO: permission
    re_path(
        "api/immigration-tasks/?",
        immigration_task_views.ImmigrationTaskAPIView.as_view(),
    ),  # TODO: permission
    re_path(
        "api/immigration-task-list/?",
        immigration_task_list_views.ImmigrationTaskListAPIView.as_view(),
    ),  # TODO: permission
    re_path(
        "api/?",
        get_schema_view(title="GMD", version="0.0.1"),
        name="openapi-schema",
    ),
    # Assume anything else is a client-side route handled by Vue router
    # https://stackoverflow.com/questions/42864641/handling-single-page-application-url-and-django-url
    re_path(
        r"^.*$", login_required(TemplateView.as_view(template_name="app/index.html"))
    ),
]
