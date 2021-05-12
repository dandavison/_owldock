from django.core import serializers
from django.core.management.base import BaseCommand
from django.db.models import QuerySet
from django.conf import settings

from app.models import Country
from immigration.models import (
    IssuedDocument,
    IssuedDocumentType,
    ProcessRuleSet,
    ProcessRuleSetStep,
    ProcessStep,
    Route,
    ServiceItem,
)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print("countries...")
        self._serialize_queryset(Country.objects.order_by("name"), "country.json")
        print("processruleset...")
        self._serialize_queryset(
            ProcessRuleSet.objects.prefetch_related(
                "nationalities", "home_countries"
            ).order_by("route__host_country", "route__name"),
            "processruleset.json",
        )
        print("processrulesetstep...")
        self._serialize_queryset(
            ProcessRuleSetStep.objects.order_by(
                "process_ruleset__route__host_country", "process_ruleset__route__name"
            ),
            "processrulesetstep.json",
        )
        print("processstep...")
        self._serialize_queryset(
            ProcessStep.objects.prefetch_related("issued_documents").order_by(
                "processruleset__route__host_country",
                "processruleset__route__name",
                "id",
            ),
            "processstep.json",
        )
        print("route...")
        self._serialize_queryset(
            Route.objects.order_by(
                "host_country",
                "name",
            ),
            "route.json",
        )
        print("issueddocument...")
        self._serialize_queryset(
            IssuedDocument.objects.order_by(
                "id",
            ),
            "issueddocument.json",
        )
        print("issueddocumenttype...")
        self._serialize_queryset(
            IssuedDocumentType.objects.order_by(
                "name",
            ),
            "issueddocumenttype.json",
        )
        print("serviceitem...")
        self._serialize_queryset(
            ServiceItem.objects.order_by(
                "description",
            ),
            "serviceitem.json",
        )

    def _serialize_queryset(self, queryset: QuerySet, filename: str) -> None:
        path = settings.BASE_DIR / "db" / filename
        serializer = serializers.get_serializer("json")()
        with open(path, "w") as f:
            serializer.serialize(
                queryset,
                indent=2,
                sort_keys=True,
                stream=f,
            )
