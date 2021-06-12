"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict, Any, Tuple, Type

from sims.sim_info import SimInfo
from sims4communitylib.classes.serialization.common_serializable import CommonSerializable
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.persistence.data_management.common_data_manager import CommonDataManager
from sims4communitylib.persistence.data_stores.common_data_store import CommonDataStore
from sims4communitylib.persistence.common_sim_data_storage import CommonSimDataStorage
from sims4communitylib.persistence.data_stores.common_sim_data_store import CommonSimDataStore


class CommonPersistedSimDataStorage(CommonSimDataStorage):
    """CommonPersistedSimDataStorage(sim_info)

    A wrapper for Sim instances that allows storing of data and persisting it between saves.

    .. warning:: Data stored within will be persisted for a Save even when closing and reopening the game!
    .. warning:: DO NOT CREATE THIS CLASS DIRECTLY, IT IS ONLY MEANT TO INHERIT FROM!

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        # Inherit from CommonPersistedSimDataStorage
        class ExamplePersistedSimDataStorage(CommonPersistedSimDataStorage):
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

    :param sim_info: The SimInfo of a Sim.
    :type sim_info: SimInfo
    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        raise NotImplementedError('Missing \'{}\' inside {}.'.format(cls.get_mod_identity.__name__, cls.__class__))

    def __init__(self, sim_info: SimInfo):
        super().__init__(sim_info)
        if self.__class__.__name__ is CommonPersistedSimDataStorage.__name__:
            raise RuntimeError('{} cannot be created directly. You must inherit from it to create an instance of it.'.format(self.__class__.__name__))
        from sims4communitylib.persistence.data_management.common_data_manager_registry import CommonDataManagerRegistry
        self._data_manager_registry = CommonDataManagerRegistry()
        self.__data_manager: CommonDataManager = None
        self._data = self._load_persisted_data()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_persisted_sim_data_storage'

    @property
    def data_store_type(self) -> Type[CommonDataStore]:
        """data_store_type()

        The type of data store used for saving and loading data.

        :return: The type of the data store to use when saving and loading data.
        :rtype: Type[CommonDataStore]
        """
        return CommonSimDataStore

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

    @property
    def _persist_empty_values(self) -> bool:
        return False

    def customize_data_pre_save(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """customize_data_pre_save(data)

        A hook that allows customization of data before it is persisted/saved.

        :param data: The data intending to be saved, it is available for customization.
        :type data: Dict[str, Any]
        :return: The customized data.
        :rtype: Dict[str, Any]
        """
        data_to_save = dict(data)
        for (key, value) in data_to_save.items():
            if not hasattr(self, key):
                del data[key]
        return data

    def _save_persisted_data(self) -> None:
        data_to_save = dict()
        for data_property_name in self._data.keys():
            if data_property_name not in self.whitelist_property_names or data_property_name in self.blacklist_property_names:
                continue
            data = self._data[data_property_name]
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
            return
        if not self._persist_empty_values:
            if not data_to_save:
                self._data_manager.get_data_store_by_type(self.data_store_type).remove_data_by_key(str(self.sim_id))
                return
        self._data_manager.get_data_store_by_type(self.data_store_type).set_value_by_key(str(self.sim_id), data_to_save)

    def _load_persisted_data(self) -> Dict[str, Any]:
        return self._data_manager.get_data_store_by_type(self.data_store_type).get_value_by_key(str(self.sim_id))
