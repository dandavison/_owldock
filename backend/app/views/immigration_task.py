from django_typomatic import ts_interface
from rest_framework import generics
from rest_framework import serializers

from app.models import ImmigrationTask


@ts_interface()
class ImmigrationTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImmigrationTask
        fields = "__all__"


class ImmigrationTaskAPIView(generics.ListCreateAPIView):
    queryset = ImmigrationTask.objects.all()
    serializer_class = ImmigrationTaskSerializer
