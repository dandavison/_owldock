from datetime import datetime

from django.utils import timezone

from . import models
from .types import Country


class ClientContact_(models.ClientContact):
    class Meta:
        proxy = True

    def initiate_case(
        self,
        employee_id: int,
        process_id: int,
        host_country: Country,
        target_entry_date: datetime,
    ) -> models.Case:
        """
        Create a case associated with the current client contact,
        but not yet associated with any provider.
        """
        now = timezone.now()
        return models.Case.objects.create(
            created_at=now,
            modified_at=now,
            client_contact=self,
            employee_id=employee_id,
            process_id=process_id,
            host_country=host_country,
            target_entry_date=target_entry_date,
            progress=0.0,
        )
