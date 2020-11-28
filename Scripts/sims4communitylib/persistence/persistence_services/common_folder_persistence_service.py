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


class CommonFolderPersistenceService(CommonPersistenceService):
    """CommonFolderPersistenceService(main_file_name='main.json', combined_file_name='combined.json', allow_duplicates_in_collections=False)

    A service that persists data to a file within a folder on the system. It also loads all data from a folder on the system while loading the main file last.

    :param main_file_name: A file that will be loaded after the other files in the folder specified by folder_name. Default is 'main.json'.
    :type main_file_name: str, optional
    :param combined_file_name: The name of the file to persist data to when saving. Default is combined.json
    :type combined_file_name: str, optional
    :param allow_duplicates_in_collections: When loading the dictionary data and merging it, if set to True, duplicate values will be allowed to exist within collections within those dictionaries. Default is False.
    :type allow_duplicates_in_collections: bool, optional
    """

    def _folder_path(self, mod_identity: CommonModIdentity, identifier: str=None) -> str:
        from sims4communitylib.utils.common_log_utils import CommonLogUtils
        folder_path = os.path.join(CommonLogUtils.get_sims_documents_location_path(), 'Mods', 'mod_data', mod_identity.base_namespace.lower())
        if identifier is not None:
            folder_path = os.path.join(folder_path, identifier)
        return folder_path

    def __init__(self, main_file_name: str= 'main.json', combined_file_name: str= 'combined.json', allow_duplicates_in_collections: bool=False) -> None:
        super().__init__()
        self._main_file_name = main_file_name
        self._combined_file_name = combined_file_name
        self._allow_duplicates_in_collections = allow_duplicates_in_collections

    # noinspection PyMissingOrEmptyDocstring
    def load(self, mod_identity: CommonModIdentity, identifier: str=None) -> Dict[str, Any]:
        folder_path = self._folder_path(mod_identity, identifier=identifier)

        self.log.format_with_message('Loading data.', mod=mod_identity, folder_path=folder_path)

        if not os.path.exists(folder_path):
            self.log.format_with_message('No folder was found at path.', mod=mod_identity, folder_path=folder_path)
            return dict()

        main_file_path = os.path.join(folder_path, self._main_file_name)
        loaded_main_data: Dict[str, Any] = CommonJSONIOUtils.load_from_file(main_file_path)
        if loaded_main_data is None:
            self.log.format_with_message('Missing main data!', main_file_path=main_file_path)
            return dict()

        combined_file_path = os.path.join(folder_path, self._combined_file_name)
        loaded_combined_data: Dict[str, Any] = CommonJSONIOUtils.load_from_file(combined_file_path)

        loaded_data: Dict[str, Dict[str, Any]] = CommonJSONIOUtils.load_from_folder(folder_path, skip_file_names=(self._main_file_name, self._combined_file_name))
        if loaded_data is None:
            return dict()
        complete_data = dict()
        for (key, val) in loaded_data.items():
            complete_data = CommonCollectionUtils.merge_dict(complete_data, val, prefer_source_values=True, allow_duplicates_in_collections=self._allow_duplicates_in_collections)
        complete_data = CommonCollectionUtils.merge_dict(complete_data, loaded_main_data, prefer_source_values=True, allow_duplicates_in_collections=self._allow_duplicates_in_collections)
        if loaded_combined_data is not None:
            complete_data = CommonCollectionUtils.merge_dict(complete_data, loaded_combined_data, prefer_source_values=True, allow_duplicates_in_collections=self._allow_duplicates_in_collections)
        self.log.format_with_message('Done loading data.', mod=mod_identity, folder_path=folder_path, complete_data=complete_data)
        return complete_data

    # noinspection PyMissingOrEmptyDocstring
    def save(self, mod_identity: CommonModIdentity, data: Dict[str, Any], identifier: str=None) -> bool:
        folder_path = self._folder_path(mod_identity, identifier=identifier)

        file_path = os.path.join(folder_path, self._combined_file_name)
        self.log.format_with_message('Loading data.', mod=mod_identity, file_path=file_path)

        os.makedirs(folder_path, exist_ok=True)
        if os.path.exists(file_path):
            self.log.debug('File existed already, removing the existing one.')
            os.remove(file_path)

        result = CommonJSONIOUtils.write_to_file(file_path, data)
        self.log.format_with_message('Done saving data.', file_path=file_path)
        return result

    # noinspection PyMissingOrEmptyDocstring
    def remove(self, mod_identity: CommonModIdentity, identifier: str=None) -> bool:
        folder_path = self._folder_path(mod_identity, identifier=identifier)

        file_path = os.path.join(folder_path, self._combined_file_name)
        self.log.format_with_message('Removing data.', mod=mod_identity, file_path=file_path)

        if os.path.exists(file_path):
            self.log.debug('Data existed, removing it.')
            os.remove(file_path)

        self.log.format_with_message('Data deleted successfully.', file_path=file_path)
        return not os.path.exists(file_path)
