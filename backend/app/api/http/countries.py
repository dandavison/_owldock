from django.http import HttpRequest

from app import models as app_orm_models
from immigration import api as immigration_api
from owldock.api.http.base import BaseView
from owldock.http import OwldockJsonResponse


class CountriesList(BaseView):
    def get(self, request: HttpRequest):
        countries = immigration_api.models.CountryList.from_orm(
            list(app_orm_models.Country.objects.all())
        )
        data = countries.dict()["__root__"]
        return OwldockJsonResponse(data)
