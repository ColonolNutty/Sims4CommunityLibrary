"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.classes.math.common_weighted_value import CommonWeightedValue


class CommonWeightedValueTally:
    """ A tally that keeps track of weighted values. """
    def __init__(self) -> None:
        self._value: CommonWeightedValue = CommonWeightedValue(value=0.0, weight=0.0)
        self._value_count: int = 0
        self._weight_count: int = 0

    def add_value(self, common_weighted_value: CommonWeightedValue):
        """ Add to the tally. """
        if common_weighted_value is None:
            return
        if common_weighted_value.has_value():
            self._value_count += 1
        if common_weighted_value.has_weight():
            self._weight_count += 1
        self._value += common_weighted_value

    def get_total_value(self) -> float:
        """ Tally up all weighted values and calculate the total. """
        total_value = self._value.value / max(1, self._value_count)
        total_weight = self._value.weight / max(1, self._weight_count)
        return total_value * total_weight

    def __str__(self) -> str:
        return 'Tally:\n  Value: {}\n  Weight: {}\n Value Count: {}\n Weight Count: {}'.format(self._value.value, self._value.weight, self._value_count, self._weight_count)

    def __repr__(self) -> str:
        return 'tally_{}_value_count_{}_weight_count_{}'.format(repr(self._value), self._value_count, self._weight_count)
