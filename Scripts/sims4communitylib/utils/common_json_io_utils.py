"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import json
from typing import Union, Any

from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_io_utils import CommonIOUtils


class CommonJSONIOUtils:
    """
        Utilities for handling reading/writing JSON data to and from files.
    """
    @staticmethod
    def write_to_file(file_path: str, obj: Any, buffering: int=1, encoding: str= 'utf-8') -> bool:
        """
            Serialize an object to a file as JSON.
        :param file_path: The file to write to.
        :param obj: The object to write as JSON.
        :param encoding: See the 'open' function documentation for more details.
        :param buffering: See the 'open' function documentation for more details.
        :return: True if successful. False if not.
        """
        if file_path is None or obj is None:
            return False
        try:
            with open(file_path, mode='w+', buffering=buffering, encoding=encoding) as file:
                json.dump(obj, file)
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity().name, 'Error occurred while writing JSON to file \'{}\''.format(file_path), exception=ex)
            return False
        return True

    @staticmethod
    def load_from_file(file_path: str, buffering: int=1, encoding: str= 'utf-8') -> Union[Any, None]:
        """
            Deserialize an object from a JSON file.
        :param file_path: The file to read from.
        :param encoding: See the 'open' function documentation for more details.
        :param buffering: See the 'open' function documentation for more details.
        :return: The contents of the file as an object or None if an error occurred.
        """
        file_contents: str = CommonIOUtils.load_from_file(file_path, buffering=buffering, encoding=encoding)
        if file_contents is None:
            return None
        try:
            return json.loads(file_contents)
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity().name, 'Error occurred while reading JSON from file \'{}\''.format(file_path), exception=ex)
            return None
