import json
from django.http import HttpRequest, HttpResponse
from django.views import View

from app.api.serializers import MoveSerializer, ProcessSerializer
from app.models import Country
from immigration.models import Move
from immigration.query import get_processes
from owldock.http import HttpResponseBadRequest, OwldockJsonResponse


# TODO: auth?
class ProcessQuery(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        move_serializer = MoveSerializer(data=json.loads(request.body))
        if move_serializer.is_valid():
            # TODO
            move = Move(
                host_country=Country.objects.get(
                    name=move_serializer.validated_data["host_country"]["name"]
                )
            )
            processes = get_processes(move)
            process_serializer = ProcessSerializer(processes, many=True)
            return OwldockJsonResponse(process_serializer.data)
        else:
            return HttpResponseBadRequest(
                f"validation-errors: {move_serializer.errors}"
            )
