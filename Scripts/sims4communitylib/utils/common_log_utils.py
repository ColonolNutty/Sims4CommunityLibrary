"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from typing import Union

from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_date_utils import CommonRealDateUtils


class CommonLogUtils:
    """Utilities for retrieving the paths used for logging.

    """
    # 10 MB
    _MAX_FILE_SIZE = 1048576

    @staticmethod
    def get_exceptions_file_path(mod_identifier: Union[str, CommonModIdentity]) -> str:
        """get_exceptions_file_path(mod_identifier)

        Retrieve the file path to the Exceptions file used for logging error messages.

        :param mod_identifier: The name or identity of the mod requesting the file path.
        :type mod_identifier: Union[str, CommonModIdentity]
        :return: An str file path to the Exceptions file.
        :rtype: str
        """
        return CommonLogUtils._get_file_path(mod_identifier, 'Exceptions')

    @staticmethod
    def get_message_file_path(mod_identifier: Union[str, CommonModIdentity]) -> str:
        """get_message_file_path(mod_identifier)

        Retrieve the file path to the Messages file used for logging info/debug messages.

        :param mod_identifier: The name of the mod requesting the file path.
        :type mod_identifier: Union[str, CommonModIdentity]
        :return: An str file path to the Messages file.
        :rtype: str
        """
        return CommonLogUtils._get_file_path(mod_identifier, 'Messages')

    @staticmethod
    def get_sims_documents_location_path() -> str:
        """get_sims_documents_location_path()

        Retrieve the full path of the folder 'Documents\Electronic Arts\The Sims 4'

        :return: The file path to 'Documents\Electronic Arts\The Sims 4' folder.
        :rtype: str
        """
        file_path = ''
        from sims4communitylib.modinfo import ModInfo
        root_file = os.path.normpath(os.path.dirname(os.path.realpath(ModInfo.get_identity().file_path))).replace(os.sep, '/')
        root_file_split = root_file.split('/')
        # noinspection PyTypeChecker
        exit_index = len(root_file_split) - root_file_split.index('Mods')
        for index in range(0, len(root_file_split) - exit_index):
            file_path = os.path.join(file_path + os.sep, str(root_file_split[index]))
        return file_path

    @staticmethod
    def _get_file_path(mod_identifier: Union[str, CommonModIdentity], file_name: str) -> str:
        if isinstance(mod_identifier, CommonModIdentity):
            mod_identifier = mod_identifier.name
        root_path = CommonLogUtils.get_sims_documents_location_path()
        file_path = os.path.join(root_path, '{}_{}.txt'.format(mod_identifier, file_name))
        if os.path.exists(file_path) and CommonLogUtils._file_is_too_big(file_path):
            current_date_time = CommonRealDateUtils.get_current_date_string()
            os.rename(file_path, os.path.join(root_path, 'Old_{}_{}_{}.txt'.format(mod_identifier, file_name, str(current_date_time).replace(':', '_'))))
        return file_path

    @staticmethod
    def _file_is_too_big(file_path: str) -> bool:
        return os.path.getsize(file_path) > CommonLogUtils._MAX_FILE_SIZE
