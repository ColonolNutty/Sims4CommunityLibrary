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
from sims4communitylib.utils.common_collection_utils import CommonCollectionUtils
from sims4communitylib.utils.common_json_io_utils import CommonJSONIOUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry


class CommonFolderPersistenceService(CommonPersistenceService):
    """CommonFolderPersistenceService(main_file_name='main.json', combined_file_name='combined.json', allow_duplicates_in_collections=False, data_folder_path=None)

    A service that persists data to a file within a folder on the system. It also loads all data from a folder on the system while loading the main file last.

    :param main_file_name: A file that will be loaded after the other files in the folder specified by folder_name. Default is 'main.json'.
    :type main_file_name: str, optional
    :param combined_file_name: The name of the file to persist data to when saving. Default is combined.json
    :type combined_file_name: str, optional
    :param allow_duplicates_in_collections: When loading the dictionary data and merging it, if set to True, duplicate values will be allowed to exist within collections within those dictionaries. Default is False.
    :type allow_duplicates_in_collections: bool, optional
    :param data_folder_path: Use to specify a custom folder path at the top level for which to save/load data to/from. Default is "Mods/mod_data".
    :type data_folder_path: str, optional
    :param create_combined_file: If True, after reading through all json files, a combined.json file will be created that will include all other json data. If false, a combined.json file will not be created. Default is false.
    :type create_combined_file: bool, optional
    """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'common_folder_persistence_service'

    def __init__(
        self,
        main_file_name: str='main.json',
        combined_file_name: str='combined.json',
        allow_duplicates_in_collections: bool=False,
        data_folder_path: str=None,
        create_combined_file: bool=False
    ) -> None:
        super().__init__()
        self._main_file_name = main_file_name
        self._combined_file_name = combined_file_name
        self._allow_duplicates_in_collections = allow_duplicates_in_collections
        from sims4communitylib.utils.common_log_utils import CommonLogUtils
        self._data_folder_path = data_folder_path or CommonLogUtils.get_mod_data_location_path()
        from sims4communitylib.s4cl_configuration import S4CLConfiguration
        self._create_combined_file = create_combined_file or S4CLConfiguration().create_combined_json

    # noinspection PyMissingOrEmptyDocstring
    def load(self, mod_identity: CommonModIdentity, identifier: str=None) -> Dict[str, Any]:
        # mod_folder_persistence_service
        log = CommonLogRegistry().register_log(mod_identity, '{}_{}'.format(mod_identity.base_namespace, self.log_identifier))
        folder_path = self._folder_path(mod_identity, identifier=identifier)

        log.format_with_message('Loading data.', mod=mod_identity, folder_path=folder_path)

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

        if self._create_combined_file:
            combined_file_path = os.path.join(folder_path, self._combined_file_name)
            loaded_combined_data: Dict[str, Any] = CommonJSONIOUtils.load_from_file(combined_file_path)
        else:
            loaded_combined_data = None

        def _on_file_read_failure(file_path: str, ex: Exception):
            log.error('Failed to read file with path {}'.format(file_path), exception=ex)
            return True

        loaded_data: Dict[str, Dict[str, Any]] = CommonJSONIOUtils.load_from_folder(
            folder_path,
            skip_file_names=(self._main_file_name, self._combined_file_name),
            on_file_read_failure=_on_file_read_failure
        )
        if loaded_data is None:
            return dict()
        complete_data = dict()
        for (key, val) in loaded_data.items():
            file_names.append(key)
            complete_data = CommonCollectionUtils.merge_dict(complete_data, val, prefer_source_values=True, allow_duplicates_in_collections=self._allow_duplicates_in_collections)
        if self._create_combined_file:
            if loaded_combined_data is not None:
                complete_data = CommonCollectionUtils.merge_dict(loaded_combined_data, complete_data, prefer_source_values=True, allow_duplicates_in_collections=self._allow_duplicates_in_collections)
        complete_data = CommonCollectionUtils.merge_dict(complete_data, loaded_main_data, prefer_source_values=True, allow_duplicates_in_collections=self._allow_duplicates_in_collections)
        log.format_with_message('Done loading data.', mod=mod_identity, folder_path=folder_path, complete_data=complete_data, file_names=file_names)
        complete_data['loaded_file_names'] = file_names
        return complete_data

    # noinspection PyMissingOrEmptyDocstring
    def save(self, mod_identity: CommonModIdentity, data: Dict[str, Any], identifier: str=None) -> bool:
        # mod_folder_persistence_service
        log = CommonLogRegistry().register_log(mod_identity, '{}_{}'.format(mod_identity.base_namespace, self.log_identifier))
        folder_path = self._folder_path(mod_identity, identifier=identifier)
        data_to_save = data.copy()

        if self._create_combined_file:
            file_path = os.path.join(folder_path, self._combined_file_name)
            log.format_with_message('Loading data.', mod=mod_identity, file_path=file_path)
            if 'loaded_file_names' in data_to_save:
                del data_to_save['loaded_file_names']

            os.makedirs(folder_path, exist_ok=True)
            if os.path.exists(file_path):
                log.debug('File existed already, removing the existing one.')
                os.remove(file_path)

            result = CommonJSONIOUtils.write_to_file(file_path, data_to_save)
            log.format_with_message('Done saving data.', file_path=file_path)
            return result
        return True

    # noinspection PyMissingOrEmptyDocstring
    def remove(self, mod_identity: CommonModIdentity, identifier: str=None) -> bool:
        # mod_folder_persistence_service
        log = CommonLogRegistry().register_log(mod_identity, '{}_{}'.format(mod_identity.base_namespace, self.log_identifier))
        folder_path = self._folder_path(mod_identity, identifier=identifier)

        if self._create_combined_file:
            file_path = os.path.join(folder_path, self._combined_file_name)
            log.format_with_message('Removing data.', mod=mod_identity, file_path=file_path)

            if os.path.exists(file_path):
                log.debug('Data existed, removing it.')
                os.remove(file_path)

            log.format_with_message('Data deleted successfully.', file_path=file_path)
            return not os.path.exists(file_path)
        return True

    def _folder_path(self, mod_identity: CommonModIdentity, identifier: str=None) -> str:
        folder_path = os.path.join(self._data_folder_path, mod_identity.base_namespace.lower())
        if identifier is not None:
            folder_path = os.path.join(folder_path, identifier)
        return folder_path
