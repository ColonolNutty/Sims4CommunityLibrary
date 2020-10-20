"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import json
from typing import Union, Any
from sims4communitylib.utils.common_io_utils import CommonIOUtils


class CommonJSONIOUtils:
    """Utilities for reading/writing JSON data to and from files.

    """
    @staticmethod
    def write_to_file(file_path: str, obj: Any, buffering: int=1, encoding: str= 'utf-8') -> bool:
        """write_to_file(file_path, obj, buffering=1, encoding='utf-8')

        Serialize an object to a file as JSON.

        :param file_path: The file to write to.
        :type file_path: str
        :param obj: The object to write as JSON.
        :type obj: Any
        :param buffering: See the built-in python :func:`~open` function documentation for more details.
        :type buffering: int, optional
        :param encoding: See the built-in python :func:`~open` function documentation for more details.
        :type encoding: str, optional
        :return: True if successful. False if not.
        :rtype: bool
        """
        if file_path is None or obj is None:
            return False
        with open(file_path, mode='w+', buffering=buffering, encoding=encoding) as file:
            json.dump(obj, file)
        return True

    @staticmethod
    def load_from_file(file_path: str, buffering: int=1, encoding: str= 'utf-8') -> Union[Any, None]:
        """load_from_file(file_path, buffering=1, encoding='utf-8')

        Deserialize an object from a JSON file.

        :param file_path: The file to read from.
        :type: file_path: str
        :param buffering: See the built-in python :func:`~open` function documentation for more details.
        :type buffering: int, optional
        :param encoding: See the built-in python :func:`~open` function documentation for more details.
        :type encoding: str, optional
        :return: The contents of the file as an object or None if an error occurred.
        :rtype: Union[Any, None]
        """
        file_contents: str = CommonIOUtils.load_from_file(file_path, buffering=buffering, encoding=encoding)
        if file_contents is None:
            return None
        return json.loads(file_contents)
