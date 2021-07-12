from django.http import HttpRequest, JsonResponse
from django.views.generic import RedirectView, View
from subprocess import check_output, CalledProcessError

from app.models import Provider
from client.models import Client
from owldock.state_machine.role import get_role, Role


class HomeView(RedirectView):
    def get_redirect_url(self, *args, **kwargs) -> str:
        role = get_role(self.request.user)
        if role in [Role.CLIENT_CONTACT, Role.PROVIDER_CONTACT]:
            return "/portal/"
        else:
            return "/accounts/logout/"


class StatusView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse(
            {
                "commit": self._get_git_head_commit(),
                "clients": Client.objects.count(),
                "providers": Provider.objects.count(),
            }
        )

    def _get_git_head_commit(self) -> str:
        try:
            return check_output(["git", "rev-parse", "HEAD"]).strip().decode("utf-8")
        except CalledProcessError:
            return "error"
