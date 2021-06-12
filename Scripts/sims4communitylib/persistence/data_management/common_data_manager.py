"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict, Any, Type, Tuple

from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.persistence.data_stores.common_data_store import CommonDataStore
from sims4communitylib.persistence.persistence_services.common_persistence_service import CommonPersistenceService


class CommonDataManager(HasLog):
    """CommonDataManager()

    Manage a storage of data.

    """
    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return super().mod_identity

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return super().log_identifier

    def __init__(self, identifier: str=None) -> None:
        super().__init__()
        self._identifier = identifier
        self.__data_store_data = None
        self.__data_stores = dict()
        self._loaded = False
        self._can_be_saved = True
        self._persistence_service = None

    @property
    def _can_be_saved(self) -> bool:
        return self.__can_be_saved

    @_can_be_saved.setter
    def _can_be_saved(self, val: bool):
        self.__can_be_saved = val

    @property
    def persistence_services(self) -> Tuple[CommonPersistenceService]:
        """A collection of services that save and load data for the manager using the Mod Identity of the manager.

        .. note:: The precedence of data being loaded/saved is in the order you return them in.\
                  For example, with (CommonHiddenHouseholdPersistenceService, CommonFilePersistenceService), data loaded via the file will override data loaded via the hidden household

        :return: A collection of persistence services.
        :rtype: Tuple[CommonPersistenceService]
        """
        raise NotImplementedError()

    @property
    def _data_store_data(self) -> Dict[str, Dict[str, Any]]:
        """
        Data stores owned by a Mod in serializable form organized by identifiers.

        .. note:: The Key is the identifier of a setting collection. The value is the library of settings related to the setting collection.

        :return: Data stores in serializable form organized by a Sub Name.
        :rtype: Dict[str, Dict[str, Any]]
        """
        if not self._loaded or self.__data_store_data is None:
            self.load()
        return self.__data_store_data

    @property
    def _data_stores(self) -> Dict[str, CommonDataStore]:
        """

        Data stores owned by a Mod organized by identifiers

        .. note:: The Key is the identifier of a setting collection. The value is the library of settings related to the setting collection.

        :return: Data stores owned by a Mod organized by identifiers
        :rtype: Dict[str, CommonDataStore]
        """
        return self.__data_stores

    def get_data_store_by_type(self, data_store_type: Type[CommonDataStore]) -> CommonDataStore:
        """get_data_store_by_type(data_store_type)

        Retrieve a data store by its type.

        .. note:: This will also add the data store using the type if it does not exist already.

        :param data_store_type: The type of data store.
        :type data_store_type: Type[CommonDataStore]
        :return: The data store.
        :rtype: CommonDataStore
        """
        name = data_store_type.get_identifier()
        if name in self._data_stores:
            return self._data_stores[name]
        default_data_store: CommonDataStore = data_store_type()
        if name not in self._data_store_data:
            self._data_store_data[name] = dict()

        default_data_store.update_data(self._data_store_data[name])
        self.log.format_with_message('Created data store', name=default_data_store.get_identifier())
        self._data_store_data[name] = default_data_store.get_store_data_for_persistence()
        self._data_stores[name] = default_data_store
        return self._data_stores[name]

    def load(self) -> None:
        """load()

        Load data into the data manager.
        """
        if self._loaded:
            return
        try:
            self.log.debug('Loading data.')
            self.__data_store_data = self._load()
            self._loaded = True
        except Exception as ex:
            self.log.error('Error occurred while loading data \'{}\'.'.format(self.__repr__()), exception=ex)
            self.__data_store_data = dict()
            self._loaded = True

    def reload(self) -> None:
        """reload()

        Reloads data into the data manager.
        """
        self._loaded = False
        self.load()

    def save(self) -> bool:
        """save()

        Save data from the data manager.

        :return: True, if save was successful. False, if not.
        :rtype: bool
        """
        try:
            self.log.debug('Saving data.')
            # Update global data with data from the data stores.
            for (name, data_store) in self._data_stores.items():
                data_store: CommonDataStore = data_store
                self._data_store_data[name] = data_store.get_store_data_for_persistence()
            return self._save()
        except Exception as ex:
            self.log.error('Error occurred while saving data \'{}\'.'.format(self.__repr__()), exception=ex)
        return False

    def clear(self) -> None:
        """clear()

        Clear all data from the data manager.
        """
        self.__data_store_data = dict()
        self.__data_stores = dict()
        self._loaded = False

    def remove_all_data(self, prevent_save: bool=False) -> bool:
        """remove_all_data(prevent_save=False)

        Reset the data store to default values and remove persisted files.

        :param prevent_save: If True, when the game is saved, the data will not be persisted.
        :type prevent_save: bool
        :return: True, if all data was successfully removed. False, if not.
        :rtype: bool
        """
        try:
            self.__data_store_data = dict()
            self.__data_stores = dict()
            if prevent_save:
                self._can_be_saved = False
            return self._remove()
        except Exception as ex:
            self.log.error('Error while resetting settings.', exception=ex)
        return False

    def remove_data_store_by_name(self, name: str) -> bool:
        """remove_data_store_by_name(name)

        Remove a data store by its name.

        :param name: The name of a data store.
        :param name: str
        :return: True, if successfully removed. False, if not.
        :rtype: bool
        """
        if name in self._data_stores:
            del self._data_stores[name]
        if name in self._data_store_data:
            del self._data_store_data[name]
        return True

    def _load(self) -> Dict[str, Dict[str, Any]]:
        data = dict()
        for persistence_service in self.persistence_services:
            loaded_data = persistence_service.load(self.mod_identity, identifier=self._identifier)
            self.log.format_with_message('Loaded data.', loaded_data=loaded_data)
            data.update(loaded_data)
        return data

    def _save(self) -> bool:
        if not self._can_be_saved:
            return False
        success = True
        self.log.format_with_message('Save data.', save_data=self._data_store_data)
        for persistence_service in self.persistence_services:
            success = persistence_service.save(self.mod_identity, self._data_store_data, identifier=self._identifier)
            if not success:
                success = False
        return success

    def _remove(self) -> bool:
        success = True
        for persistence_service in self.persistence_services:
            success = persistence_service.remove(self.mod_identity, identifier=self._identifier)
            if not success:
                success = False
        return success

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return 'Data Manager: \'{}\'\n Data Stores:\n{}'.format(repr(self.mod_identity), self._data_stores)
