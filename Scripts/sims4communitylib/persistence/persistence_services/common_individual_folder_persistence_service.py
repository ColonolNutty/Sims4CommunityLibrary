"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from typing import Dict, Any

from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.persistence.persistence_services.common_persistence_service import CommonPersistenceService
from sims4communitylib.utils.common_json_io_utils import CommonJSONIOUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry


class CommonIndividualFolderPersistenceService(CommonPersistenceService):
    """CommonIndividualFolderPersistenceService(main_file_name='main.json', combined_file_name='combined.json', allow_duplicates_in_collections=False, data_folder_path=None)

    A service that persists data to a file within a folder on the system. It also loads all data from a folder on the system while loading the main file last.

    :param main_file_name: A file that will be loaded after the other files in the folder specified by folder_name. Default is 'main.json'.
    :type main_file_name: str, optional
    :param data_folder_path: Use to specify a custom folder path at the top level for which to save/load data to/from. Default is "Mods/mod_data".
    :type data_folder_path: str, optional
    """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'common_individual_folder_persistence_service'

    def __init__(
        self,
        main_file_name: str = 'main.json',
        data_folder_path: str = None
    ) -> None:
        super().__init__()
        self._main_file_name = main_file_name
        from sims4communitylib.utils.common_log_utils import CommonLogUtils
        self._data_folder_path = data_folder_path or CommonLogUtils.get_mod_data_location_path()

    # noinspection PyMissingOrEmptyDocstring
    def load(self, mod_identity: CommonModIdentity, identifier: str = None) -> Dict[str, Dict[str, Any]]:
        # mod_folder_persistence_service
        log = CommonLogRegistry().register_log(mod_identity, f'{mod_identity.base_namespace}_{self.log_identifier}')
        folder_path = self._folder_path(mod_identity, identifier=identifier)

        log.format_with_message('Loading data.', mod=mod_identity, folder_path=folder_path, identifier=identifier)

        if not os.path.exists(folder_path):
            log.format_with_message('No folder was found at path.', mod=mod_identity, folder_path=folder_path)
            return dict()
        file_names = list()

        main_file_path = os.path.join(folder_path, self._main_file_name)
        loaded_main_data: Dict[str, Any] = CommonJSONIOUtils.load_from_file(main_file_path)
        if loaded_main_data is None:
            log.format_with_message('Missing main data!', main_file_path=main_file_path)
            loaded_main_data = dict()

        file_names.append(self._main_file_name)

        def _on_file_read_failure(file_path: str, ex: Exception):
            log.error(f'Failed to read file with path {file_path}', exception=ex)
            return True

        loaded_data: Dict[str, Dict[str, Any]] = CommonJSONIOUtils.load_from_folder(
            folder_path,
            skip_file_names=(self._main_file_name,),
            on_file_read_failure=_on_file_read_failure
        )
        log.format_with_message('Got loaded data.', loaded_data=loaded_data)
        if loaded_data is None:
            return dict()
        data_by_file_name: Dict[str, Dict[str, Any]] = dict()
        for (key, val) in loaded_data.items():
            data_by_file_name[key] = val
            file_names.append(key)
        data_by_file_name[self._main_file_name] = loaded_main_data
        log.format_with_message('Done loading data.', mod=mod_identity, folder_path=folder_path, complete_data=data_by_file_name, file_names=file_names)
        return data_by_file_name

    # noinspection PyMissingOrEmptyDocstring
    def save(self, mod_identity: CommonModIdentity, data: Dict[str, Dict[str, Any]], identifier: str = None) -> bool:
        # mod_folder_persistence_service
        log = CommonLogRegistry().register_log(mod_identity, f'{mod_identity.base_namespace}_{self.log_identifier}')
        folder_path = self._folder_path(mod_identity, identifier=identifier)
        for (file_name, file_data) in data.items():
            if file_name == 'main.json':
                continue
            file_path = os.path.join(folder_path, file_name)
            log.format_with_message('Loading data.', mod=mod_identity, file_path=file_path)

            os.makedirs(folder_path, exist_ok=True)
            if os.path.exists(file_path):
                log.debug('File existed already, removing the existing one.')
                os.remove(file_path)

            result = CommonJSONIOUtils.write_to_file(file_path, file_data)
            log.format_with_message('Done saving data.', file_path=file_path)
            if not result:
                log.format_with_message('Failed to save data.', file_path=file_path, data=file_data)
        return True

    # noinspection PyMissingOrEmptyDocstring
    def remove(self, mod_identity: CommonModIdentity, identifier: str = None) -> bool:
        return True

    def _folder_path(self, mod_identity: CommonModIdentity, identifier: str = None) -> str:
        folder_path = os.path.join(self._data_folder_path, mod_identity.base_namespace.lower())
        if identifier is not None:
            folder_path = os.path.join(folder_path, identifier)
        return folder_path
