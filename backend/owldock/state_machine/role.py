import logging
from enum import Enum
from typing import Optional

logger = logging.getLogger(__file__)


class GroupName(Enum):
    CLIENT_CONTACTS = "Client Contacts"
    PROVIDER_CONTACTS = "Provider Contacts"


class Role(Enum):
    CLIENT_CONTACT = "Client Contact"
    PROVIDER_CONTACT = "Provider Contact"


def get_role(user) -> Optional[Role]:
    # FIXME
    groups = {g.name for g in user.groups.all()}  # type: ignore
    is_client_contact = GroupName.CLIENT_CONTACTS.value in groups
    is_provider_contact = GroupName.PROVIDER_CONTACTS.value in groups
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
