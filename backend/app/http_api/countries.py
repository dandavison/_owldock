import django_countries
from django.http import HttpRequest, JsonResponse
from django.views import View
from django_typomatic import ts_interface
from rest_framework import serializers


class CountriesList(View):
    def get(self, request: HttpRequest):
        serializer = CountrySerializer(data=django_countries.countries, many=True)
        serializer.is_valid()
        return JsonResponse(serializer.data, safe=False)


@ts_interface()
class CountrySerializer(serializers.Serializer):  # pylint: disable=abstract-method
    code = serializers.CharField()
    name = serializers.CharField()
