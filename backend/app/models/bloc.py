from collections import defaultdict
from typing import Callable, Dict, Iterable, List, Tuple

from django.db.models import CharField, Manager, ManyToManyField

from app.models.country import Country
from owldock.models.base import BaseModel

# Maximum value of n for `bloc + n` to be a valid description of a set of countries.
MAX_ADDITIONAL_COUNTRIES = 10


class BlocManager(Manager):
    def make_get_from_countries(self) -> "Callable[[Iterable[Country]], List[Bloc]]":
        """
        Return a function taking as input an iterable of countries and returning
        a list of all blocs comprising precisely that set of countries.
        """
        country_ids2blocs = self.get_country_ids2blocs()

        def get_from_countries(countries: Iterable[Country]) -> List[Bloc]:
            return country_ids2blocs.get(tuple(sorted(c.id for c in countries)), [])

        return get_from_countries

    def make_get_description_from_countries(
        self,
    ) -> "Callable[[Iterable[Country]], str]":
        """
        Return a function taking as input an iterable of countries and returning
        a string describing the set of countries in terms of blocs.
        """
        country_ids2blocs = self.get_country_ids2blocs()
        all_country_ids = set(Country.objects.values_list("id", flat=True))
        country_ids2bloc_complements = {
            tuple(sorted(all_country_ids - set(ids))): blocs
            for ids, blocs in country_ids2blocs.items()
        }

        def get_from_countries(countries: Iterable[Country]) -> str:
            _query_ids = [c.id for c in countries]
            exact_matches = country_ids2blocs.get(tuple(sorted(_query_ids)))
            if exact_matches:
                return "/".join(b.name for b in exact_matches)
            exact_complement_matches = country_ids2bloc_complements.get(
                tuple(sorted(_query_ids))
            )
            if exact_complement_matches:
                return "/".join(f"non-{b.name}" for b in exact_complement_matches)
            query_ids = set(_query_ids)
            for _ids, blocs in country_ids2blocs.items():
                ids = set(_ids)
                if ids < query_ids:
                    n_additional = len(query_ids - ids)
                    if n_additional <= MAX_ADDITIONAL_COUNTRIES:
                        return f"{'/'.join(b.name for b in blocs)} + {n_additional}"
            return f"{len(query_ids)}"

        return get_from_countries

    def get_bloc_id2country_ids(self) -> "Dict[int, List[int]]":
        bloc_id2country_ids = defaultdict(list)
        for bloc_id, country_id in Bloc.countries.through.objects.values_list(
            "bloc_id", "country_id"
        ):
            bloc_id2country_ids[bloc_id].append(country_id)
        return dict(bloc_id2country_ids)

    def get_country_ids2blocs(self) -> "Dict[Tuple[int], List[Bloc]]":
        bloc_id2bloc = {b.id: b for b in Bloc.objects.all()}
        country_ids2blocs = defaultdict(list)
        for bloc_id, country_ids in self.get_bloc_id2country_ids().items():
            country_ids2blocs[tuple(sorted(country_ids))].append(bloc_id2bloc[bloc_id])
        return dict(country_ids2blocs)


class Bloc(BaseModel):
    name = CharField(help_text="The name of this bloc", max_length=128)
    countries = ManyToManyField(Country, blank=True)

    objects = BlocManager()
