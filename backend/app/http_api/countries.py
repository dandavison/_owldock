from django.http import HttpRequest, JsonResponse
from django.views import View
from django_typomatic import ts_interface
from rest_framework import serializers

from app.models import Country


class CountriesList(View):
    def get(self, request: HttpRequest):
        serializer = CountrySerializer(data=Country.objects.all(), many=True)
        serializer.is_valid()
        return JsonResponse(serializer.data, safe=False)


@ts_interface()
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"
