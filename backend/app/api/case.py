from django_typomatic import ts_interface
from rest_framework import generics
from rest_framework import serializers

from app.models import Case


@ts_interface()
class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = "__all__"


class CaseAPIView(generics.ListCreateAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
