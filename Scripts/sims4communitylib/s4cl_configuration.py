"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_json_io_utils import CommonJSONIOUtils


class S4CLConfiguration(CommonService):
    """ Manages configuration via the sims4communitylib.config file. """
    def __init__(self) -> None:
        file_path = os.path.dirname(os.path.dirname(os.path.dirname(ModInfo.get_identity().file_path.strip('/'))))
        full_file_path = os.path.join(file_path, 'sims4communitylib.json')
        if os.path.exists(full_file_path):
            self._config_data = CommonJSONIOUtils.load_from_file(full_file_path)
        else:
            self._config_data = dict()

    @property
    def enable_vanilla_logging(self) -> bool:
        """
        Whether or not vanilla logging should be enabled.

        :return: True, if vanilla logging should be enabled. False, if not.
        :rtype: bool
        """
        return self._config_data.get('enable_vanilla_logging', False)
