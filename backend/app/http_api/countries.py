from django.http import HttpRequest, JsonResponse
from django.views import View

from app.models import Country
from .serializers import CountrySerializer


class CountriesList(View):
    def get(self, request: HttpRequest):
        serializer = CountrySerializer(data=Country.objects.all(), many=True)
        serializer.is_valid()
        return JsonResponse(serializer.data, safe=False)
