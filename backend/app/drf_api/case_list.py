from django_typomatic import ts_interface
from rest_framework import generics
from rest_framework import serializers

from app.models import Case


@ts_interface()
class CaseListRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = "__all__"
        depth = 2


class CaseListAPIView(generics.ListAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseListRowSerializer
