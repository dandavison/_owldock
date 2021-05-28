from typing import List

from django.http import HttpRequest, HttpResponse

from app.models.bloc import Bloc
from app.models.country import Country
from immigration import models as orm_models
from immigration.api import models as api_models
from owldock.dev.db_utils import print_queries, print_query_counts
from owldock.api.http.base import BaseView
from owldock.http import OwldockJsonResponse


class ProcessRuleSet(BaseView):
    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        with print_query_counts():
            orm_process_ruleset = api_models.ProcessRuleSet.get_orm_model(id=id)

        with print_queries():
            api_process_ruleset = api_models.ProcessRuleSet.from_orm(
                orm_process_ruleset
            )
            data = api_process_ruleset.dict()
        return OwldockJsonResponse(data)


# TODO: auth?
class ProcessRuleSetList(BaseView):
    def get(self, request: HttpRequest, country_code: str) -> HttpResponse:
        with print_query_counts():
            orm_process_rulesets = api_models.ProcessRuleSetList.get_orm_models(
                route__host_country__code=country_code
            )

        with print_queries():
            api_process_rulesets = api_models.ProcessRuleSetList.from_orm(
                orm_process_rulesets
            )
            data = api_process_rulesets.dict()["__root__"]
        self._add_bloc_descriptions("nationalities", data)
        return OwldockJsonResponse(data)

    @staticmethod
    def _add_bloc_descriptions(key: str, data: List[dict]) -> None:
        # pydantic does not serialize computed properties
        # https://github.com/samuelcolvin/pydantic/issues/935
        get_bloc_description_from_countries = (
            Bloc.objects.make_get_description_from_countries()
        )
        country_code2country = {c.code: c for c in Country.objects.all()}
        for prs in data:
            countries = [country_code2country[c["code"]] for c in prs[key]]
            description = get_bloc_description_from_countries(countries)
            # The set of countries is being used to describe a rule here, and
            # empty set means a rule imposing no constraint.
            prs[f"{key}_description"] = "" if description == "0" else description
