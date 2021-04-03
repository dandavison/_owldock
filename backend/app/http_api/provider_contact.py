from django.conf import settings
from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseNotFound,
    JsonResponse,
)
from django.views import View

from app.exceptions import PermissionDenied
from app.models import CaseStep, ProviderContact
from app.http_api.serializers import (
    CaseSerializer,
)


# TODO: Refactor to share implementation with _ClientContactView
class _ProviderContactView(View):
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        try:
            self.provider_contact = ProviderContact.objects.get(  # pylint: disable=attribute-defined-outside-init
                user=self.request.user  # type: ignore
            )
        except ProviderContact.DoesNotExist as exc:
            self.provider_contact = None

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not self.provider_contact:
            if settings.DEBUG:
                return HttpResponseForbidden("User is not a provider contact")
            else:
                raise Http404
        else:
            return super().dispatch(request, *args, **kwargs)


class Case(_ProviderContactView):
    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        case = self.provider_contact.get_case_with_read_permissions(case_id=id)
        serializer = CaseSerializer(case)
        return JsonResponse(serializer.data, safe=False)


class CaseList(_ProviderContactView):
    def get(self, request: HttpRequest) -> HttpResponse:
        cases = self.provider_contact.case_set.all()
        serializer = CaseSerializer(data=cases, many=True)
        serializer.is_valid()
        return JsonResponse(serializer.data, safe=False)


class CaseStepUploadFiles(_ProviderContactView):
    def post(self, request: HttpRequest, step_id: int) -> HttpResponse:
        try:
            self.provider_contact.add_uploaded_files_to_case_step(
                request.FILES.getlist("file"), step_id=step_id
            )
        except PermissionDenied:
            if settings.DEBUG:
                return HttpResponseForbidden(
                    f"User {request.user} does not have permission to upload files to case step {step_id}"
                )
            else:
                raise Http404
        except CaseStep.DoesNotExist:
            if settings.DEBUG:
                return HttpResponseNotFound(f"Case step {step_id} does not exist")
            else:
                raise Http404
        else:
            return JsonResponse({"errors": None})