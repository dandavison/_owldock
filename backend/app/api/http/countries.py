from django.http import HttpRequest

from app.api.serializers import CountrySerializer
from app.models import Country
from owldock.api.http.base import BaseView
from owldock.http import OwldockJsonResponse


class CountriesList(BaseView):
    def get(self, request: HttpRequest):
        serializer = CountrySerializer(data=Country.objects.all(), many=True)
        serializer.is_valid()
        return OwldockJsonResponse(serializer.data)
