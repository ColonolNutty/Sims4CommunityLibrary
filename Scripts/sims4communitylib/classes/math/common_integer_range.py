"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union


class CommonIntegerRange:
    """CommonIntegerRange(min_value=None, max_value=None)

    A range with a minimum and maximum for use in calculations.

    :param min_value: The minimum threshold. Set to None if there is no minimum. Default is None.
    :type min_value: int, optional
    :param max_value: The maximum threshold. Set to None if there is no maximum. Default is None.
    :type max_value: int, optional
    """
    def __init__(self, min_value: int=None, max_value: int=None):
        self._min_value = min_value
        self._max_value = max_value

    @property
    def min_value(self) -> Union[int, None]:
        """The minimum threshold of this range.

        :return: The minimum threshold of this range.
        :rtype: Union[int, None]
        """
        return self._min_value

    @property
    def max_value(self) -> Union[int, None]:
        """The maximum threshold of this range.

        :return: The maximum threshold of this range.
        :rtype: Union[int, None]
        """
        return self._max_value

    def in_range(self, value: int, or_equal: bool=True) -> bool:
        """in_range(value, or_equal=True)

        If a Minimum and Maximum value are specified, determine if the specified value is between or equal to the Minimum and Maximum values.
        If a Maximum value is not specified, determine if the specified value is greater than or equal to the Minimum value.
        If a Minimum value is not specified, determine if the specified value is less than or equal to the Maximum value.

        :param value: The value to check.
        :type value: int
        :param or_equal: If True, the value may equal the minimum or maximum values to pass. Default is True.
        :type or_equal: bool, optional
        :return: True, if the value is within range of the Minimum and Maximum values. False, it not.
        :rtype: bool
        """
        if self.min_value is None and self.max_value is None:
            return False
        if self.min_value is None:
            if or_equal:
                return value <= self.max_value
            return value < self.max_value
        if self.max_value is None:
            if or_equal:
                return value >= self.min_value
            return value > self.min_value
        if or_equal:
            return self.min_value <= value <= self.max_value
        return self.min_value < value < self.max_value
