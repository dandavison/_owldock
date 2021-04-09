import sys
import traceback

from owldock.dev.traceback import render_stack


class process_exception:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if exception:
            tb = sys.exc_info()[2]
            print(render_stack(traceback.format_tb(tb)))
