"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from typing import Tuple, Dict, List, Any

from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_json_io_utils import CommonJSONIOUtils
from sims4communitylib.utils.common_log_registry import CommonMessageType
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils

ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'


class S4CLConfiguration(HasLog, CommonService):
    """ Manages configuration via the sims4communitylib.config file. """
    _CONFIGURATION_FILE_NAME = 'sims4communitylib.config'
    if not ON_RTD:
        _DEFAULT_CONFIG_DATA = {
            'enable_vanilla_logging': False,
            'enable_extra_shift_click_menus': True,
            'persist_mod_data_per_save_slot': False,
            'create_combined_json': False,
            'max_output_file_size_in_bytes': 524288000,
            'enable_logs': {
                'example_log_that_is_enabled': ['DEBUG', 'WARN']
            }
        }
    else:
        _DEFAULT_CONFIG_DATA = dict()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    def __init__(self) -> None:
        self._config_data = dict()
        super().__init__()
        self._config_data: Dict[str, Any] = S4CLConfiguration._DEFAULT_CONFIG_DATA.copy()
        try:
            file_path = os.path.dirname(os.path.dirname(os.path.dirname(self.mod_identity.file_path.rstrip('/').rstrip('\\'))))
            full_file_path = os.path.join(file_path, S4CLConfiguration._CONFIGURATION_FILE_NAME)
            try:
                if os.path.exists(full_file_path):
                    existing_config_data = CommonJSONIOUtils.load_from_file(full_file_path) or dict()
                    if 'enable_logs_result' in existing_config_data:
                        del existing_config_data['enable_logs_result']
                    self._config_data.update(existing_config_data)
                    CommonJSONIOUtils.write_to_file(full_file_path, self._config_data)
                else:
                    CommonJSONIOUtils.write_to_file(full_file_path, self._config_data)
            except Exception as ex:
                CommonExceptionHandler.log_exception(self.mod_identity, 'Failed to read the configuration file named {} at path "{}"!'.format(S4CLConfiguration._CONFIGURATION_FILE_NAME, full_file_path), exception=ex)
                if not os.path.exists(full_file_path):
                    # noinspection PyBroadException
                    try:
                        CommonJSONIOUtils.write_to_file(full_file_path, self._config_data)
                    except:
                        pass
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Failed to format the file path to the S4CL configuration file.', exception=ex)

    @property
    def persist_mod_data_per_save_slot(self) -> bool:
        """Whether or not mod_data should include the save slot id within the persisted data file names. If False, only the Guid will be present in the file names. This value will also have an effect on loading files too!"""
        if self._config_data is None or not self._config_data:
            return False
        return self._config_data.get('persist_mod_data_per_save_slot', False)

    @property
    def enable_vanilla_logging(self) -> bool:
        """ Whether or not vanilla logging should be enabled. """
        if self._config_data is None or not self._config_data:
            return False
        return self._config_data.get('enable_vanilla_logging', False)

    @property
    def max_output_file_size_in_bytes(self) -> int:
        """ The maximum size a file created by S4CL can be in bytes. """
        if self._config_data is None or not self._config_data:
            return False
        return self._config_data.get('max_output_file_size_in_bytes', 524288000)

    @property
    def enable_extra_shift_click_menus(self) -> bool:
        """ Whether or not to enable the SHIFT+CLICK menu in places that normally do not have a SHIFT+CLICK menu due to the ignorance of the SHIFT key. i.e. Relationship Panel, Phone, and Inventory. """
        if self._config_data is None or not self._config_data:
            return False
        return self._config_data.get('enable_extra_shift_click_menus', False)

    @property
    def create_combined_json(self) -> bool:
        """ Whether or not to create a combined.json file when reading through folders. """
        if self._config_data is None or not self._config_data:
            return False
        return self._config_data.get('create_combined_json', False)

    @property
    def enable_logs(self) -> Dict[str, Tuple[CommonMessageType]]:
        """ Logs to enable before loading The Sims 4. """
        if self._config_data is None or not self._config_data:
            return dict()
        if 'enable_logs_result' in self._config_data:
            return self._config_data.get('enable_logs_result', dict())
        enable_logs = self._config_data.get('enable_logs', dict())
        enable_logs_result: Dict[str, Tuple[CommonMessageType]] = dict()
        try:
            for (key, message_type_strings) in enable_logs.items():
                message_types: List[CommonMessageType] = list()
                for message_type_string in message_type_strings:
                    message_type: CommonMessageType = CommonResourceUtils.get_enum_by_name(message_type_string, CommonMessageType, default_value=CommonMessageType.INVALID)
                    if message_type is None:
                        continue
                    message_types.append(message_type)
                if message_types:
                    enable_logs_result[key] = tuple(message_types)
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'Error occurred while parsing the enable_logs configuration value.', exception=ex)
            return dict()
        self._config_data['enable_logs_result'] = enable_logs_result
        return enable_logs_result
