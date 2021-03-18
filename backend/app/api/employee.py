from django_typomatic import ts_interface
from rest_framework import generics
from rest_framework import serializers

from app.models import Employee


@ts_interface()
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
        depth = 1

class EmployeeAPIView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
