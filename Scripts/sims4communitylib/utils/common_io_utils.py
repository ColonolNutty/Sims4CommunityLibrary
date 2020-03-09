"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from typing import Union
from sims4communitylib.modinfo import ModInfo


class CommonIOUtils:
    """Utilities for reading/writing to and from files.

    """
    @staticmethod
    def write_to_file(file_path: str, data: str, buffering: int=1, encoding: str='utf-8', ignore_errors: bool=False) -> bool:
        """write_to_file(file_path, data, buffering=1, encoding='utf-8', ignore_errors=False)

        Write string data to a file.

        :param file_path: The file to write to.
        :type file_path: str
        :param data: The data to write.
        :type data: str
        :param buffering: See the built-in python :func:`~open` function documentation for more details.
        :type buffering: int, optional
        :param encoding: See the built-in python :func:`~open` function documentation for more details.
        :type encoding: str, optional
        :param ignore_errors: If True, any exceptions thrown will be ignored (Useful in preventing infinite loops)
        :type ignore_errors: bool, optional
        :return: True if successful. False if not.
        :rtype: bool
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
            CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Error occurred while writing to file \'{}\''.format(file_path), exception=ex)
            return False
        return True

    @staticmethod
    def load_from_file(file_path: str, buffering: int=1, encoding: str='utf-8') -> Union[str, None]:
        """load_from_file(file_path, buffering=1, encoding='utf-8')

        Load string data from a file.

        :param file_path: The file to read from.
        :type file_path: str
        :param buffering: See the built-in python :func:`~open` function documentation for more details.
        :type buffering: int, optional
        :param encoding: See the built-in python :func:`~open` function documentation for more details.
        :type encoding: str, optional
        :return: The contents of the file as a string or None if an error occurred.
        :rtype: Union[str, None]
        """
        if not os.path.isfile(file_path):
            return None
        try:
            with open(file_path, mode='r', buffering=buffering, encoding=encoding) as file:
                return file.read()
        except Exception as ex:
            from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
            CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Error occurred while reading from file \'{}\''.format(file_path), exception=ex)
            return None
