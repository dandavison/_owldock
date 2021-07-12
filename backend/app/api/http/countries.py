from django.http import HttpRequest

from app.models import Country
from immigration import api as immigration_api
from owldock.api.http.base import BaseView
from owldock.http import OwldockJsonResponse


class CountriesList(BaseView):
    def get(self, request: HttpRequest):
        countries = immigration_api.models.CountryList.from_orm(
            list(Country.objects.all())
        )
        data = countries.dict()["__root__"]
        return OwldockJsonResponse(data)
