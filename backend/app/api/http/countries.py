from django.http import HttpRequest

from immigration.api import models as api_models
from app.models import Country
from owldock.api.http.base import BaseView
from owldock.http import OwldockJsonResponse


class CountriesList(BaseView):
    def get(self, request: HttpRequest):
        countries = api_models.CountryList.from_orm(list(Country.objects.all()))
        data = countries.dict()["__root__"]
        return OwldockJsonResponse(data)
