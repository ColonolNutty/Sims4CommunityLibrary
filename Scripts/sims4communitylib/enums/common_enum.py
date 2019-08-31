"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, TypeVar, Generic, Dict, List, Union, Tuple

CommonEnumType = TypeVar('CommonEnumType')


class CommonEnum(Generic[CommonEnumType]):
    """
        An enum that holds a integer value.
    """
    def __init__(self, enum_name: str, enum_value: CommonEnumType):
        super().__init__()
        self._name = enum_name
        self._value = enum_value

    def __new__(cls, _, enum_value: CommonEnumType) -> 'CommonEnum':
        return super().__new__(cls, enum_value)

    @property
    def item(self) -> Tuple[str, CommonEnumType]:
        """
            The name and value of the enum.
        :return: A tuple containing the name and value.
        """
        return self.name, self.value

    @property
    def name(self) -> str:
        """
            The name of the enum.
        :return: The name of this enum.
        """
        return self._name

    @property
    def value(self) -> CommonEnumType:
        """
            The value of the enum.
        :return: The value of the enum.
        """
        return self._value

    def __eq__(self, other: Any) -> bool:
        other_value = other
        if hasattr(other, 'value'):
            other_value = other.value
        return self.value.__eq__(other_value)

    def __repr__(self) -> str:
        return '<CommonEnum {}:{}>'.format(self.name, self.value)

    def __str__(self) -> str:
        return self.__repr__()

    def __hash__(self):
        return hash(self.value)


class CommonEnumMetaclass(type):
    """
        A common metaclass for all Enum metaclass types.
    """
    def __new__(mcs, cls, bases, class_dict):
        obj_attrs = set(dir(type(cls, (object,), {})))
        enum_cls = super().__new__(mcs, cls, bases, class_dict)
        member_names = set(class_dict.keys()) - obj_attrs
        enum_dict = {}
        for member_name in member_names:
            if callable(getattr(enum_cls, member_name)) or (member_name.startswith('_') and member_name.endswith('_')):
                continue
            enum_dict[member_name] = getattr(enum_cls, member_name)
        enum_cls._enum_items = enum_dict
        expected_enum_type = mcs.get_enum_type()
        for enum_name, enum_value in enum_dict.items():
            if expected_enum_type is not None and type(enum_value) != expected_enum_type:
                raise ValueError('Incorrect enum value type for enum class \'{}\', expected type \'{}\', got type: \'{}\'. Enum Name: \'{}\', Enum Value: \'{}\''.format(cls, expected_enum_type, type(enum_value), enum_name, enum_value))
            if expected_enum_type is None:
                common_enum = CommonEnum[Any](enum_name, enum_value)
            else:
                common_enum = CommonEnum[expected_enum_type](enum_name, enum_value)
            setattr(enum_cls, enum_name, common_enum)

        return enum_cls

    @classmethod
    def get_enum_type(mcs) -> Union[type, None]:
        """
            Retrieve the expected enum type of this enum.
        :return: The expect enum type
        """
        return None

    def items(cls) -> Dict[str, CommonEnum]:
        """
            Retrieve all enums of this class
        :return: A dictionary of enum name/values
        """
        return cls._enum_items

    def names(cls) -> List[str]:
        """
            Retrieve all names of all enums of this class
        :return: A list of strings
        """
        return list(cls._enum_items.keys())

    def values(cls) -> List[CommonEnum]:
        """
            Retrieve all names of all enums of this class
        :return: A list of strings
        """
        return list(cls._enum_items.values())

    def __getitem__(cls, key: str) -> Union[CommonEnum, None]:
        return getattr(cls._enum_items, key.upper(), None)

    def __iter__(cls):
        return cls._enum_items.__iter__()

    def __len__(cls) -> int:
        return len(cls._enum_items)

    def __repr__(cls) -> str:
        return '{}: {}'.format(cls.__name__, cls._enum_items)


class CommonEnumIntMetaclass(CommonEnumMetaclass):
    """
        A metaclass for integer enums.
    """
    @classmethod
    def get_enum_type(mcs) -> type:
        """
            Retrieve the expected enum type of this enum.
        :return: The expect enum type
        """
        return int


class CommonEnumFloatMetaclass(CommonEnumMetaclass):
    """
        A metaclass for float enums.
    """
    @classmethod
    def get_enum_type(mcs) -> type:
        """
            Retrieve the expected enum type of this enum.
        :return: The expect enum type
        """
        return float


class CommonEnumStringMetaclass(CommonEnumMetaclass):
    """
        A metaclass for string enums.
    """
    @classmethod
    def get_enum_type(mcs) -> type:
        """
            Retrieve the expected enum type of this enum.
        :return: The expect enum type
        """
        return str


class CommonEnumObjectMetaclass(CommonEnumMetaclass):
    """
        A metaclass for string enums.
    """
    @classmethod
    def get_enum_type(mcs) -> type:
        """
            Retrieve the expected enum type of this enum.
        :return: The expect enum type
        """
        return object
