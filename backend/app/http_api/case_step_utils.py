from uuid import UUID
from typing import Union

from django.db.transaction import atomic
from django.http import HttpRequest, HttpResponse

from app.exceptions import PermissionDenied
from app.http_api.serializers import CaseStepSerializer
from app.models import ProviderContact
from client.models import CaseStep, ClientContact
from owldock.http import (
    HttpResponseForbidden,
    HttpResponseNotFound,
    make_explanatory_http_response,
    OwldockJsonResponse,
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


def add_uploaded_files_to_case_step(
    client_or_provider_contact: Union[ClientContact, ProviderContact],
    request: HttpRequest,
    uuid: UUID,
) -> HttpResponse:
    try:
        client_or_provider_contact.add_uploaded_files_to_case_step(
            request.FILES.getlist("file"), step_uuid=uuid
        )
    except PermissionDenied:
        return HttpResponseForbidden(
            (
                f"User {request.user} does not have permission to upload files to "
                f"case step {uuid}"
            )
        )
    except CaseStep.DoesNotExist:
        try:
            case_step = client_or_provider_contact.cases_steps_with_read_permission.get(
                uuid=uuid
            )
        except CaseStep.DoesNotExist:
            return HttpResponseNotFound(f"Case step {uuid} does not exist")
        else:
            return OwldockJsonResponse(
                None,
                errors=[
                    (
                        f"You don't currently have permission to upload files to this "
                        f"step. The status of this step is {case_step.state.value}."
                    )
                ],
            )
    else:
        return OwldockJsonResponse(None)
