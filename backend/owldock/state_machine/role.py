import logging
from enum import Enum
from typing import Optional, Union, TYPE_CHECKING

from django.http import HttpRequest

from app.models import User

if TYPE_CHECKING:
    from app.models import ProviderContact
    from client.models import ClientContact

logger = logging.getLogger(__file__)


class Role(Enum):
    ADMIN = "Admin"
    CLIENT_CONTACT = "Client Contact"
    PROVIDER_CONTACT = "Provider Contact"


class UserRole:
    def __init__(self, user: User):
        from client.models import ClientContact
        from app.models import ProviderContact

        self.user = user
        try:
            self.client_contact: Optional[ClientContact] = ClientContact.objects.get(
                user_uuid=user.uuid
            )
        except ClientContact.DoesNotExist:
            self.client_contact = None

        try:
            self.provider_contact: Optional[
                ProviderContact
            ] = ProviderContact.objects.get(user=user)
        except ProviderContact.DoesNotExist:
            self.provider_contact = None

        self._validate()

    def _validate(self):
        if self.client_contact and self.provider_contact:
            logger.error(
                "User %s is both a client contact and a provider contact",
                self.user,
            )

    @property
    def role(self) -> Optional[Role]:
        self._validate()
        if self.user.is_superuser:
            return Role.ADMIN
        if self.client_contact:
            return Role.CLIENT_CONTACT
        if self.provider_contact:
            return Role.PROVIDER_CONTACT
        else:
            return None

    @property
    def client_or_provider_contact(
        self,
    ) -> "Optional[Union[ClientContact, ProviderContact]]":
        self._validate()
        return self.client_contact or self.provider_contact or None


def get_role(user) -> Optional[Role]:
    return UserRole(user).role


def get_role_from_http_request(request: HttpRequest) -> Optional[Role]:
    cache_attrname = "_owldock_user_role"
    if not hasattr(request, cache_attrname):
        setattr(request, cache_attrname, get_role(request.user))
    return getattr(request, cache_attrname)
