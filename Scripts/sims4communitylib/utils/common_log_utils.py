"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os

from sims4communitylib.utils.common_date_utils import CommonRealDateUtils


class CommonLogUtils:
    """ Utilities for getting paths used for logging. """
    # 10 MB
    _MAX_FILE_SIZE = 1048576

    @classmethod
    def get_exceptions_file_path(cls, mod_name: str) -> str:
        """
            Retrieve the file path to the Exceptions file used for logging error messages.
        :param mod_name: The name of the mod requesting the file path.
        :return: An str file path to the Exceptions file.
        """
        return CommonLogUtils._get_file_path(mod_name, 'Exceptions')

    @classmethod
    def get_message_file_path(cls, mod_name: str) -> str:
        """
            Retrieve the file path to the Messages file used for logging info/debug messages.
        :param mod_name: The name of the mod requesting the file path.
        :return: An str file path to the Messages file.
        """
        return CommonLogUtils._get_file_path(mod_name, 'Messages')

    @classmethod
    def get_sims_documents_location_path(cls) -> str:
        """
            Retrieves the folder path of the folder 'Documents\Electronic Arts\The Sims 4'
        :return: The file path to 'Documents\Electronic Arts\The Sims 4' folder.
        """
        file_path = ''
        root_file = os.path.normpath(os.path.dirname(os.path.realpath(__file__))).replace(os.sep, '/')
        root_file_split = root_file.split('/')
        exit_index = len(root_file_split) - root_file_split.index('Mods')
        for index in range(0, len(root_file_split) - exit_index):
            file_path = os.path.join(file_path, str(root_file_split[index]))
        return file_path

    @classmethod
    def _get_file_path(cls, mod_name: str, file_name: str):
        """
            Get an absolute file path to the file with the file name.
        :param mod_name: The name of the mod requesting the file name.
        :param file_name: A part of the name of the file being requested.
        :return: Ab str file path to the file.
        """
        root_path = CommonLogUtils.get_sims_documents_location_path()
        file_path = os.path.join(root_path, '{}_{}.txt'.format(mod_name, file_name))
        if os.path.exists(file_path) and CommonLogUtils._file_is_too_big(file_path):
            current_date_time = CommonRealDateUtils.get_current_date_string()
            os.rename(file_path, os.path.join(root_path, 'Old_{}_{}_{}.txt'.format(mod_name, file_name, current_date_time)))
        return file_path

    @classmethod
    def _file_is_too_big(cls, file_path: str):
        return os.path.getsize(file_path) > CommonLogUtils._MAX_FILE_SIZE
