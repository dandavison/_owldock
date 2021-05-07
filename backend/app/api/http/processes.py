from django.http import Http404, HttpRequest, HttpResponse
from django.views import View

from app.api.serializers import ProcessSerializer
from immigration.models import ProcessRuleSet
from owldock.http import OwldockJsonResponse


class ProcessList(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Return ProcessRuleSets matching host country and applicant nationality.
        """
        nationality_codes = [
            s.strip()
            for s in request.GET.get("nationalities", "").strip().split(",")
            if s.strip()
        ]
        host_country_code = request.GET.get("host_country", "").strip()
        if not (nationality_codes and any(nationality_codes) and host_country_code):
            raise Http404(
                "nationalities and host_country must be supplied in URL params"
            )
        processes = ProcessRuleSet.objects.filter(
            nationalities__code__in=nationality_codes,
            route__host_country__code=host_country_code,
        ).distinct()
        # TODO: Process vs ProcessRuleSet
        serializer = ProcessSerializer(data=processes, many=True)
        serializer.is_valid()
        return OwldockJsonResponse(serializer.data)
