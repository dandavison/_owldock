import logging
from enum import Enum
from typing import Optional, Union

from django.conf import settings

logger = logging.getLogger(__file__)


class Role(Enum):
    CLIENT_CONTACT = "Client Contact"
    PROVIDER_CONTACT = "Provider Contact"


class UserRole:
    def __init__(self, user: settings.AUTH_USER_MODEL):
        from client.models import ClientContact
        from app.models import ProviderContact

        try:
            self.client_contact = ClientContact.objects.get(user_uuid=user.uuid)
        except ClientContact.DoesNotExist:
            self.client_contact = None

        try:
            self.provider_contact = ProviderContact.objects.get(user=user)
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
    def role(self) -> Role:
        self._validate()
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
