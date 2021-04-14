import random

from django.db.transaction import atomic

from app.models import Process, Provider, ProviderContact
from client.models import Applicant, ClientProviderRelationship
from client.tests.fake_create_case import fake_create_case_and_offer_steps


@atomic
def create_fake_cases(self, n: int):
    for applicant in Applicant.objects.all():
        client = applicant.employer
        valid_client_contacts = client.clientcontact_set.all()
        provider_uuids = [
            r.provider_uuid
            for r in ClientProviderRelationship.objects.filter(client=client)
        ]
        valid_providers = Provider.objects.filter(uuid__in=provider_uuids)
        valid_provider_contacts = ProviderContact.objects.filter(
            provider__in=valid_providers
        )
        valid_processes = Process.objects.filter(route__providers__in=valid_providers)

        client_contact = random.choice(list(valid_client_contacts))
        provider_contact = random.choice(list(valid_provider_contacts))
        process = random.choice(list(valid_processes))
        fake_create_case_and_offer_steps(
            applicant, client_contact, process, provider_contact
        )
