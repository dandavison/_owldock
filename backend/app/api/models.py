from typing import List
from uuid import UUID

from pydantic.types import conint

from owldock.api.models import BaseModel


class User(BaseModel):
    uuid: UUID
    first_name: str
    last_name: str
    email: str


class Provider(BaseModel):
    uuid: UUID
    name: str
    logo_url: str


class ProviderContact(BaseModel):
    uuid: UUID
    user: User
    provider: Provider


class ProviderContactList(BaseModel):
    __root__: List[ProviderContact]


class StoredFile(BaseModel):
    uuid: UUID
    created_by: User
    media_type: str
    name: str
    size: conint(gt=0)  # type: ignore


class StoredFileList(BaseModel):
    __root__: List[StoredFile]
