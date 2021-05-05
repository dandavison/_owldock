from app.models import bloc, Country


def test_eu_countries_exist(load_country_fixture):
    assert {
        c.name for c in Country.objects.filter(name__in=bloc.EU._COUNTRY_NAMES)
    } == set(bloc.EU._COUNTRY_NAMES)
