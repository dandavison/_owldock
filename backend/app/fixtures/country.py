import django_countries
import django_countries.fields
from django.db.transaction import atomic

from app.models import Country


@atomic
def load_country_fixture() -> None:
    print("Loading countries")
    for (code, _) in django_countries.countries:
        country = django_countries.fields.Country(code)
        Country.objects.get_or_create(
            code=country.code,
            name=country.name,
            unicode_flag=country.unicode_flag,
        )
