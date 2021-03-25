from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.views import View

from app.models import Process
from .serializers import ProcessSerializer


class ProcessList(View):
    def get(self, request: HttpRequest) -> HttpResponse:
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
        processes = Process.objects.filter(
            nationality__code__in=nationality_codes,
            route__host_country__code=host_country_code,
        )
        serializer = ProcessSerializer(data=processes, many=True)
        serializer.is_valid()
        return JsonResponse(serializer.data, safe=False)
