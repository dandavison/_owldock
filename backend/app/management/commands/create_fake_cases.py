import random

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from app.tests.fake_create_case import fake_create_case
from app.models import Process, Provider, ProviderContact
from client.models import Applicant, ClientProviderRelationship


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
            fake_create_case(applicant, client_contact, process, provider_contact)
