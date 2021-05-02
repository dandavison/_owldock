import json
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.views import View

from immigration.api.serializers import OccupationSerializer
from owldock.http import OwldockJsonResponse

OCCUPATIONS = None


def _get_occupations():
    global OCCUPATIONS
    if OCCUPATIONS is None:
        with open(settings.BASE_DIR / "data" / "occupations.json") as fp:
            raw = json.load(fp)
        OCCUPATIONS = [{"name": name} for name in raw["occupations"]]
    return OCCUPATIONS


class OccupationsList(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        serializer = OccupationSerializer(_get_occupations(), many=True)
        return OwldockJsonResponse(serializer.data)
