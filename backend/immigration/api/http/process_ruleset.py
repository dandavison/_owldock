from django.http import HttpRequest, HttpResponse
from django.views import View

from immigration import models as orm_models
from immigration.api import models as api_models
from owldock.http import OwldockJsonResponse


# TODO: auth?
class ProcessRuleSetQuery(View):
    def get(self, request: HttpRequest, country_code: str) -> HttpResponse:
        orm_process_rulesets = list(
            orm_models.ProcessRuleSet.objects.filter(
                route__host_country__code=country_code
            )
        )
        api_process_rulesets = api_models.ProcessRuleSetList.from_orm(
            orm_process_rulesets
        )
        return OwldockJsonResponse(api_process_rulesets.dict()["__root__"])
