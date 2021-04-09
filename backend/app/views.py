from django.views.generic import RedirectView

from owldock.state_machine.role import get_role, Role


class HomeView(RedirectView):
    def get_redirect_url(self, *args, **kwargs) -> str:
        role = get_role(self.request.user)
        if role in [Role.CLIENT_CONTACT, Role.PROVIDER_CONTACT]:
            return "/portal/"
        else:
            return "/accounts/logout/"
