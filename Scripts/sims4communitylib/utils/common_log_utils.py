"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from typing import Union

from sims4communitylib.mod_support.mod_identity import CommonModIdentity


class CommonLogUtils:
    """Utilities for retrieving the paths used for logging.

    """
    # 10 MB
    _MAX_FILE_SIZE = 1048576

    @staticmethod
    def get_exceptions_file_path(mod_identifier: Union[str, CommonModIdentity], custom_file_path: str=None) -> str:
        """get_exceptions_file_path(mod_identifier, custom_file_path=None)

        Retrieve the file path to the Exceptions file used for logging error messages.

        :param mod_identifier: The name or identity of the mod requesting the file path.
        :type mod_identifier: Union[str, CommonModIdentity]
        :param custom_file_path: A custom file path relative to The Sims 4 folder. Example: Value is 'fake_path/to/directory', the final path would be 'The Sims 4/fake_path/to_directory'. Default is None.
        :type custom_file_path: str, optional
        :return: An str file path to the Exceptions file.
        :rtype: str
        """
        return CommonLogUtils._get_file_name(mod_identifier, 'Exceptions', custom_file_path=custom_file_path)

    @staticmethod
    def get_message_file_path(mod_identifier: Union[str, CommonModIdentity], custom_file_path: str=None) -> str:
        """get_message_file_path(mod_identifier, custom_file_path=None)

        Retrieve the file path to the Messages file used for logging info/debug messages.

        :param mod_identifier: The name of the mod requesting the file path.
        :type mod_identifier: Union[str, CommonModIdentity]
        :param custom_file_path: A custom file path relative to The Sims 4 folder. Example: Value is 'fake_path/to/directory', the final path would be 'The Sims 4/fake_path/to_directory'. Default is None.
        :type custom_file_path: str, optional
        :return: An str file path to the Messages file.
        :rtype: str
        """
        return CommonLogUtils._get_file_name(mod_identifier, 'Messages', custom_file_path=custom_file_path)

    @staticmethod
    def get_old_exceptions_file_path(mod_identifier: Union[str, CommonModIdentity], custom_file_path: str=None) -> str:
        """get_old_exceptions_file_path(mod_identifier, custom_file_path=None)

        Retrieve the file path to the Old Exceptions file used as the overflow when the main Exception file becomes too large.

        :param mod_identifier: The name or identity of the mod requesting the file path.
        :type mod_identifier: Union[str, CommonModIdentity]
        :param custom_file_path: A custom file path relative to The Sims 4 folder. Example: Value is 'fake_path/to/directory', the final path would be 'The Sims 4/fake_path/to_directory'. Default is None.
        :type custom_file_path: str, optional
        :return: An str file path to the Old Exceptions file.
        :rtype: str
        """
        return CommonLogUtils._get_old_file_path_name(mod_identifier, 'Exceptions', custom_file_path=custom_file_path)

    @staticmethod
    def get_old_message_file_path(mod_identifier: Union[str, CommonModIdentity], custom_file_path: str=None) -> str:
        """get_old_message_file_path(mod_identifier, custom_file_path=None)

        Retrieve the file path to the Old Messages file used as the overflow when the main Messages file becomes too large.

        :param mod_identifier: The name of the mod requesting the file path.
        :type mod_identifier: Union[str, CommonModIdentity]
        :param custom_file_path: A custom file path relative to The Sims 4 folder. Example: Value is 'fake_path/to/directory', the final path would be 'The Sims 4/fake_path/to_directory'. Default is None.
        :type custom_file_path: str, optional
        :return: An str file path to the Old Messages file.
        :rtype: str
        """
        return CommonLogUtils._get_old_file_path_name(mod_identifier, 'Messages', custom_file_path=custom_file_path)

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
        if 'Mods' not in root_file_split:
            return ''
        # noinspection PyTypeChecker
        exit_index = len(root_file_split) - root_file_split.index('Mods')
        for index in range(0, len(root_file_split) - exit_index):
            file_path = os.path.join(file_path + os.sep, str(root_file_split[index]))
        return file_path

    @staticmethod
    def _get_file_name(mod_identifier: Union[str, CommonModIdentity], file_name: str, custom_file_path: str=None) -> str:
        mod_identifier = CommonModIdentity._get_mod_name(mod_identifier)
        root_path = CommonLogUtils.get_sims_documents_location_path()
        file_name = '{}_{}.txt'.format(mod_identifier, file_name)
        file_path = root_path
        if os.path.exists(file_path) and CommonLogUtils._file_is_too_big(file_path):
            old_file_name = 'Old_{}'.format(file_name)
            old_file_path = os.path.join(root_path, custom_file_path, old_file_name)
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
            os.rename(file_path, old_file_path)
        if custom_file_path is not None:
            file_path = os.path.join(file_path, custom_file_path)
        return os.path.join(file_path, file_name)

    @staticmethod
    def _get_old_file_path_name(mod_identifier: Union[str, CommonModIdentity], file_name: str, custom_file_path: str=None) -> str:
        mod_identifier = CommonModIdentity._get_mod_name(mod_identifier)
        root_path = CommonLogUtils.get_sims_documents_location_path()
        old_file_name = 'Old_{}_{}.txt'.format(mod_identifier, file_name)
        file_path = root_path
        if custom_file_path is not None:
            file_path = os.path.join(file_path, custom_file_path)
        return os.path.join(file_path, old_file_name)

    @staticmethod
    def _file_is_too_big(file_path: str) -> bool:
        return os.path.getsize(file_path) > CommonLogUtils._MAX_FILE_SIZE
