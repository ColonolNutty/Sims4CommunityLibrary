"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os

from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_json_io_utils import CommonJSONIOUtils


class S4CLConfiguration(HasLog, CommonService):
    """ Manages configuration via the sims4communitylib.config file. """
    _CONFIGURATION_FILE_NAME = 'sims4communitylib.config'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'common_s4cl_configuration'

    def __init__(self) -> None:
        super().__init__()
        file_path = os.path.dirname(os.path.dirname(os.path.dirname(self.mod_identity.file_path.strip('/'))))
        full_file_path = os.path.join(file_path, S4CLConfiguration._CONFIGURATION_FILE_NAME)
        if os.path.exists(full_file_path):
            self._config_data = CommonJSONIOUtils.load_from_file(full_file_path)
        else:
            self.log.error('Failed to locate configuration file named {} at path {}'.format(S4CLConfiguration._CONFIGURATION_FILE_NAME, file_path))
            self._config_data = dict()

    @property
    def enable_vanilla_logging(self) -> bool:
        """
        Whether or not vanilla logging should be enabled.

        :return: True, if vanilla logging should be enabled. False, if not.
        :rtype: bool
        """
        return self._config_data.get('enable_vanilla_logging', False)
