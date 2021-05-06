# type: ignore
from typing import Any, ClassVar, Dict, List, Tuple

from django.forms import ValidationError

from app.models.bloc import Blocs


class BlocChoiceFieldMixin:
    """
    A mixin for a form class that features a bloc ChoiceField adding country
    selections to a Country multiple choice (m2m) field.
    """

    _bloc_fields: ClassVar[List[Tuple[str, str]]] = []

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._set_initial_bloc_values()

    def _set_initial_bloc_values(self):
        """
        If the set of nationalities / home countries is exactly equal to one of
        the blocs, then intialise the form with that bloc selected.
        """
        bloc_countries = {b.name: set(b.countries()) for b in Blocs.blocs}
        for countries_attrname, bloc_attrname in self._bloc_fields:
            countries = set(self.initial.get(countries_attrname, []))
            for bloc in Blocs.blocs:
                if bloc_countries[bloc.name] == countries:
                    self.initial[bloc_attrname] = bloc.name
                    continue

    def clean(self) -> Dict[str, Any]:
        """
        Combine the bloc selector value with the country multiple choice
        selector value to reach a single conclusion regarding which countries
        are selected.

        We currently allow one only of the two selectors to be used.
        """
        super().clean()
        for countries_attrname, bloc_attrname in self._bloc_fields:
            if self.cleaned_data.get(bloc_attrname):
                bloc = Blocs.get_by_name(self.cleaned_data[bloc_attrname])
                if self.cleaned_data[countries_attrname] and set(
                    self.cleaned_data[countries_attrname]
                ) != set(bloc.countries()):
                    raise ValidationError(
                        "When selecting by bloc, do not use the main country selector. "
                        "If this is restrictive, please let the Owldock dev team know."
                    )
                self.cleaned_data[countries_attrname] = bloc.countries()
        return self.cleaned_data
