from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Any, List, Optional
from uuid import UUID

from app import api as app_api
from client import models as client_orm_models
from immigration import api as immigration_api
from owldock.api.models import BaseModel, DjangoOrmGetterDict


class Client(BaseModel):
    uuid: UUID
    name: str


class ClientProviderRelationship(BaseModel):
    uuid: UUID
    client: Client
    provider: app_api.models.Provider


class ClientProviderRelationshipList(BaseModel):
    __root__: List[ClientProviderRelationship]


class Applicant(BaseModel):
    id: int
    uuid: UUID
    user: app_api.models.User
    employer: Client
    home_country: immigration_api.models.Country
    nationalities: immigration_api.models.CountryList


class ApplicantList(BaseModel):
    __root__: List[Applicant]


class Action(BaseModel):
    display_name: str
    name: str
    url: Optional[str]


class ActionList(BaseModel):
    __root__: List[Action]


class CaseStepContract(BaseModel):
    id: Optional[int]
    case_step_uuid: Optional[UUID]
    provider_contact: app_api.models.ProviderContact
    accepted_at: Optional[datetime]
    rejected_at: Optional[datetime]


class CaseStepGetterDict(DjangoOrmGetterDict):
    def get(self, key: Any, default: Any = None) -> Any:
        # Serialize human-readable labels of enums
        if key in {"state"}:
            value = getattr(self._obj, key, default)
            return client_orm_models.State(value).label if value else None
        else:
            return super().get(key, default)


class CaseStep(BaseModel):
    uuid: Optional[UUID]
    actions: ActionList
    active_contract: Optional[CaseStepContract]
    process_step: immigration_api.models.ProcessStep
    state: str
    stored_files: app_api.models.StoredFileList

    class Config(BaseModel.Config):
        getter_dict = CaseStepGetterDict


class CaseStepList(BaseModel):
    __root__: List[CaseStep]


class Move(BaseModel):
    host_country: immigration_api.models.Country
    target_entry_date: date
    target_exit_date: date
    nationalities: Optional[immigration_api.models.CountryList]
    activity: Optional[str]
    contract_location: Optional[str]
    payroll_location: Optional[str]
    salary: Optional[Decimal]
    salary_currency: Optional[str]

    @property
    def duration(self) -> Optional[timedelta]:
        if self.target_entry_date and self.target_exit_date:
            return self.target_exit_date - self.target_entry_date
        else:
            return None


class Case(BaseModel):
    id: Optional[int]
    uuid: Optional[UUID]
    applicant: Applicant
    move: Move
    process: immigration_api.models.ProcessRuleSet
    steps: CaseStepList
    created_at: Optional[datetime]


class CaseList(BaseModel):
    __root__: List[Case]
