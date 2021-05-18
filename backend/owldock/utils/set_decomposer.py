from typing import Dict, Iterable, List

import numpy as np


class SetDecomposer:
    """
    Decompose an input subset in terms of edit operations on fixed basis subsets.

    >>> sd = SetDecomposer({"ab": "ab", "cd": "cd"}, "abcde")
    >>> sd.decompose("a")
    'ab - 1'
    >>> sd.decompose("dce")
    'cd + 1'
    >>> sd.decompose("abcd")
    'ab + 2'
    >>> sd.decompose("dc")
    'cd'
    >>> sd.decompose("")
    ''
    >>> sd.decompose("edcab")
    '(all)'
    """

    _empty_description = ""
    _universe_description = "(all)"

    def __init__(self, basis: Dict[str, Iterable[str]], universe: Iterable[str]):
        self.universe = set(universe)
        self.size = len(set(universe))
        self.indices = {a: i for i, a in enumerate(sorted(self.universe))}
        self.basis_names = list(basis.keys())
        self.basis = self._make_bitvectors(list(basis.values()))

    def _make_bitvectors(self, basis: List[Iterable[str]]) -> np.ndarray:
        bitvectors = np.zeros((len(basis), len(self.universe)), dtype=bool)
        for i, x in enumerate(basis):
            indices = [self.indices[a] for a in set(x)]
            bitvectors[i, indices] = True
        return bitvectors

    def decompose(self, x: Iterable[str]) -> str:
        """
        Return a string describing input subset x in terms of edit operations on
        basis subsets.
        """
        x = set(x)
        if x >= self.universe:
            if x == self.universe:
                return self._universe_description
            raise ValueError(
                f"Input set (length {len(x)}) is not a subset of universe "
                f"(length {len(self.universe)})"
            )
        elif not x:
            return self._empty_description
        v = self._make_bitvectors([x])
        additions = v & ~self.basis
        subtractions = ~v & self.basis
        n_edits = additions.sum(axis=1) + subtractions.sum(axis=1)
        closest = n_edits.argmin()
        return self._make_description(
            self.basis_names[closest], additions[closest], subtractions[closest]
        )

    def _make_description(
        self, base_name: str, additions: np.ndarray, subtractions: np.ndarray
    ) -> str:
        name = base_name
        if subtractions.any():
            name += f" - {subtractions.sum()}"
        if additions.any():
            name += f" + {additions.sum()}"
        return name
