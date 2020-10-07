"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict, Any


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
        raise NotImplementedError('Missing get_identifier class method in \'{}\'.'.format(cls.__name__))

    @property
    def _version(self) -> int:
        raise NotImplementedError('Missing _version property in \'{}\'.'.format(self.__class__.__name__))

    @property
    def _default_data(self) -> Dict[str, Any]:
        raise NotImplementedError('Missing _default_data property in \'{}\''.format(self.__class__.__name__))

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

    def set_value_by_key(self, key: str, value: Any):
        """set_value_by_key(key, value)

        Set data in storage by its key.

        :param key: An identifier.
        :type key: str
        :param value: A value.
        :type value: Any
        """
        self._storage[key] = value

    def get_value_by_key(self, key: str) -> Any:
        """get_value_by_key(key)

        Get data from storage by its key.

        :param key: An identifier.
        :type key: str
        :return: The value assigned to the key or the default value if not found.
        :rtype: Any
        """
        if key not in self._storage:
            self._storage[key] = self.get_default_value_by_key(key)
        return self._storage[key]

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

    def __repr__(self) -> str:
        return self.__class__.get_identifier()

    def __str__(self) -> str:
        return 'Data Store: \'{}\'\n Storage:\n{}'.format(str(self.__class__.get_identifier()), self._storage)
