"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict, Any, Callable, Tuple

from sims4communitylib.classes.serialization.common_serializable import CommonSerializable


class CommonDataStore:
    """CommonDataStore()

    Manage a subset of data.
    """
    _VERSION = 'version'

    def __init__(self) -> None:
        self._storage = dict(self._default_data)

    @classmethod
    def get_identifier(cls) -> str:
        """ The identifier of the data store. """
        raise NotImplementedError(f'Missing get_identifier class method in \'{cls.__name__}\'.')

    @property
    def _version(self) -> int:
        raise NotImplementedError(f'Missing _version property in \'{self.__class__.__name__}\'.')

    @property
    def _default_data(self) -> Dict[str, Any]:
        raise NotImplementedError(f'Missing _default_data property in \'{self.__class__.__name__}\'')

    @property
    def _storage(self) -> Dict[str, Any]:
        """
        A storage of data organized by identifiers.

        :return: A storage of data organized by identifiers.
        :rtype: Dict[str, Any]
        """
        return self.__storage

    @_storage.setter
    def _storage(self, value: Dict[str, Any]):
        self.__storage = value

    @property
    def _persist_empty_values(self) -> bool:
        return False

    @property
    def whitelist_property_names(self) -> Tuple[str]:
        """
        If a property is within this list, it will be persisted when saving. By default all properties are whitelisted.

        :return: A collection of property names.
        :rtype: Tuple[str]
        """
        return tuple(self._storage.keys())

    @property
    def blacklist_property_names(self) -> Tuple[str]:
        """
        If a property is within this list, it will not be persisted when saving. By default no properties are blacklisted.

        :return: A collection of property names.
        :rtype: Tuple[str]
        """
        return tuple()

    def set_value_by_key(self, key: str, value: Any, encode: Callable[[Any], Any]=None):
        """set_value_by_key(key, value, encode=None)

        Set data in storage by its key.

        :param key: An identifier.
        :type key: str
        :param value: A value.
        :type value: Any
        :param encode: If specified, the data will be encoded using this function and the result will be the new data stored. Default is None.
        :type encode: Callable[[Any], Any], optional
        """
        if encode is not None:
            value = encode(value)
        self._storage[key] = value

    def get_value_by_key(self, key: str, encode: Callable[[Any], Any]=None, decode: Callable[[Any], Any]=None) -> Any:
        """get_value_by_key(key, encode=None, decode=None)

        Get data from storage by its key.

        :param key: An identifier.
        :type key: str
        :param encode: If specified, the data will be encoded using this function and the result will be the new data stored. Default is None.
        :type encode: Callable[[Any], Any], optional
        :param decode: If specified, the data will be decoded using this function and the result will be the new result of "get_data". Default is None.
        :type decode: Callable[[Any], Any], optional
        :return: The value assigned to the key or the default value if not found.
        :rtype: Any
        """
        if key not in self._storage:
            default_val = self.get_default_value_by_key(key)
            if default_val is not None:
                if encode is not None:
                    self._storage[key] = encode(default_val)
                else:
                    self._storage[key] = default_val
            return default_val
        data = self._storage.get(key)
        if decode is not None and not isinstance(data, CommonSerializable):
            decoded = decode(data)
            if isinstance(data, CommonSerializable):
                self._storage[key] = decoded
            return decoded
        return data

    def get_default_value_by_key(self, key: str) -> Any:
        """get_default_value_by_key(key)

        Get the default value

        :param key: An identifier.
        :type key: str
        :return: The default value associated with the specified key or None if no default value has been provided for the specified key.
        :rtype: Any
        """
        if key not in self._default_data:
            return None
        return self._default_data[key]

    def remove_data_by_key(self, key: str) -> bool:
        """remove_data_by_key(key)

        Remove data from storage.

        :param key: An identifier.
        :type key: str
        :return: True, if the data with the specified identifier is removed successfully. False, if not.
        :rtype: bool
        """
        if key not in self._storage:
            return False
        del self._storage[key]
        return True

    def update_data(self, data: Dict[str, Any]):
        """update_data(data)

        Replace the data contained within the data store.

        :param data: A library of data.
        :type data: Dict[str, Any]
        """

        version_name = self.__class__._VERSION

        if data is None or not data:
            self._storage = dict(self._default_data)
            if version_name not in self._storage:
                self._storage[version_name] = self._version
            return

        if version_name not in data or int(data[version_name]) != int(self._version):
            new_data = dict(data)
            default_data = dict(self._default_data)
            for (default_data_key, default_data_value) in default_data.items():
                # If Data has the key, we don't want to override it. Keep the old data.
                if default_data_key in new_data:
                    continue
                new_data[default_data_key] = default_data[default_data_key]
            new_data[version_name] = self._version
            data = new_data

        self._storage = data

    def customize_data_pre_save(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """customize_data_pre_save(data)

        A hook that allows customization of data before it is persisted/saved.

        :param data: The data intending to be saved, it is available for customization.
        :type data: Dict[str, Any]
        :return: The customized data.
        :rtype: Dict[str, Any]
        """
        return data

    def get_store_data_for_persistence(self) -> Dict[str, Any]:
        """get_store_data_for_persistence()

        :return: The data of this data store, but in an easy to serialize format.
        :rtype: Dict[str, Any]
        """
        data_to_save = dict()
        for data_property_name in self._storage.keys():
            if data_property_name not in self.whitelist_property_names or data_property_name in self.blacklist_property_names:
                continue
            data = self._storage[data_property_name]
            if self._persist_empty_values:
                data_to_save[data_property_name] = data.serialize() if isinstance(data, CommonSerializable) else data
            else:
                if data is None or (data != 0 and not isinstance(data, bool) and not data):
                    continue
                serialized_data = data.serialize() if isinstance(data, CommonSerializable) else data
                if data is None or (serialized_data != 0 and not isinstance(data, bool) and not serialized_data):
                    continue
                data_to_save[data_property_name] = serialized_data
        data_to_save = self.customize_data_pre_save(data_to_save)
        if data_to_save is None:
            return dict()
        if not self._persist_empty_values:
            if not data_to_save:
                return dict()
        return data_to_save

    def __repr__(self) -> str:
        return self.__class__.get_identifier()

    def __str__(self) -> str:
        return 'Data Store: \'{}\'\n Storage:\n{}'.format(str(self.__class__.get_identifier()), self._storage)
