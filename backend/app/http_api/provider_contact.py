import json
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.views import View

from app.models import ProviderContact, ProviderContact
from .serializers import CaseSerializer, ApplicantSerializer, ProviderContactSerializer


class _ProviderContactView(View):
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        try:
            self.provider_contact = ProviderContact.objects.get(  # pylint: disable=attribute-defined-outside-init
                user=self.request.user  # type: ignore
            )
        except ProviderContact.DoesNotExist as exc:
            raise Http404 from exc


class CaseList(_ProviderContactView):
    def get(self, request: HttpRequest) -> HttpResponse:
        cases = self.provider_contact.case_set.all()
        serializer = CaseSerializer(data=cases, many=True)
        serializer.is_valid()
        return JsonResponse(serializer.data, safe=False)
