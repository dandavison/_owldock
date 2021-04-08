import random
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from app.models import Process, Provider, ProviderContact
from client.models import Case, Applicant, ClientProviderRelationship


class Command(BaseCommand):
    @atomic
    def handle(self, *args, **kwargs):
        self._create_cases(100)

    def _create_cases(self, n: int):
        for applicant in Applicant.objects.all():
            client = applicant.employer
            valid_client_contacts = client.clientcontact_set.all()
            provider_ids = [
                r.provider_id
                for r in ClientProviderRelationship.objects.filter(client_id=client.id)
            ]
            valid_providers = Provider.objects.filter(id__in=provider_ids)
            valid_provider_contacts = ProviderContact.objects.filter(
                provider__in=valid_providers
            )
            valid_processes = Process.objects.filter(
                route__providers__in=valid_providers
            )

            client_contact = random.choice(list(valid_client_contacts))
            provider_contact = random.choice(list(valid_provider_contacts))
            process = random.choice(list(valid_processes))

            now = datetime.now()
            target_entry_date = now + timedelta(days=int(random.uniform(10, 600)))
            target_exit_date = target_entry_date + timedelta(
                days=int(random.uniform(50, 600))
            )

            case = Case.objects.create(
                client_contact_id=client_contact.id,
                applicant_id=applicant.id,
                process_id=process.id,
                target_entry_date=target_entry_date,
                target_exit_date=target_exit_date,
            )
            for i, process_step in enumerate(process.steps.order_by("sequence_number")):
                case.steps.create(
                    process_step_id=process_step.id,
                    sequence_number=i,
                    provider_contact_id=provider_contact.id,
                )
