import uuid
from typing import Optional

from django_tools.middlewares.ThreadLocal import get_current_user


def get_current_user_uuid() -> Optional[uuid.UUID]:
    user = get_current_user()
    return user.uuid if user else None
