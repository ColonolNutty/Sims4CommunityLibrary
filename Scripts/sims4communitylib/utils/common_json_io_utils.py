"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import json
import os
from json import JSONEncoder, JSONDecoder
from os import DirEntry
from typing import Union, Any, Iterator, Dict, Type, Callable

from sims4communitylib.classes.serialization.common_serializable import CommonSerializable
from sims4communitylib.utils.common_io_utils import CommonIOUtils


class CommonJSONIOUtils:
    """Utilities for reading/writing JSON data to and from files."""
    @staticmethod
    def write_to_file(file_path: str, obj: Any, buffering: int=1, encoding: str='utf-8', encoder_class: Type[JSONEncoder]=None) -> bool:
        """write_to_file(file_path, obj, buffering=1, encoding='utf-8', encoder_class=None)

        Serialize an object to a file as JSON.

        :param file_path: The file to write to.
        :type file_path: str
        :param obj: The object to write as JSON.
        :type obj: Any
        :param buffering: See the built-in python :func:`~open` function documentation for more details.
        :type buffering: int, optional
        :param encoding: See the built-in python :func:`~open` function documentation for more details.
        :type encoding: str, optional
        :param encoder_class: Specify a custom JSON encoder class to use in place of the default serialization. Default is None.
        :type encoder_class: Type[JSONEncoder], optional
        :return: True if successful. False if not.
        :rtype: bool
        """
        if file_path is None or obj is None:
            return False
        dir_name = os.path.dirname(file_path)
        temp_file_name = 'temp' + os.path.basename(file_path)
        temp_file_path = os.path.join(dir_name, temp_file_name)
        if encoder_class is not None:
            json_obj = json.dumps(obj, cls=encoder_class, indent=2)
        else:
            json_obj = json.dumps(obj, default=lambda o: o.serialize() if isinstance(o, CommonSerializable) else o.__dict__ if hasattr(o, '__dict__') else o, indent=2)

        with open(temp_file_path, mode='w+', buffering=buffering, encoding=encoding) as file:
            file.write(json_obj)
            file.flush()

        # File is empty.
        if os.stat(temp_file_path).st_size != 0:
            if os.path.exists(file_path):
                os.remove(file_path)
            os.rename(temp_file_path, file_path)
        else:
            os.remove(temp_file_path)
            raise Exception(f'Failed to write file {file_path}, it wrote empty for some reason!')
        return True

    @staticmethod
    def load_from_file(file_path: str, buffering: int=1, encoding: str='utf-8', decoder_class: Type[JSONDecoder]=None, object_hook: Callable[[Dict[str, Any]], Any]=None) -> Union[Any, None]:
        """load_from_file(file_path, buffering=1, encoding='utf-8', decoder_class=None, object_hook=None)

        Deserialize an object from a JSON file.

        :param file_path: The file to read from.
        :type: file_path: str
        :param buffering: See the built-in python :func:`~open` function documentation for more details.
        :type buffering: int, optional
        :param encoding: See the built-in python :func:`~open` function documentation for more details.
        :type encoding: str, optional
        :param decoder_class: Specify a custom JSON decoder class to use in place of the default deserialization. Default is None.
        :type decoder_class: Type[JSONDecoder], optional
        :param object_hook: A callable that will be called whenever a dictionary appears while decoding JSON. It can be used to create custom objects from data. Default is None.
        :type object_hook: Callable[[Dict[str, Any]], Any], optional
        :return: The contents of the file as an object or None if an error occurred.
        :rtype: Union[Any, None]
        """
        try:
            file_contents: str = CommonIOUtils.load_from_file(file_path, buffering=buffering, encoding=encoding)
            if file_contents is None:
                return None
            if len(file_contents) == 0:
                return None
            return json.loads(file_contents, cls=decoder_class, object_hook=object_hook)
        except Exception as ex:
            raise Exception(f'Failed to read file {file_path}, it is either corrupted, or happened to be locked at the time of trying to read it.') from ex

    @staticmethod
    def load_from_folder(
        folder_path: str,
        skip_file_names: Iterator[str]=(),
        buffering: int=1,
        encoding: str='utf-8',
        decoder_class: Type[JSONDecoder]=None,
        object_hook: Callable[[Dict[str, Any]], Any]=None,
        on_file_read_failure: Callable[[str, Exception], bool]=lambda *_, **__: True
    ) -> Union[Dict[str, Any], None]:
        """load_from_folder(\
            folder_path,\
            skip_file_names=(),\
            buffering=1,\
            encoding='utf-8',\
            decoder_class=None,\
            object_hook=None,\
            on_file_read_failure=lambda \*_, \*\*__: True\
        )

        Deserialize objects from a folder containing JSON files.

        :param folder_path: The folder to read from.
        :type: folder_path: str
        :param skip_file_names: A collection of file names to ignore. Default is an empty collection.
        :type skip_file_names: Iterator[str], optional
        :param buffering: See the built-in python :func:`~open` function documentation for more details.
        :type buffering: int, optional
        :param encoding: See the built-in python :func:`~open` function documentation for more details.
        :type encoding: str, optional
        :param decoder_class: Specify a custom JSON decoder class to use in place of the default deserialization. Default is None.
        :type decoder_class: Type[JSONDecoder], optional
        :param object_hook: A callable that will be called whenever a dictionary appears while decoding JSON. It can be used to create custom objects from data. Default is None.
        :type object_hook: Callable[[Dict[str, Any]], Any], optional
        :param on_file_read_failure: When a file fails to read due to an exception, this callback will be called. If the callback returns False, no more files will be read. If the callback returns True, the rest of the files will continue to be read. Default is a callback that returns True.
        :type on_file_read_failure: Callable[[str, Exception], bool], optional
        :return: A dictionary of the contents of each file within the specified folder organized by file name or None if the folder path does not exist.
        :rtype: Union[Dict[str, Any], None]
        """
        if not os.path.exists(folder_path):
            return None
        if skip_file_names is None:
            skip_file_names = tuple()
        skip_file_names = tuple(skip_file_names)
        skip_file_names = (
            *skip_file_names,
            '.DS_Store',
            'desktop.ini'
        )
        data = dict()
        for entry in os.scandir(folder_path):
            entry: DirEntry = entry
            if not entry.is_file() or entry.name is None or entry.name in skip_file_names:
                continue
            try:
                file_contents: str = CommonJSONIOUtils.load_from_file(entry.path, buffering=buffering, encoding=encoding, decoder_class=decoder_class, object_hook=object_hook)
            except Exception as ex:
                if not on_file_read_failure(entry.path, ex):
                    break
                continue
            if file_contents is None:
                continue
            data[entry.name] = file_contents
        return data
