import json
import logging
from typing import List

from django.db.transaction import atomic
from django.http import HttpRequest, HttpResponse

from app.models.bloc import Bloc
from app.models.country import Country
from immigration import models as orm_models
from immigration.api import models as api_models
from owldock.dev.db_utils import print_queries, print_query_counts
from owldock.api.http.base import BaseView
from owldock.http import (
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    OwldockJsonResponse,
)

logger = logging.getLogger(__name__)


class ProcessRuleSet(BaseView):
    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        return self._get(id)

    def _get(self, id: int) -> HttpResponse:
        with print_query_counts():
            orm_process_ruleset = api_models.ProcessRuleSet.get_orm_model(id=id)

        with print_queries():
            api_process_ruleset = api_models.ProcessRuleSet.from_orm(
                orm_process_ruleset
            )
            data = api_process_ruleset.dict()
        return OwldockJsonResponse(data)

    @atomic
    def post(self, request: HttpRequest, id: int) -> HttpResponse:
        """
        Handle write request from Gantt chart editor.
        """
        if not request.user.is_superuser:
            return HttpResponseForbidden("User is not a superuser")
        try:
            process_ruleset = orm_models.ProcessRuleSet.objects.select_related(
                "route__host_country"
            ).get(id=id)
        except orm_models.ProcessRuleSet.DoesNotExist:
            return HttpResponseNotFound(f"No ProcessRuleSet matching id={id} exists")
        else:
            data = json.loads(request.body)
            process_steps = orm_models.ProcessStep.objects.get_for_host_country_codes(
                [process_ruleset.route.host_country.code]
            ).in_bulk()
            try:
                for step_data in data:
                    step = process_steps[step_data["id"]]
                    step.depends_on.set(step_data["depends_on_"])
                    assert set(s.id for s in step.depends_on.all()) == set(
                        step_data["depends_on_"]
                    )
                    (
                        step.estimated_min_duration_days,
                        step.estimated_max_duration_days,
                    ) = step_data["step_duration_range"]
                    step.save()
                    prss, created = orm_models.ProcessRuleSetStep.objects.get_or_create(
                        process_ruleset=process_ruleset, process_step=step
                    )
                    if created:
                        logger.info(f"Created ProcessRuleSetSet: {prss}")
            except (KeyError, IndexError, ValueError, TypeError) as exc:
                return HttpResponseBadRequest(f"{exc.__class__.__name__}({exc})")
            else:
                return self._get(id)


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
