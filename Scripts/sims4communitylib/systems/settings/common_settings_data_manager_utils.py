"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Type, Union, Dict, Any, TypeVar

from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.persistence.data_management.common_data_manager_registry import CommonDataManagerRegistry
from sims4communitylib.persistence.data_stores.common_data_store import CommonDataStore
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.systems.settings.common_settings_data_manager import CommonSettingsDataManager

CommonDataStoreType = TypeVar('CommonDataStoreType', bound=CommonDataStore)


class CommonSettingsDataManagerUtils(CommonService, HasLog):
    """ Utilities to manage settings data. """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        raise NotImplementedError()

    @property
    def _data_manager_type(self) -> Type[CommonSettingsDataManager]:
        raise NotImplementedError()

    def __init__(self) -> None:
        super().__init__()
        self.__data_manager: Union[CommonSettingsDataManager, None] = None

    @property
    def _data_manager(self) -> CommonSettingsDataManager:
        """ The data manager containing data. """
        if self.__data_manager is None:
            self.__data_manager = CommonDataManagerRegistry().locate_data_manager(self.mod_identity, identifier=self._data_manager_type.get_identifier())
        return self.__data_manager

    def _get_data_store(self, data_store_type: Type[CommonDataStoreType]) -> Union[CommonDataStoreType, None]:
        return self._data_manager.get_data_store_by_type(data_store_type)

    def get_all_data(self) -> Dict[str, Dict[str, Any]]:
        """ Get all data. """
        return self._data_manager._data_store_data

    def save(self) -> bool:
        """ Save data. """
        return self._data_manager.save()

    def reset(self, prevent_save: bool = False) -> bool:
        """ Reset data. """
        return self._data_manager.remove_all_data(prevent_save=prevent_save)
