"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""


class CommonWeightedValue:
    """ A value with a weight. To be used in conjunction with other CommonWeightedValueTally. """
    def __init__(self, value: float=0.0, weight: float=1.0):
        if value is None:
            raise AssertionError('Value is None')
        if weight is None:
            raise AssertionError('Weight is None')
        self._value = value
        self._weight = weight

    @property
    def value(self) -> float:
        """ The value. """
        return self._value

    @property
    def weight(self) -> float:
        """ The weight. """
        return self._weight

    def __add__(self, other: 'CommonWeightedValue') -> 'CommonWeightedValue':
        return CommonWeightedValue(value=self.value + other.value, weight=self.weight + other.weight)

    def __sub__(self, other: 'CommonWeightedValue') -> 'CommonWeightedValue':
        return CommonWeightedValue(value=self.value - other.value, weight=self.weight - other.weight)

    def __mul__(self, other: 'CommonWeightedValue') -> 'CommonWeightedValue':
        return CommonWeightedValue(value=self.value * other.value, weight=self.weight * other.weight)

    def has_value(self) -> bool:
        """ Determine if this weighted value has a value. """
        return self.value != 0.0

    def has_weight(self) -> bool:
        """ Determine if this weighted value has a weight. """
        return self.weight > 0.0

    @staticmethod
    def create_empty() -> 'CommonWeightedValue':
        """ Create an empty CommonWeightedValue. """
        return CommonWeightedValue(value=0.0, weight=1.0)

    def __str__(self) -> str:
        return 'Weighted Value:\n Value: {}\n Weight: {}'.format(self.value, self.weight)

    def __repr__(self) -> str:
        return 'value_{}_weight_{}'.format(repr(self.value), repr(self.weight))
