"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import json
import os
from os import DirEntry
from typing import Union, Any, Iterator, Dict
from sims4communitylib.utils.common_io_utils import CommonIOUtils


class CommonJSONIOUtils:
    """Utilities for reading/writing JSON data to and from files."""
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

    @staticmethod
    def load_from_folder(folder_path: str, skip_file_names: Iterator[str]=(), buffering: int=1, encoding: str= 'utf-8') -> Union[Dict[str, Any], None]:
        """load_from_folder(folder_path, skip_file_names=(), buffering=1, encoding='utf-8')

        Deserialize objects from a folder containing JSON files.

        :param folder_path: The folder to read from.
        :type: folder_path: str
        :param skip_file_names: A collection of file names to ignore. Default is an empty collection.
        :type skip_file_names: Iterator[str], optional
        :param buffering: See the built-in python :func:`~open` function documentation for more details.
        :type buffering: int, optional
        :param encoding: See the built-in python :func:`~open` function documentation for more details.
        :type encoding: str, optional
        :return: An dictionary of the contents of each file within the specified folder organized by file name or None if the folder path does not exist.
        :rtype: Union[Dict[str, Any], None]
        """
        if not os.path.exists(folder_path):
            return None
        if skip_file_names is None:
            skip_file_names = tuple()
        skip_file_names = tuple(skip_file_names)
        data = dict()
        for entry in os.scandir(folder_path):
            entry: DirEntry = entry
            if not entry.is_file() or entry.name is None or entry.name in skip_file_names:
                continue
            file_contents: str = CommonJSONIOUtils.load_from_file(entry.path, buffering=buffering, encoding=encoding)
            if file_contents is None:
                continue
            data[entry.name] = json.loads(file_contents)
        return data
