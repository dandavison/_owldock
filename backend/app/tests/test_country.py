from app.models import Country


def test_eu_countries_exist(load_country_fixture):
    assert {
        c.name
        for c in Country.objects.filter(name__in=Country.objects.EU_COUNTRY_NAMES)
    } == set(Country.objects.EU_COUNTRY_NAMES)
