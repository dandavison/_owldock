from typing import Dict, Iterable, Set

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

    def __init__(self, bases: Dict[str, Iterable[str]], universe: Iterable[str]):
        self.indices = {a: i for i, a in enumerate(sorted(universe))}
        self.universe = set(universe)
        self.size = len(set(universe))
        self.bases: Dict[str, np.ndarray] = {
            name: self._make_bitvector(set(x)) for name, x in bases.items()
        }

    def _make_bitvector(self, x: Set[str]) -> np.ndarray:
        indices = [self.indices[a] for a in x]
        v = np.zeros(len(self.universe), dtype=bool)
        v[indices] = 1
        return v

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
        v = self._make_bitvector(x)
        no_edits = np.zeros(self.size, dtype=bool)
        min_name, min_n_edits, min_edits = (
            "",
            len(self.universe) + 1,
            (no_edits, no_edits),
        )
        for name, base_v in self.bases.items():
            additions = v & ~base_v
            subtractions = ~v & base_v
            n_edits = additions.sum() + subtractions.sum()
            if n_edits < min_n_edits:
                min_name, min_n_edits, min_edits = (
                    name,
                    n_edits,
                    (additions, subtractions),
                )
        return self._make_description(min_name, *min_edits)

    def _make_description(
        self, base_name: str, additions: np.ndarray, subtractions: np.ndarray
    ) -> str:
        name = base_name
        if subtractions.any():
            name += f" - {subtractions.sum()}"
        if additions.any():
            name += f" + {additions.sum()}"
        return name
