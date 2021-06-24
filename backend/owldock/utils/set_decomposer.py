from typing import Iterable, Mapping, Sequence, Set

import numpy as np


class SetDecomposer:
    """
    Decompose an input subset in terms of edit operations on fixed basis subsets.

    If the minimum number of edit operations (Hamming distance) between the
    input set and any basis set exceeds `max_distance` then no decomposition is
    returned and instead the set is described by its size.

    >>> sd = SetDecomposer({"ab": "ab", "cd": "cd"}, "abcde", max_distance=1.0)
    >>> sd.decompose("a")
    'ab - 1'
    >>> sd.decompose("dce")
    'non-ab'
    >>> sd.decompose("abcd")
    'ab + 2'
    >>> sd.decompose("dc")
    'cd'
    >>> sd.decompose("dc")
    'cd'
    >>> sd.decompose("")
    ''
    >>> sd.decompose("edcab")
    '(all)'
    >>> sd = SetDecomposer({"ab": "ab", "cd": "cd"}, "abcde", max_distance=0.3)
    >>> sd.decompose("a")
    'ab - 1'
    >>> sd = SetDecomposer({"ab": "ab", "cd": "cd"}, "abcde", max_distance=0.1)
    >>> sd.decompose("a")
    '1'
    """

    _empty_description = ""
    _universe_description = "(all)"

    def __init__(
        self,
        basis: Mapping[str, Iterable[str]],
        universe: Iterable[str],
        max_distance=0.05,
    ):
        self.universe = set(universe)
        self.size = len(set(universe))
        self.indices = {a: i for i, a in enumerate(sorted(self.universe))}

        self.basis_names = list(basis.keys()) + [f"non-{name}" for name in basis.keys()]
        basis_sets = [set(x) for x in basis.values()] + [
            self.universe - set(x) for x in basis.values()
        ]
        self.basis = self._make_bitvectors(basis_sets)
        assert self.basis.shape == (len(self.basis_names), len(self.universe))
        self.max_distance = max_distance

    def _make_bitvectors(self, basis: Sequence[Set[str]]) -> np.ndarray:
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
            x,
            self.basis_names[closest],
            additions[closest],
            subtractions[closest],
        )

    def _make_description(
        self,
        x: Set[str],
        basis_set_name: str,
        additions: np.ndarray,
        subtractions: np.ndarray,
    ) -> str:
        n_additions, n_subtractions = additions.sum(), subtractions.sum()
        if n_additions + n_subtractions > len(self.universe) * self.max_distance:
            return f"{len(x)}"
        name = basis_set_name
        if n_additions:
            name += f" + {n_additions}"
        if n_subtractions:
            name += f" - {n_subtractions}"
        return name
