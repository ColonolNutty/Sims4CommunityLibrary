"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Union, Dict, Any, Iterator, TypeVar, Generic, Type

from sims4communitylib.enums.enumtypes.common_versioned_int import CommonVersionedInt
from sims4communitylib.enums.enumtypes.common_versioned_int_flags import CommonVersionedIntFlags
from sims4communitylib.classes.serialization.common_serializable import CommonSerializable
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils

CommonEnumType = TypeVar('CommonEnumType', CommonVersionedIntFlags, CommonVersionedInt)

CommonVersionedEnumValueCollectionType = TypeVar('CommonVersionedEnumValueCollectionType', bound="CommonVersionedEnumValueCollection")


class CommonVersionedEnumValueCollection(CommonSerializable, Generic[CommonEnumType]):
    """CommonVersionedEnumValueCollection(\
        enum_values,\
        version=None\
    )

    A collection of enum values with a version.

    :param enum_values: A collection of enum values.
    :type enum_values: Iterator[CommonEnumType]
    :param version: The version of the data. Default is the version of the enum.
    :type version: str, optional
    """

    def __init__(self: CommonVersionedEnumValueCollectionType, enum_values: Iterator[CommonEnumType], version: str = None):
        self._enum_values = tuple(enum_values)
        self._version = version or self.get_enum_type().get_version()

    @property
    def enum_values(self: CommonVersionedEnumValueCollectionType) -> Tuple[CommonEnumType]:
        """A collection of enum values."""
        # noinspection PyTypeChecker
        return self._enum_values

    @property
    def version(self: CommonVersionedEnumValueCollectionType) -> str:
        """The version of the enum values."""
        return self._version

    @classmethod
    def get_enum_type(cls: Type[CommonVersionedEnumValueCollectionType]) -> Type[CommonEnumType]:
        """The type of enum."""
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    def serialize(self: CommonVersionedEnumValueCollectionType) -> Union[str, Dict[str, Any]]:
        data = dict()
        data['enum_values'] = [enum_value.name for enum_value in self.enum_values]
        data['version'] = self.version
        return data

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def deserialize(cls: Type[CommonVersionedEnumValueCollectionType], data: Union[str, Dict[str, Any]]) -> Union[CommonVersionedEnumValueCollectionType, None]:
        if not hasattr(data, 'get'):
            return None
        enum_value_names = data.get('enum_values', None)
        if enum_value_names is None:
            return None

        enum_values = list()
        for enum_value_name in enum_value_names:
            enum_value = CommonResourceUtils.get_enum_by_name(enum_value_name, cls.get_enum_type(), default_value=None)
            if enum_value is None:
                continue
            enum_value = cls.get_enum_type().convert_obsolete_value(enum_value)
            enum_values.append(enum_value)

        version = data.get('version', None)
        if version is None or version != cls.get_enum_type().get_version():
            return None
        return cls(enum_values, version=version)
