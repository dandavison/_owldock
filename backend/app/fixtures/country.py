import django_countries
from django.db.transaction import atomic

from app.models import Country


@atomic
def load_country_fixture() -> None:
    print("Loading countries")
    for (code, _) in django_countries.countries:
        Country.objects.get_or_create_from_code(code)
