import json
from django.http import HttpRequest, HttpResponse
from django.views import View

from app.api.serializers import MoveSerializer, ProcessSerializer
from immigration.query import get_processes
from owldock.http import HttpResponseBadRequest, OwldockJsonResponse

red = lambda s: __import__("clint").textui.colored.red(s, always=True, bold=True)

# TODO: auth?
class ProcessQuery(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        data = json.loads(request.body)
        print(red(json.dumps(data, indent=2)))
        move_serializer = MoveSerializer(data=data)
        if move_serializer.is_valid():
            processes = get_processes(move_serializer.data)
            process_serializer = ProcessSerializer(processes, many=True)
            return OwldockJsonResponse(process_serializer.data)
        else:
            __import__("pdb").set_trace()
            return HttpResponseBadRequest(
                f"validation-errors: {move_serializer.errors}"
            )
