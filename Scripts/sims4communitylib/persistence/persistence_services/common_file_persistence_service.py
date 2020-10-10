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
from sims4communitylib.utils.save_load.common_save_utils import CommonSaveUtils


class CommonFilePersistenceService(CommonPersistenceService):
    """CommonFilePersistenceService(per_save=True)

    A service that persists data into a file on the system.

    :param per_save: If True, the data will persist for each Save file individually. If False, the data will persist for all Save files. Default is True.
    :type per_save: bool, optional
    """

    def _file_path(self, mod_identity: CommonModIdentity, identifier: str=None) -> str:
        from sims4communitylib.utils.common_log_utils import CommonLogUtils
        data_name = self._format_data_name(mod_identity, identifier=identifier)
        if self._per_save:
            save_slot_id = CommonSaveUtils.get_save_slot_id()
            save_slot_guid = CommonSaveUtils.get_save_slot_guid()
            return os.path.join(CommonLogUtils.get_sims_documents_location_path(), 'saves', mod_identity.base_namespace.lower(), f'{data_name}_id_{save_slot_id}_guid_{save_slot_guid}.json')
        else:
            return os.path.join(CommonLogUtils.get_sims_documents_location_path(), 'saves', mod_identity.base_namespace.lower(), f'{data_name}.json')

    def __init__(self, per_save: bool=True) -> None:
        super().__init__()
        self._per_save = per_save

    # noinspection PyMissingOrEmptyDocstring
    def load(self, mod_identity: CommonModIdentity, identifier: str=None) -> Dict[str, Any]:
        file_path = self._file_path(mod_identity, identifier=identifier)

        self.log.format_with_message('Loading data.', mod=mod_identity, file_path=file_path)

        if not os.path.exists(file_path):
            self.log.format_with_message('No data was found at path.', mod=mod_identity, file_path=file_path)
            return dict()

        loaded_data: Dict[str, Any] = CommonJSONIOUtils.load_from_file(file_path)
        if loaded_data is None:
            return dict()
        self.log.format_with_message('Done loading data.', mod=mod_identity, file_path=file_path, loaded_data=loaded_data)
        return loaded_data

    # noinspection PyMissingOrEmptyDocstring
    def save(self, mod_identity: CommonModIdentity, data: Dict[str, Any], identifier: str=None) -> bool:
        file_path = self._file_path(mod_identity, identifier=identifier)

        self.log.format_with_message('Loading data.', mod=mod_identity, file_path=file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if os.path.exists(file_path):
            self.log.debug('File existed already, removing the existing one.')
            os.remove(file_path)

        result = CommonJSONIOUtils.write_to_file(file_path, data)
        self.log.format_with_message('Done saving data.', file_path=file_path)
        return result

    # noinspection PyMissingOrEmptyDocstring
    def remove(self, mod_identity: CommonModIdentity, identifier: str=None) -> bool:
        file_path = self._file_path(mod_identity, identifier=identifier)

        self.log.format_with_message('Loading data.', mod=mod_identity, file_path=file_path)

        if os.path.exists(file_path):
            self.log.debug('File existed already, removing the existing one.')
            os.remove(file_path)

        self.log.format_with_message('Data deleted successfully.', file_path=file_path)
        return not os.path.exists(file_path)
