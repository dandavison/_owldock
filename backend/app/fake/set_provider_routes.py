from django.db.transaction import atomic

from app.models import Provider, Route


@atomic
def set_provider_routes():
    other_provider, *providers = Provider.objects.order_by("-name")
    other_route, *routes = Route.objects.order_by("-name")

    for (_providers, _routes) in [
        (providers, routes),
        ([other_provider], [other_route]),
    ]:
        for _provider in _providers:
            _provider.routes.add(*_routes)
