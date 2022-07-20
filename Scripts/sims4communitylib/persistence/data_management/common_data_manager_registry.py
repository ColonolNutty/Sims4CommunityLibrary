"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Dict, Any, Type, Callable

from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.save.events.save_loaded import S4CLSaveLoadedEvent
from sims4communitylib.events.save.events.save_saved import S4CLSaveSavedEvent
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.persistence.data_management.common_data_manager import CommonDataManager
from sims4communitylib.services.common_service import CommonService


class CommonDataManagerRegistry(CommonService, HasClassLog):
    """CommonDataManagerRegistry()

    A registry that maintains data managers for saving and loading of data.

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        from typing import Tuple
        from sims4communitylib.mod_support.mod_identity import CommonModIdentity
        from sims4communitylib.persistence.data_management.common_data_manager import CommonDataManager
        from sims4communitylib.persistence.data_management.common_data_manager_registry import CommonDataManagerRegistry
        from sims4communitylib.persistence.persistence_services.common_persistence_service import CommonPersistenceService


        # This attribute will register the data manager to the registry.
        # @CommonDataManagerRegistry.common_data_manager()
        # Passing an identifier argument will give a unique identifier to the data manager, but it isn't required unless you have multiple managers for your mod.
        @CommonDataManagerRegistry.common_data_manager(identifier='I_am_unique')
        class ExampleDataManager(CommonDataManager):
            # noinspection PyMissingOrEmptyDocstring
            @property
            def mod_identity(self) -> CommonModIdentity:
                # !!! Override this property using your own CommonModIdentity !!!
                return ModInfo.get_identity()

            # noinspection PyMissingOrEmptyDocstring
            @property
            def log_identifier(self) -> str:
                return 'the_example_data_manager'

            # noinspection PyMissingOrEmptyDocstring
            @property
            def persistence_services(self) -> Tuple[CommonPersistenceService]:
                from sims4communitylib.persistence.persistence_services.common_hidden_household_persistence_service import \
                    CommonHiddenHouseholdPersistenceService
                from sims4communitylib.persistence.persistence_services.common_file_persistence_service import \
                    CommonFilePersistenceService
                # The order matters. The later services will override data loaded from the earlier services. In the follow, any data loaded from the file will override any matching data that was loaded from the hidden household.
                result: Tuple[CommonPersistenceService] = (
                    # Having this will result in the data being saved to a hidden household.
                    CommonHiddenHouseholdPersistenceService(),
                    # Having this will result in the data also being saved to a file at saves\\mod_name\\do_not_remove_mod_name_author_I_am_unique_id_1234_guid_5435.json (Notice that "I_am_unique" becomes a part of the file name because it was specified as the identifier)
                    CommonFilePersistenceService()
                )
                return result

    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_data_manager_registry'

    def __init__(self) -> None:
        super().__init__()
        self._data_managers: Dict[str, CommonDataManager] = dict()

    @staticmethod
    def common_data_manager(identifier: str = None) -> Callable[[Type[CommonDataManager]], Any]:
        """common_data_manager(identifier=None)

        An attribute that will register the decorated data manager to the registry.

        :param identifier: If you need to distinguish two different data managers for your mod, this will be the unique identifier. Default is None.
        :type identifier: str, optional
        """
        def _inner_test_class(cls: Type[CommonDataManager]) -> Any:
            nonlocal identifier
            if identifier is None:
                if hasattr(cls, 'get_identifier'):
                    identifier = cls.get_identifier()
            CommonDataManagerRegistry()._register_data_manager(cls(identifier=identifier), identifier=identifier)
            return cls
        return _inner_test_class

    def _register_data_manager(self, data_manager: CommonDataManager, identifier: str = None):
        self.log.format_with_message('Registering data store.', data_store=data_manager)
        formatted_identifier = self._format_identifier(data_manager.mod_identity, identifier=identifier)
        if formatted_identifier not in self._data_managers:
            self._data_managers[formatted_identifier] = data_manager

    def save_data(self) -> None:
        """save_data()

        Save the data of all data managers.

        """
        self.log.debug('Saving data managers.')
        from sims4communitylib.persistence.common_game_object_data_storage import _CommonGameObjectDataStorageMetaclass
        for (mod_name, data_storage_library) in _CommonGameObjectDataStorageMetaclass._game_object_storage_instances.items():
            data_storage_library: Dict[int, '_CommonGameObjectDataStorageMetaclass'] = data_storage_library
            for data_storage in data_storage_library.values():
                if hasattr(data_storage, '_save_persisted_data'):
                    data_storage._save_persisted_data()
        from sims4communitylib.persistence.common_sim_data_storage import _CommonSimDataStorageMetaclass
        for (mod_name, data_storage_library) in _CommonSimDataStorageMetaclass._sim_storage_instances.items():
            data_storage_library: Dict[int, '_CommonSimDataStorageMetaclass'] = data_storage_library
            for data_storage in data_storage_library.values():
                if hasattr(data_storage, '_save_persisted_data'):
                    data_storage._save_persisted_data()
        for data_manager in self._data_managers.values():
            self.log.format_with_message('Saving data manager', data_manager=data_manager)
            data_manager.save()
        self.log.debug('Done saving data managers.')

    def clear_data(self) -> None:
        """clear_data()

        Clear all data managers in the registry.
        """
        self.log.debug('Clearing data managers.')
        from sims4communitylib.persistence.common_game_object_data_storage import _CommonGameObjectDataStorageMetaclass
        _CommonGameObjectDataStorageMetaclass._game_object_storage_instances = dict()
        from sims4communitylib.persistence.common_sim_data_storage import _CommonSimDataStorageMetaclass
        _CommonSimDataStorageMetaclass._sim_storage_instances = dict()
        for data_manager in self._data_managers.values():
            try:
                self.log.format_with_message('Saving data manager', data_manager=data_manager)
                data_manager.clear()
            except Exception as ex:
                self.log.format_error_with_message('Failed to clear data manager. An error occurred.', data_manager=data_manager, exception=ex)
        self.log.debug('Done clearing data managers.')

    def locate_data_manager(self, mod_identity: CommonModIdentity, identifier: str = None) -> Union[CommonDataManager, None]:
        """locate_data_manager(mod_identity, identifier=None)

        Locate a data manager for a mod.

        :param mod_identity: The identity of the Mod.
        :type mod_identity: CommonModIdentity
        :param identifier: If you distinguished your data manager with an identifier when registering it, provide it here to locate the correct data manager, otherwise leave it as None. Default is None.
        :type identifier: str, optional
        :return: The data manager for the specified mod with the specified identifier (if specified) or None if not found.
        :rtype: Union[CommonDataManager, None]
        """
        formatted_identifier = self._format_identifier(mod_identity, identifier=identifier)
        self.log.format_with_message('Attempting to locate data manager.', identifier=formatted_identifier)
        if formatted_identifier not in self._data_managers:
            self.log.format_with_message(f'Data manager not registered for mod \'{mod_identity.name}\', adding the default data manager.')
            return None
        self.log.debug('Located data manager.')
        return self._data_managers[formatted_identifier]

    def _format_identifier(self, mod_identity: CommonModIdentity, identifier: str = None) -> str:
        if identifier is None:
            return repr(mod_identity)
        else:
            return f'{repr(mod_identity)}_{identifier}'


# noinspection PyUnusedLocal
@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _common_save_data_on_save_saved(event_data: S4CLSaveSavedEvent) -> bool:
    CommonDataManagerRegistry().save_data()
    return True


# noinspection PyUnusedLocal
@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _common_clear_data_on_save_loaded(event_data: S4CLSaveLoadedEvent) -> bool:
    CommonDataManagerRegistry().clear_data()
    return True
