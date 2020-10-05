from collections.abc import Iterable
from decimal import Decimal

import statistics

class IntList(list):
    def _is_really_numbers_only(self, items):
        if isinstance(items, Iterable) and not isinstance(items, str):
            return all(self._is_really_numbers_only(item) for item in items)
        else:
            return isinstance(items, int) or isinstance(items, float) or isinstance(items, Decimal)

    def append(self, other):
        if self._is_really_numbers_only(other):
            return super().append(other)
        else:
            raise TypeError()

    def __add__(self, other):
        if self._is_really_numbers_only(other):
            return super().__add__(other)
        else:
            raise TypeError()

    def __iadd__(self, other):
        if self._is_really_numbers_only(other):
            return super().__iadd__(other)
        else:
            raise TypeError()

    @property
    def mean(self):
        items = [float(item) for item in self]
        return statistics.mean(items)

    @property
    def median(self):
        return statistics.median(self)