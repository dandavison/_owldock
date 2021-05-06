import random
from datetime import timedelta
from decimal import Decimal

import factory
from django.utils import timezone

from app.models import Country
from immigration.models import (
    IssuedDocument,
    IssuedDocumentType,
    Location,
    Move,
    ProcessRuleSet,
    ProcessStep,
    Route,
    ServiceItem,
)
from owldock.tests.factories import BaseModelFactory


class MoveFactory(factory.Factory):
    class Meta:
        model = Move

    host_country = factory.LazyAttribute(
        lambda _: random.choice(list(Country.objects.all()))
    )
    target_entry_date = factory.LazyAttribute(
        lambda _: timezone.now() + timedelta(days=100)
    )
    target_exit_date = factory.LazyAttribute(
        lambda obj: obj.target_entry_date + timedelta(days=100)
    )
    activity = "Sculptor"
    contract_location = factory.LazyAttribute(lambda _: random.choice(Location.choices))
    payroll_location = factory.LazyAttribute(lambda _: random.choice(Location.choices))
    nationalities = factory.LazyAttribute(
        lambda _: [random.choice(list(Country.objects.all()))]
    )


class RouteFactory(BaseModelFactory):
    class Meta:
        model = Route

    name = "Work Permit"
    host_country = factory.LazyAttribute(
        lambda _: random.choice(list(Country.objects.all()))
    )


class ProcessRuleSetFactory(BaseModelFactory):
    class Meta:
        model = ProcessRuleSet

    route = factory.SubFactory(RouteFactory)
    contract_location = factory.LazyAttribute(
        lambda _: random.choice(Location.choices)[0]
    )
    payroll_location = factory.LazyAttribute(
        lambda _: random.choice(Location.choices)[0]
    )
    minimum_salary = factory.LazyAttribute(
        lambda _: Decimal(random.uniform(0.00, 10000.00))
    )
    duration_min_days = factory.LazyAttribute(lambda _: random.choice(range(0, 100)))
    duration_max_days = factory.LazyAttribute(
        lambda obj: obj.duration_min_days + random.choice(range(0, 100))
    )
    intra_company_moves_only = factory.LazyAttribute(
        lambda _: random.choice([True, False])
    )

    @factory.post_generation
    def nationalities(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for country in extracted:
                self.nationalities.add(country)

    @factory.post_generation
    def home_countries(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for country in extracted:
                self.home_countries.add(country)


class ProcessStepFactory(BaseModelFactory):
    class Meta:
        model = ProcessStep

    process_rule_set = factory.SubFactory(ProcessRuleSetFactory)
    name = "Fake Process Step"
    sequence_number = 1
    # TODO: issued_documents
    estimated_min_duration_days = factory.LazyAttribute(
        lambda _: random.choice(range(1, 30))
    )
    estimated_max_duration_days = factory.LazyAttribute(
        lambda obj: obj.estimated_min_duration_days + random.choice(range(1, 30))
    )
    applicant_can_enter_host_country_after = factory.LazyAttribute(
        lambda _: random.choice([True, False])
    )
    applicant_can_work_in_host_country_after = factory.LazyAttribute(
        lambda _: random.choice([True, False])
    )
    required_only_if_payroll_location = factory.LazyAttribute(
        lambda _: random.choice(Location.choices)[0]
    )
    required_only_if_duration_exceeds = factory.LazyAttribute(
        lambda _: random.choice(range(0, 100))
    )

    @factory.post_generation
    def serviceitem(self, create, extracted, **kwargs):
        if not create:
            return

        serviceitem_description = extracted or self.name
        ServiceItemFactory.create(
            process_step=self, description=serviceitem_description
        )

    @factory.post_generation
    def required_only_if_nationalities(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for country in extracted:
                self.required_only_if_nationalities.add(country)


class ServiceItemFactory(BaseModelFactory):
    class Meta:
        model = ServiceItem

    process_step = factory.SubFactory(ProcessStepFactory)
    description = "Fake Process Step Service Item"


class IssuedDocumentTypeFactory(BaseModelFactory):
    class Meta:
        model = IssuedDocumentType

    name = "Visa"


class IssuedDocumentFactory(BaseModelFactory):
    class Meta:
        model = IssuedDocument

    issued_document_type = factory.SubFactory(IssuedDocumentTypeFactory)
    process_step = factory.SubFactory(ProcessStepFactory)
    proves_right_to_enter = factory.LazyAttribute(
        lambda _: random.choice([True, False])
    )
    proves_right_to_reside = factory.LazyAttribute(
        lambda _: random.choice([True, False])
    )
    proves_right_to_work = factory.LazyAttribute(lambda _: random.choice([True, False]))
