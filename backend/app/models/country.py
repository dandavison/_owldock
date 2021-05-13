# Regarding use of Meta.constraints rather than unique=True in the field
# declaration:
# Suppose some POST data has been received by a DRF serializer, and the plan is
# to create Service entries with get_or_create semantics. The DRF serializer
# will fail its validity check if the new Service entries look like they are
# going to try to create duplicates. But only if the unique_contraint is added
# in the Django field definition.
from collections import defaultdict

import moneyed
import pycountry
from django.db import models

from owldock.models.base import BaseModel


class Country(BaseModel):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=2)
    unicode_flag = models.CharField(max_length=2)

    _COUNTRY_ID_TO_CURRENCIES = None

    @property
    def currency(self):
        country_numeric_code = pycountry.countries.get(alpha_2=self.code).numeric
        try:
            return moneyed.get_currency(iso=country_numeric_code)
        except moneyed.CurrencyDoesNotExist:
            # A disadvantage of this method is that some countries have more
            # than one currency and we have no information about which we should
            # choose.
            if self._COUNTRY_ID_TO_CURRENCIES is None:
                self._compute_country_id_to_currencies()
                assert self._COUNTRY_ID_TO_CURRENCIES
            return sorted(self._COUNTRY_ID_TO_CURRENCIES.get(self.id, [None]))[0]

    @classmethod
    def _compute_country_id_to_currencies(cls):
        # moneyed.CURRENCIES[_3_letter_currency_code].countries is a list of
        # upper-case country names, e.g. the list of countries using the Euro.
        # It seems unfortunate that the countries are not represented by one of
        # their official codes.
        name2id = {c.name.lower(): c.id for c in cls.objects.all()}
        id2currencies = defaultdict(list)
        for currency in moneyed.CURRENCIES.values():
            for country_name in currency.countries:
                try:
                    id = name2id[country_name.lower()]
                except KeyError:
                    pass
                else:
                    id2currencies[id].append(currency)
        cls._COUNTRY_ID_TO_CURRENCIES = dict(id2currencies)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("name",),
                name="country__name__unique_constraint",
            ),
            models.UniqueConstraint(
                fields=("code",), name="country__code__unique_constraint"
            ),
        ]
        verbose_name_plural = "Countries"
