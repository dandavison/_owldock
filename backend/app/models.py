from pprint import pformat

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id})"


class Client(BaseModel):
    name = models.CharField(max_length=128)


class ClientContact(BaseModel):
    user = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.deletion.CASCADE)


class Provider(BaseModel):
    name = models.CharField(max_length=128)


class ProviderContact(BaseModel):
    user = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.deletion.CASCADE)


class Employee(BaseModel):
    user = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
    employer = models.ForeignKey(Client, on_delete=models.deletion.CASCADE)
    home_country = models.CharField(max_length=128)


class Activity(BaseModel):
    name = models.CharField(max_length=128)


class Process(BaseModel):
    name = models.CharField(max_length=128)
    activities = models.ManyToManyField(Activity)


class Case(BaseModel):
    # TODO: created_by (ClientContact or User?)

    # A case is initiated by a client_contact and it will usually stay non-null.
    # It may become null if a ClientContact ceases to be employed by a Client.
    client_contact = models.ForeignKey(
        ClientContact, null=True, on_delete=models.deletion.SET_NULL
    )
    # A case is born without a provider_contact; one is assigned later.
    provider_contact = models.ForeignKey(
        ProviderContact, null=True, on_delete=models.deletion.SET_NULL
    )
    # A case is always associated with an employee.
    employee = models.ForeignKey(Employee, on_delete=models.deletion.CASCADE)

    # A case is always associated with a process
    process = models.ForeignKey(Process, on_delete=models.deletion.PROTECT)

    # TODO: what is this?
    service = models.CharField(max_length=128)

    # Case data
    host_country = models.CharField(max_length=128)
    target_entry_date = models.DateField()
    status = models.CharField(max_length=128)

    # TODO: compute
    progress = models.FloatField()
