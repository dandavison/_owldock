import logging
from enum import Enum
from typing import Optional

logger = logging.getLogger(__file__)


class Role(Enum):
    CLIENT_CONTACT = "Client Contact"
    PROVIDER_CONTACT = "Provider Contact"


def get_role(user) -> Optional[Role]:
    from client.models import ClientContact
    from app.models import ProviderContact

    is_client_contact = ClientContact.objects.filter(user_id=user.uuid).exists()
    is_provider_contact = ProviderContact.objects.filter(user_id=user.uuid).exists()
    if is_client_contact and is_provider_contact:
        logger.error(
            "User %s is in both client-contact and provider-contact groups",
            user,
        )
        return None
    elif is_client_contact:
        return Role.CLIENT_CONTACT
    elif is_provider_contact:
        return Role.PROVIDER_CONTACT
    else:
        return None
