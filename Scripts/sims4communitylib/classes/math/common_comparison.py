"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any


class CommonComparison:
    """A comparison that may be used in functions that require a CommonComparison object."""
    def compare(self, value_a: Any, value_b: Any) -> bool:
        """Compare two values."""
        raise NotImplementedError()


class CommonComparisonEqualTo(CommonComparison):
    """Check if A is equal to B."""

    # noinspection PyMissingOrEmptyDocstring
    def compare(self, value_a: Any, value_b: Any) -> bool:
        return value_a == value_b


class CommonComparisonGreaterThan(CommonComparison):
    """Check if A is greater than B."""

    # noinspection PyMissingOrEmptyDocstring
    def compare(self, value_a: Any, value_b: Any) -> bool:
        return value_a > value_b


class CommonComparisonLessThan(CommonComparison):
    """Check if A is less than B."""

    # noinspection PyMissingOrEmptyDocstring
    def compare(self, value_a: Any, value_b: Any) -> bool:
        return value_a < value_b


class CommonComparisonGreaterThanOrEqualTo(CommonComparison):
    """Check if A is greater than or equal to B."""

    # noinspection PyMissingOrEmptyDocstring
    def compare(self, value_a: Any, value_b: Any) -> bool:
        return value_a >= value_b


class CommonComparisonLessThanOrEqualTo(CommonComparison):
    """Check if A is less than or equal to B."""

    # noinspection PyMissingOrEmptyDocstring
    def compare(self, value_a: Any, value_b: Any) -> bool:
        return value_a <= value_b
