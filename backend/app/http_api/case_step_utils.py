from django.db.transaction import atomic
from django.http import JsonResponse

from app.http_api.serializers import CaseStepSerializer
from client.models.case_step import CaseStep
from owldock.api.http import (
    HttpResponseForbidden,
    make_explanatory_http_response,
)
from owldock.state_machine.django_fsm_utils import can_proceed, why_cant_proceed


@atomic
def perform_case_step_transition(transition_name, queryset, queryset_name, **kwargs):
    try:
        case_step = queryset.get(**kwargs)
    except CaseStep.DoesNotExist:
        return make_explanatory_http_response(queryset, queryset_name, **kwargs)
    transition = getattr(case_step, transition_name)
    if not can_proceed(transition):
        return HttpResponseForbidden(
            f"Case step {case_step} cannot do transition {transition.__name__}:\n"
            f"{why_cant_proceed(transition)}"
        )
    transition()
    case_step.save()
    if queryset.filter(**kwargs).exists():
        serializer = CaseStepSerializer(case_step)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse(None, safe=False)
