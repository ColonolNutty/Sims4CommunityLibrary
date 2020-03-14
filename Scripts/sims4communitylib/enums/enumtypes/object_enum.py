"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any
from sims4communitylib.enums.common_enum import CommonEnumMetaclass


class CommonEnumObject(object):
    """CommonEnumObject(enum_name, enum_value, class_name)

    An enum that holds an object value.

    :param enum_name: The name of the enum.
    :type enum_name: str
    :param enum_value: The value of the enum.
    :type enum_value: object
    :param class_name: The name of the class containing the enum.
    :type class_name: str
    """
    def __init__(self, enum_name: str, enum_value: object, class_name: str):
        super().__init__()
        self._name = enum_name
        self._value = enum_value
        self._class_name = class_name

    def __new__(cls, _, enum_value: object, class_name: str):
        return super().__new__(cls, enum_value)

    @property
    def name(self) -> str:
        """The name of the enum.

        :return: The name of the enum.
        :rtype: str
        """
        return self._name

    @property
    def value(self) -> object:
        """The value of the enum.

        :return: The value of the enum.
        :rtype: object
        """
        return self._value

    def __eq__(self, other: Any):
        other_value = other
        if hasattr(other, 'value'):
            other_value = other.value
        return self.value.__eq__(other_value)

    def __repr__(self) -> str:
        return '{}.{}'.format(self._class_name, self.name)

    def __str__(self) -> str:
        return self.__repr__()

    def __hash__(self) -> int:
        return hash(self.value)


class CommonEnumObjectMetaclass(CommonEnumMetaclass):
    """A metaclass for object enums.

    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_enum_type(mcs) -> Any:
        return object

    @classmethod
    def _get_common_enum(mcs, enum_name: str, enum_value: object, class_name: str):
        return CommonEnumObject(enum_name, enum_value, class_name)


class CommonEnumObjectBase(object, metaclass=CommonEnumObjectMetaclass):
    """An inheritable class to turn properties of the class into object enums.

    """
    def __call__(self, val) -> CommonEnumObject:
        pass
