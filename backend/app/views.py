from django.http import HttpRequest, JsonResponse
from django.views.generic import RedirectView, View
from subprocess import check_output, CalledProcessError

from app import models as app_orm_models
from client import models as client_orm_models
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
                "clients": client_orm_models.Client.objects.count(),
                "providers": app_orm_models.Provider.objects.count(),
            }
        )

    def _get_git_head_commit(self) -> str:
        try:
            return check_output(["git", "rev-parse", "HEAD"]).strip().decode("utf-8")
        except CalledProcessError:
            return "error"
