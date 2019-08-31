from typing import Any
from sims4communitylib.enums.common_enum import CommonEnumMetaclass


class CommonFloatEnum(float):
    """
        An enum that holds a integer value.
    """
    def __init__(self, enum_name: str, enum_value: float):
        super().__init__()
        self._name = enum_name
        self._value = enum_value

    def __new__(cls, _, enum_value: float):
        return super().__new__(cls, enum_value)

    @property
    def name(self) -> str:
        """
            The name of the enum.
        :return: The name of this enum.
        """
        return self._name

    @property
    def value(self) -> float:
        """
            The value of the enum.
        :return: The value of the enum.
        """
        return self._value

    def __eq__(self, other: Any):
        other_value = other
        if hasattr(other, 'value'):
            other_value = other.value
        return self.value.__eq__(other_value)

    def __repr__(self):
        return '<{} {}:{}>'.format(self.__class__.__name__, self.name, self.value)

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash(self.value)


class CommonEnumFloatMetaclass(CommonEnumMetaclass):
    """
        A metaclass for float enums.
    """
    @classmethod
    def get_enum_type(mcs):
        """
            Retrieve the expected enum type of this enum.
        :return: The expect enum type
        """
        return float

    @classmethod
    def _get_common_enum(mcs, enum_name: str, enum_value: float):
        return CommonFloatEnum(enum_name, enum_value)
