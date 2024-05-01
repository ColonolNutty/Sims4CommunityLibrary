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

    @staticmethod
    def get_sims_4_game_version() -> str:
        """get_sims_4_game_version()

        Retrieve the current game version of Sims 4.

        :return: The current game version of Sims 4.
        :rtype: str
        """
        the_sims_4_folder = CommonLogUtils.get_sims_documents_location_path()
        filename = os.path.join(the_sims_4_folder, 'GameVersion.txt')
        import re
        with open(filename, 'rb') as fp:
            v = fp.read().decode(errors='ignore')  # convert b to str and ignore errors
            v = re.sub(r'[^0-9.]', '', v)  # in case of UTF-8 characters which survived 'ignore': replace everything with '' except of '0-9' and '.'
        return v

    @staticmethod
    def get_exceptions_file_path(mod_identifier: Union[str, CommonModIdentity], custom_file_path: str=None) -> str:
        """get_exceptions_file_path(mod_identifier, custom_file_path=None)

        Retrieve the file path to the Exceptions file used for logging error messages.

        :param mod_identifier: The name or identity of the mod requesting the file path.
        :type mod_identifier: Union[str, CommonModIdentity]
        :param custom_file_path: A custom file path relative to The Sims 4 folder. Example: Value is 'fake_path/to/directory', the final path would be 'The Sims 4/fake_path/to_directory'. Default is None.
        :type custom_file_path: str, optional
        :return: A file path to the Exceptions file.
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
        :return: A file path to the Messages file.
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
        :return: A file path to the Old Exceptions file.
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
        :return: A file path to the Old Messages file.
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
        # return os.environ['TS4_MODS_FOLDER']
        documents_path = os.path.dirname(CommonLogUtils.get_mods_location_path())
        if os.path.exists(documents_path):
            return documents_path
        from sims4communitylib.modinfo import ModInfo
        root_file = os.path.normpath(os.path.dirname(os.path.realpath(ModInfo.get_identity().file_path))).replace(os.sep, '/')
        root_file_split = root_file.split('/')
        if 'Mods' not in root_file_split:
            return ''
        file_path = ''
        # noinspection PyTypeChecker
        exit_index = len(root_file_split) - root_file_split.index('Mods')
        for index in range(0, len(root_file_split) - exit_index):
            file_path = os.path.join(file_path + os.sep, str(root_file_split[index]))
        return file_path

    @staticmethod
    def get_mods_location_path() -> str:
        """get_sims_mods_location_path()

        Retrieve the full path of the folder 'Documents\Electronic Arts\The Sims 4\Mods'

        :return: The file path to 'Documents\Electronic Arts\The Sims 4\Mods' folder.
        :rtype: str
        """
        current_file_path = os.path.dirname(os.path.abspath(__file__))
        mods_folder = os.path.join(current_file_path.partition(f"{os.sep}Mods{os.sep}")[0], 'Mods')
        return mods_folder

    @staticmethod
    def get_mod_logs_location_path() -> str:
        """get_mod_logs_location_path()

        Retrieve the full path of the folder 'Documents\Electronic Arts\The Sims 4\mod_logs'

        :return: The file path to 'Documents\Electronic Arts\The Sims 4\mod_logs' folder.
        :rtype: str
        """
        sims_documents_location = CommonLogUtils.get_sims_documents_location_path()
        if sims_documents_location == '':
            return ''
        return os.path.join(sims_documents_location, 'mod_logs')

    @staticmethod
    def get_mod_data_location_path() -> str:
        """get_mod_data_location_path()

        Retrieve the full path of the folder 'Documents\Electronic Arts\The Sims 4\Mods\mod_data'

        :return: The file path to 'Documents\Electronic Arts\The Sims 4\Mods\mod_data' folder.
        :rtype: str
        """
        mods_location = CommonLogUtils.get_mods_location_path()
        if mods_location == '':
            return ''
        return os.path.join(mods_location, 'mod_data')

    @staticmethod
    def _get_file_name(mod_identifier: Union[str, CommonModIdentity], file_name: str, custom_file_path: str=None) -> str:
        from sims4communitylib.utils.misc.common_mod_identity_utils import CommonModIdentityUtils
        mod_identifier = CommonModIdentityUtils.determine_mod_name_from_identifier(mod_identifier)
        file_path = CommonLogUtils.get_mod_logs_location_path()
        file_name = '{}_{}.txt'.format(mod_identifier, file_name)
        if not os.path.exists(file_path):
            os.makedirs(file_path, exist_ok=True)
        if custom_file_path is not None:
            file_path = os.path.join(file_path, custom_file_path)
        current_file = os.path.join(file_path, file_name)
        try:
            if os.path.exists(current_file) and CommonLogUtils._file_is_too_big(current_file):
                new_file_name = file_name.replace('.txt', '')
                old_file_name = None
                for x in range(20):
                    old_file_name = 'Old_{}_{}.txt'.format(new_file_name, x)
                    if not os.path.exists(os.path.join(file_path, old_file_name)):
                        break
                if old_file_name is None:
                    return current_file
                old_file_path = os.path.join(file_path, old_file_name)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
                os.rename(current_file, old_file_path)
        except PermissionError:
            pass
        return current_file

    @staticmethod
    def _get_old_file_path_name(mod_identifier: Union[str, CommonModIdentity], file_name: str, custom_file_path: str=None) -> str:
        from sims4communitylib.utils.misc.common_mod_identity_utils import CommonModIdentityUtils
        mod_identifier = CommonModIdentityUtils.determine_mod_name_from_identifier(mod_identifier)
        file_path = CommonLogUtils.get_mod_logs_location_path()
        old_file_name = 'Old_{}_{}.txt'.format(mod_identifier, file_name)
        if not os.path.exists(file_path):
            os.makedirs(file_path, exist_ok=True)
        if custom_file_path is not None:
            file_path = os.path.join(file_path, custom_file_path)
        return os.path.join(file_path, old_file_name)

    @staticmethod
    def _file_is_too_big(file_path: str) -> bool:
        from sims4communitylib.s4cl_configuration import S4CLConfiguration
        return os.path.getsize(file_path) > S4CLConfiguration().max_output_file_size_in_bytes
