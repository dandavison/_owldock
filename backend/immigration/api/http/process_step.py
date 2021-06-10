from django.http import HttpRequest, HttpResponse

from immigration.api import models as api_models
from owldock.api.http.base import BaseView
from owldock.http import OwldockJsonResponse


class ProcessStepList(BaseView):
    def get(self, request: HttpRequest, country_code: str) -> HttpResponse:
        orm_process_steps = api_models.ProcessStepList.get_orm_models(country_code)
        api_process_steps = api_models.ProcessStepList.from_orm(orm_process_steps)
        data = api_process_steps.dict()["__root__"]
        return OwldockJsonResponse(data)
