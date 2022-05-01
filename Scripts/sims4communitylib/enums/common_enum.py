"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, List, Union, Iterator


class CommonEnumMetaclass(type):
    """A metaclass that converts the properties of a class into enum objects and allows iteration of those properties.

    """
    def __new__(mcs, cls: Any, bases: Any, class_dict: Any):
        obj_attrs = set(dir(type(cls, (object,), {})))
        enum_cls = super().__new__(mcs, cls, bases, class_dict)
        member_names = set(class_dict.keys()) - obj_attrs
        enum_dict = dict()
        for member_name in member_names:
            if callable(getattr(enum_cls, member_name)) or (member_name.startswith('_') and member_name.endswith('_')):
                continue
            enum_dict[member_name] = getattr(enum_cls, member_name)
        enum_cls._members_ = enum_dict
        expected_enum_type = mcs.get_enum_type()
        for enum_name, enum_value in enum_dict.items():
            if hasattr(enum_value, 'value'):
                enum_value = enum_value.value
            if expected_enum_type is not None and type(enum_value) != expected_enum_type:
                raise ValueError('Incorrect enum value type for class \'{}\', expected type \'{}\', got type: \'{}\'. Enum Name: \'{}\', Enum Value: \'{}\''.format(cls, expected_enum_type, type(enum_value), enum_name, enum_value))
            common_enum = mcs._get_common_enum(enum_name, enum_value, enum_cls.__name__)
            setattr(enum_cls, enum_name, common_enum)

        return enum_cls

    def __call__(cls, val: Any):
        for (enum_name, enum_value) in cls._members_.items():
            if val == enum_name or val == enum_value:
                return getattr(cls, enum_name)
        raise KeyError('Value: \'{}\' not found within class \'{}\''.format(val, cls.__name__))

    @classmethod
    def _get_common_enum(mcs, enum_name: str, enum_value: Any, class_name: str):
        from sims4communitylib.enums.enumtypes.object_enum import CommonEnumObject
        return CommonEnumObject(enum_name, enum_value, class_name)

    @classmethod
    def get_enum_type(mcs) -> Union[type, None]:
        """Retrieve the enum type of this class.

        :return: The expected enum type.
        :rtype: A base type.
        """
        return None

    def items(cls) -> List[Any]:
        """Retrieve all enum items of the class

        :return: A collection of the enum items of all enums of the class.
        :rtype: List[Any]
        """
        return [getattr(cls, name) for (name, value) in cls._members_.items()]

    def names(cls) -> List[str]:
        """Retrieve all names of all enums of the class.

        :return: A collection of the names of all enums of the class.
        :rtype: List[str]
        """
        return list(cls._members_.keys())

    def values(cls) -> List[Any]:
        """Retrieve all enum values of all enums of this class

        :return: A collection of the enum values of all enums of the class.
        :rtype: List[Any]
        """
        return list(cls._members_.values())

    def __getitem__(cls, key: str):
        return getattr(cls._members_, key.upper())

    def __iter__(cls) -> Iterator[Any]:
        return cls._members_.__iter__()

    def __len__(cls) -> int:
        return len(cls._members_)

    def __repr__(cls) -> str:
        return '{}'.format(cls.__name__)
