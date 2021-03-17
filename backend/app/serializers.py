from django_typomatic import ts_interface
from rest_framework import serializers

from app.models import PersonImmigrationTask


@ts_interface()
class PersonImmigrationTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonImmigrationTask
        fields = [
            "id",
            "person",
            "case_type",
            "current_status",
            "host_country",
            "progress",
            "service",
            "target_entry_date",
        ]
        depth = 1
