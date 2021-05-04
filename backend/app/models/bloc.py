from typing import List, Type, Union

from django.db.models import QuerySet

from app.models import Country


# TODO: interface/protocol


class EU:
    name = "EU"
    display_name = "EU"
    _COUNTRY_NAMES = [
        "Austria",
        "Belgium",
        "Bulgaria",
        "Croatia",
        "Cyprus",
        "Czechia",
        "Denmark",
        "Estonia",
        "Finland",
        "France",
        "Germany",
        "Greece",
        "Hungary",
        "Ireland",
        "Italy",
        "Latvia",
        "Lithuania",
        "Luxembourg",
        "Malta",
        "Netherlands",
        "Poland",
        "Portugal",
        "Romania",
        "Slovakia",
        "Slovenia",
        "Spain",
        "Sweden",
    ]

    @staticmethod
    def countries() -> "QuerySet[Country]":
        return Country.objects.filter(name__in=EU._COUNTRY_NAMES)


class NonEU:
    name = "NON_EU"
    display_name = "non-EU"

    @staticmethod
    def countries() -> "QuerySet[Country]":
        return Country.objects.exclude(name__in=EU._COUNTRY_NAMES)


BlocType = Union[Type[EU], Type[NonEU]]


class Blocs:
    blocs: List[BlocType] = [EU, NonEU]

    @classmethod
    def choices(cls):
        return [(b.name, b.display_name) for b in cls.blocs]

    @classmethod
    def get_by_name(cls, name: str) -> BlocType:
        [bloc] = [b for b in cls.blocs if b.name == name]
        return bloc
