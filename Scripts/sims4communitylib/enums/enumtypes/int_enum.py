"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from sims4communitylib.enums.common_enum import CommonEnumMetaclass


class CommonEnumInt(int):
    """
        An enum that holds an integer value.
    """
    def __init__(self, enum_name: str, enum_value: int, class_name: str):
        super().__init__()
        self._name = enum_name
        self._value = enum_value
        self._class_name = class_name

    def __new__(cls, _, enum_value: int, class_name: str):
        return super().__new__(cls, enum_value)

    @property
    def name(self) -> str:
        """
            The name of the enum.
        :return: The name of this enum.
        """
        return self._name

    @property
    def value(self) -> int:
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
        return '{}'.format(self._class_name, self.name)

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash(self.value)


class CommonEnumIntMetaclass(CommonEnumMetaclass):
    """
        A metaclass for integer enums.
    """
    @classmethod
    def get_enum_type(mcs):
        """
            Retrieve the expected enum type of this enum.
        :return: The expected enum type
        """
        return int

    @classmethod
    def _get_common_enum(mcs, enum_name: str, enum_value: int, class_name: str):
        return CommonEnumInt(enum_name, enum_value, class_name)


class CommonEnumIntBase(int, metaclass=CommonEnumIntMetaclass):
    """ A base class for integer enums. """
    def __call__(self, val) -> CommonEnumInt:
        for (enum_name, enum_value) in self.__class__._members_.items():
            if val == enum_name or val == enum_value:
                return getattr(self, enum_name)
        return val
