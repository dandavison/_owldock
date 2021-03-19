import logging
from typing import Optional

from django.contrib.auth.models import User
from django.views.generic import RedirectView

from app.constants import GroupName
from app.constants import Role

logger = logging.getLogger(__file__)


class HomeView(RedirectView):
    def get_redirect_url(self, *args, **kwargs) -> str:
        role = get_role(self.request.user)
        if role == Role.CLIENT_CONTACT:
            return "/client-portal/"
        elif role == Role.PROVIDER_CONTACT:
            return "/provider-portal/"
        else:
            return "/accounts/logout/"


def get_role(user: User) -> Optional[Role]:
    groups = {g.name for g in user.groups.all()}
    is_client_contact = GroupName.CLIENT_CONTACTS.value in groups
    is_provider_contact = GroupName.PROVIDER_CONTACTS.value in groups
    if is_client_contact and is_provider_contact:
        logger.error(
            f"User {user} is in both client-contact and provider-contact groups"
        )
        return None
    elif is_client_contact:
        return Role.CLIENT_CONTACT
    elif is_provider_contact:
        return Role.PROVIDER_CONTACT
    else:
        return None
