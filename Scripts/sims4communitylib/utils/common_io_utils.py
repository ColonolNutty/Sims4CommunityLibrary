"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from typing import Union
from sims4communitylib.modinfo import ModInfo


class CommonIOUtils:
    """
        Utilities for handling reading/writing to and from files.
    """
    @staticmethod
    def write_to_file(file_path: str, data: str, buffering: int=1, encoding: str='utf-8', ignore_errors: bool=False) -> bool:
        """
            Write string data to a file.
        :param file_path: The file to write to.
        :param data: The data to write.
        :param encoding: See the 'open' function documentation for more details.
        :param buffering: See the 'open' function documentation for more details.
        :param ignore_errors: If True, any exceptions thrown will be ignored (Useful in preventing infinite loops)
        :return: True if successful. False if not.
        """
        if file_path is None or data is None:
            return False
        try:
            with open(file_path, mode='a', buffering=buffering, encoding=encoding) as opened_file:
                opened_file.write(data)
                opened_file.flush()
                opened_file.close()
        except Exception as ex:
            if ignore_errors:
                return False
            from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
            CommonExceptionHandler.log_exception(ModInfo.get_identity().name, 'Error occurred while writing to file \'{}\''.format(file_path), exception=ex)
            return False
        return True

    @staticmethod
    def load_from_file(file_path: str, buffering: int=1, encoding: str='utf-8') -> Union[str, None]:
        """
            Load string data from a file.
        :param file_path: The file to read from.
        :param encoding: See the 'open' function documentation for more details.
        :param buffering: See the 'open' function documentation for more details.
        :return: The contents of the file as a string or None if an error occurred.
        """
        if not os.path.isfile(file_path):
            return None
        try:
            with open(file_path, mode='r', buffering=buffering, encoding=encoding) as file:
                return file.read()
        except Exception as ex:
            from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
            CommonExceptionHandler.log_exception(ModInfo.get_identity().name, 'Error occurred while reading from file \'{}\''.format(file_path), exception=ex)
            return None
