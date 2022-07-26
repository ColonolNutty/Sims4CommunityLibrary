"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Tuple, Callable, TypeVar, Type, Generic

from sims4communitylib.classes.enums.common_versioned_enum_value_collection import CommonVersionedEnumValueCollection
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.enums.enumtypes.common_int_flags import CommonIntFlags
from sims4communitylib.enums.enumtypes.common_versioned_int import CommonVersionedInt
from sims4communitylib.enums.enumtypes.common_versioned_int_flags import CommonVersionedIntFlags
from sims4communitylib.systems.settings.common_settings_data_store import CommonSettingsDataStore
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils

SettingEnumType = TypeVar('SettingEnumType', CommonInt, CommonIntFlags, CommonVersionedInt, CommonVersionedIntFlags)
SettingDataStoreType = TypeVar('SettingDataStoreType', bound=CommonSettingsDataStore)
SettingEnumValueCollectionType = TypeVar('SettingEnumValueCollectionType', bound=CommonVersionedEnumValueCollection)


class CommonSettingUtils(Generic[SettingDataStoreType]):
    """ Utilities for settings. """
    @classmethod
    def get_enum_tuple_setting(cls, key: str, enum_type: Type[SettingEnumType], invalid_enum_value: SettingEnumType) -> Tuple[SettingEnumType]:
        """ Retrieve a setting that is a collection of enum values. """
        result: Tuple[SettingEnumType] = cls._get_tuple_enum_value(key, enum_type, invalid_enum_value)
        return result

    @classmethod
    def set_enum_tuple_setting(cls, key: str, value: Tuple[SettingEnumType]):
        """ Set a setting that is a collection of enum values. """
        cls._set_tuple_enum_value(key, value)

    @classmethod
    def get_enum_value_collection_setting(cls, key: str, enum_value_collection_type: Type[SettingEnumValueCollectionType]) -> SettingEnumValueCollectionType:
        """ Retrieve an enum value collection setting. """
        result: SettingEnumValueCollectionType = cls._get_enum_value_collection(key, enum_value_collection_type)
        return result

    @classmethod
    def set_enum_value_collection_setting(cls, key: str, value: SettingEnumValueCollectionType):
        """ Set an enum value collection setting. """
        cls._set_enum_value_collection(key, value)

    @classmethod
    def _get_enum_value_collection(cls, key: str, enum_value_collection_type: Type[SettingEnumValueCollectionType]) -> SettingEnumValueCollectionType:
        enum_value_collection = cls.get_value(
            key,
            encode=lambda _enum_data: _enum_data.serialize(),
            decode=lambda _enum_data: enum_value_collection_type.deserialize(_enum_data) or cls._data_store().get_default_value_by_key(key)
        )
        if not enum_value_collection:
            return cls._data_store().get_default_value_by_key(key)
        return enum_value_collection

    @classmethod
    def _set_enum_value_collection(cls, key: str, value: SettingEnumValueCollectionType) -> None:
        cls.set_value(
            key,
            value,
            encode=lambda _enum_value: _enum_value.serialize(),
        )

    @classmethod
    def _get_enum_value(cls, key: str, enum_type: Type[SettingEnumType], invalid_enum_value: SettingEnumType) -> SettingEnumType:
        return cls.get_value(
            key,
            encode=lambda _enum_val: _enum_val.name,
            decode=lambda _enum_str: CommonResourceUtils.get_enum_by_name(_enum_str, enum_type, default_value=invalid_enum_value)
        )

    @classmethod
    def _set_enum_value(cls, key: str, value: SettingEnumType):
        return cls.set_value(
            key,
            value,
            encode=lambda _enum_val: _enum_val.name,
        )

    @classmethod
    def _get_tuple_enum_value(cls, key: str, enum_type: Type[SettingEnumType], invalid_enum_value: SettingEnumType) -> Tuple[SettingEnumType]:
        enum_val_list = cls.get_value(
            key,
            encode=lambda _enum_val_list: [_enum_val.name if hasattr(_enum_val, 'name') else _enum_val for _enum_val in _enum_val_list],
            decode=lambda _str_val_list: [CommonResourceUtils.get_enum_by_name(enum_str, enum_type, default_value=invalid_enum_value) if isinstance(enum_str, str) else enum_str for enum_str in _str_val_list]
        )
        result: Tuple[SettingEnumType, ...] = tuple([enum_val for enum_val in enum_val_list if enum_val != invalid_enum_value])
        return result

    @classmethod
    def _set_tuple_enum_value(cls, key: str, value: Tuple[SettingEnumType]) -> None:
        cls.set_value(
            key,
            value,
            encode=lambda _enum_list: [enum_value.name for enum_value in _enum_list],
        )

    @classmethod
    def get_value(cls, key: str, encode: Callable[[Any], Any] = None, decode: Callable[[Any], Any] = None) -> Any:
        """Get a value using an encoding and decoding."""
        return cls._data_store().get_value_by_key(key, encode=encode, decode=decode)

    @classmethod
    def set_value(cls, key: str, value: Any, encode: Callable[[Any], Any] = None) -> Any:
        """Set a value using an encoding and decoding."""
        return cls._data_store().set_value_by_key(key, value, encode=encode)

    @classmethod
    def _data_store(cls) -> SettingDataStoreType:
        raise NotImplementedError()
