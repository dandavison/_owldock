# type: ignore
from typing import Any, ClassVar, Dict, List

from django.db.models import TextChoices
from django.forms import ChoiceField, ModelChoiceField, RadioSelect, ValidationError

from app.models import Bloc, Country


class IncludeChoices(TextChoices):
    INCLUDE = "Include"
    EXCLUDE = "Exclude"


class BlocChoiceFieldMixin:
    """
    A mixin for a form class that features a bloc ChoiceField adding country
    selections to a Country multiple choice (m2m) field.
    """

    _bloc_fields: ClassVar[List[str]] = []

    @classmethod
    def make_bloc_field(cls):
        return ModelChoiceField(
            Bloc.objects.all(),
            required=False,
            label="Bloc",
        )

    @classmethod
    def make_bloc_include_field(cls):
        return ChoiceField(
            choices=IncludeChoices.choices,
            widget=RadioSelect,
            initial=IncludeChoices.INCLUDE,
            label="",
        )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.blocs = Bloc.objects.prefetch_related("countries").all()
        self._set_initial_bloc_values()

    @property
    def _augmented_bloc_fields(self):
        for bloc_field in self._bloc_fields:
            yield bloc_field, f"{bloc_field}_bloc", f"{bloc_field}_bloc_include"

    def _set_initial_bloc_values(self):
        """
        If the set of nationalities / home countries is exactly equal to one of
        the blocs, then intialise the form with that bloc selected.
        """

        bloc_countries = {b.name: set(b.countries.all()) for b in self.blocs}
        for countries_attrname, bloc_attrname, _ in self._augmented_bloc_fields:
            countries = set(self.initial.get(countries_attrname, []))
            for bloc in self.blocs:
                if bloc_countries[bloc.name] == countries:
                    self.initial[bloc_attrname] = bloc
                    continue

    def clean(self) -> Dict[str, Any]:
        """
        Combine the bloc selector value with the country multiple choice
        selector value to reach a single conclusion regarding which countries
        are selected.

        We currently allow one only of the two selectors to be used.
        """
        super().clean()
        for (
            countries_attrname,
            bloc_attrname,
            include_attrname,
        ) in self._augmented_bloc_fields:
            if self.cleaned_data.get(bloc_attrname):
                bloc = self.cleaned_data[bloc_attrname]
                existing_countries = self.cleaned_data[countries_attrname]
                self.cleaned_data[countries_attrname] = {
                    IncludeChoices.INCLUDE: existing_countries.union(
                        bloc.countries.all()
                    ),
                    IncludeChoices.EXCLUDE: existing_countries.exclude(
                        id__in=bloc.countries.all()
                    ),
                }[self.cleaned_data[include_attrname]]
        return self.cleaned_data
