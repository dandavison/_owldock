from django.http import HttpRequest
from django.views import View

from app.models import Country
from owldock.http import OwldockJsonResponse
from .serializers import CountrySerializer


class CountriesList(View):
    def get(self, request: HttpRequest):
        serializer = CountrySerializer(data=Country.objects.all(), many=True)
        serializer.is_valid()
        return OwldockJsonResponse(serializer.data)
