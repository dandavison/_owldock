from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.urls import include
from django.urls import path
from django.urls import re_path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from app import views as app_views

router = DefaultRouter()
router.register("person-immigration-tasks", app_views.PersonImmigrationTaskViewSet)

# Note: every route defined here must set appropriate access controls

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("", login_required(TemplateView.as_view(template_name="app/index.html"))),
    path("admin/", admin.site.urls),  # TODO: permission
    path("api/", include(router.urls)),  # TODO: permission
    # Assume anything else is a client-side route handled by Vue router
    # https://stackoverflow.com/questions/42864641/handling-single-page-application-url-and-django-url
    re_path(
        r"^.*$", login_required(TemplateView.as_view(template_name="app/index.html"))
    ),
]
