from django.contrib.auth import get_user_model
from django_countries.serializers import CountryFieldMixin
from django_typomatic import ts_interface
from rest_framework import serializers

from app.models import Case
from app.models import Country, Employee, Process


# FIXME: These serializers are sending the user.password hash


@ts_interface()
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


@ts_interface()
class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = "__all__"
        depth = 2


@ts_interface()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"
        depth = 2


@ts_interface()
class EmployeeSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
        depth = 1


@ts_interface()
class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = "__all__"
        depth = 2
