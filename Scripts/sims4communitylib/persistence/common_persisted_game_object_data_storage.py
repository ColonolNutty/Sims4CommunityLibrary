"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict, Any, Tuple, Type

from objects.game_object import GameObject
from sims4communitylib.classes.serialization.common_serializable import CommonSerializable
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.persistence.data_management.common_data_manager import CommonDataManager
from sims4communitylib.persistence.data_stores.common_data_store import CommonDataStore
from sims4communitylib.persistence.common_game_object_data_storage import CommonGameObjectDataStorage
from sims4communitylib.persistence.data_stores.common_game_object_data_store import CommonGameObjectDataStore


class CommonPersistedGameObjectDataStorage(CommonGameObjectDataStorage):
    """CommonPersistedGameObjectDataStorage(game_object)

    A wrapper for Game Object instances that allows storing of data and persisting it between saves.

    .. warning:: Data stored within will be persisted for a Save even when closing and reopening the game!
    .. warning:: DO NOT CREATE THIS CLASS DIRECTLY, IT IS ONLY MEANT TO INHERIT FROM!

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        # Inherit from CommonPersistedGameObjectDataStorage
        class ExamplePersistedGameObjectDataStorage(CommonPersistedGameObjectDataStorage):
            @classmethod
            def get_mod_identity(cls) -> CommonModIdentity:
                # !!!Override with the CommonModIdentity of your own mod!!!
                from sims4communitylib.modinfo import ModInfo
                return ModInfo.get_identity()

            @property
            def example_property_one(self) -> bool:
                # Could also be written self.get_data(default=False, key='example_property_one') and it would do the same thing.
                return self.get_data(default=False)

            @example_property_one.setter
            def example_property_one(self, value: bool):
                # Could also be written self.set_data(value, key='example_property_one') and it would do the same thing.
                self.set_data(value)

    :param game_object: An instance of a GameObject
    :type game_object: GameObject
    """
    def __init__(self, game_object: GameObject):
        super().__init__(game_object)
        if self.__class__.__name__ is CommonPersistedGameObjectDataStorage.__name__:
            raise RuntimeError('{} cannot be created directly. You must inherit from it to create an instance of it.'.format(self.__class__.__name__))
        from sims4communitylib.persistence.data_management.common_data_manager_registry import CommonDataManagerRegistry
        self._data_manager_registry = CommonDataManagerRegistry()
        self.__data_manager: CommonDataManager = None
        self._data = self._load_persisted_data()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        raise NotImplementedError('Missing \'{}\' inside {}.'.format(cls.get_mod_identity.__name__, cls.__class__))

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_persisted_game_object_data_storage'

    @property
    def data_store_type(self) -> Type[CommonDataStore]:
        """data_store_type()

        The type of data store used for saving and loading data.

        :return: The type of the data store to use when saving and loading data.
        :rtype: Type[CommonDataStore]
        """
        return CommonGameObjectDataStore

    @property
    def whitelist_property_names(self) -> Tuple[str]:
        """
        If a property is within this list, it will be persisted when saving. By default all properties are whitelisted.

        :return: A collection of property names.
        :rtype: Tuple[str]
        """
        return tuple(self._data.keys())

    @property
    def blacklist_property_names(self) -> Tuple[str]:
        """
        If a property is within this list, it will not be persisted when saving. By default no properties are blacklisted.

        :return: A collection of property names.
        :rtype: Tuple[str]
        """
        return tuple()

    @property
    def _data_manager(self) -> CommonDataManager:
        if self.__data_manager is None:
            self.__data_manager = self._data_manager_registry.locate_data_manager(self.mod_identity)
            if self.__data_manager is None:
                raise RuntimeError('Failed to locate a data manager for {}, maybe you forgot to register one?'.format(self.mod_identity.name))
        return self.__data_manager

    def _save_persisted_data(self) -> None:
        data_to_save = dict()
        for data_property_name in self._data.keys():
            if data_property_name not in self.whitelist_property_names or data_property_name in self.blacklist_property_names:
                continue
            data = self._data[data_property_name]
            data_to_save[data_property_name] = data.serialize() if isinstance(data, CommonSerializable) else data
        self._data_manager.get_data_store_by_type(self.data_store_type).set_value_by_key(str(self.game_object_id), data_to_save)

    def _load_persisted_data(self) -> Dict[str, Any]:
        return self._data_manager.get_data_store_by_type(self.data_store_type).get_value_by_key(str(self.game_object_id))
