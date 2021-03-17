from django_typomatic import ts_interface
from rest_framework import serializers

from app.models import ImmigrationTask


@ts_interface()
class ImmigrationTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImmigrationTask
        fields = [
            "id",
            "employee",
            "case_type",
            "current_status",
            "host_country",
            "progress",
            "service",
            "target_entry_date",
        ]
        depth = 1
