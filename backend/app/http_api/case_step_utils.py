from django.db.transaction import atomic
from owldock.http import OwldockJsonResponse

from app.http_api.serializers import CaseStepSerializer
from client.models.case_step import CaseStep
from owldock.http import (
    HttpResponseForbidden,
    make_explanatory_http_response,
)
from owldock.state_machine.django_fsm_utils import can_proceed, why_cant_proceed


@atomic
def perform_case_step_transition(
    transition_name,
    queryset,
    queryset_name,
    query_kwargs,
    transition_kwargs=None,
):
    try:
        case_step = queryset.get(**query_kwargs)
    except CaseStep.DoesNotExist:
        return make_explanatory_http_response(queryset, queryset_name, **query_kwargs)
    transition = getattr(case_step, transition_name)
    if not can_proceed(transition):
        return HttpResponseForbidden(
            f"Case step {case_step} cannot do transition {transition.__name__}:\n"
            f"{why_cant_proceed(transition)}"
        )
    transition(**(transition_kwargs or {}))
    case_step.save()
    if queryset.filter(**query_kwargs).exists():
        serializer = CaseStepSerializer(case_step)
        return OwldockJsonResponse(serializer.data)
    else:
        return OwldockJsonResponse(None)
