from django.http import JsonResponse


class OwldockJsonResponse(JsonResponse):
    """
    All owldock JSON responses must have the format defined here.
    """

    def __init__(self, data, errors=None, messages=None, **kwargs):
        payload = {
            "data": data,
            "errors": errors or [],
            "messages": messages or [],
        }
        super().__init__(payload, **kwargs)
