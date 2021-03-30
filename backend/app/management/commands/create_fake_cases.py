import random
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from app.models import Case, Applicant, Process, Provider, ProviderContact


class Command(BaseCommand):
    @atomic
    def handle(self, *args, **kwargs):
        self._create_cases(100)

    def _create_cases(self, n: int):
        for applicant in Applicant.objects.all():
            valid_client_contacts = applicant.employer.contacts.all()
            valid_providers = Provider.objects.filter(clients=applicant.employer)
            valid_provider_contacts = ProviderContact.objects.filter(
                provider__in=valid_providers
            )
            valid_processes = Process.objects.filter(
                route__providers__in=valid_providers
            )

            client_contact = random.sample(list(valid_client_contacts), 1)[0]
            provider_contact = random.sample(list(valid_provider_contacts), 1)[0]
            process = random.sample(list(valid_processes), 1)[0]

            now = datetime.now()
            target_entry_date = now + timedelta(days=int(random.uniform(10, 600)))
            target_exit_date = target_entry_date + timedelta(
                days=int(random.uniform(50, 600))
            )

            Case.objects.create(
                client_contact=client_contact,
                provider_contact=provider_contact,
                applicant=applicant,
                process=process,
                target_entry_date=target_entry_date,
                target_exit_date=target_exit_date,
            )
