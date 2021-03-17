from django.contrib import admin
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from app import views

router = DefaultRouter()
router.register("person-immigration-tasks", views.PersonImmigrationTaskViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
