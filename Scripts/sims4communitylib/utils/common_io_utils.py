"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""


class CommonIOUtils:
    """
        Utilities for handling reading/writing to and from files.
    """
    # noinspection PyBroadException
    @staticmethod
    def write_to_file(file_path: str, data: str, buffering: int=1, encoding: str='utf-8'):
        """
            Write string data to a file.
        :param encoding: See the 'open' function documentation for more details
        :param buffering: See the 'open' function documentation for more details
        :param file_path: The file to write to.
        :param data: The data to write.
        :return: True if successful.
        """
        if file_path is None or data is None:
            return False
        try:
            opened_file = open(file_path, mode='a', buffering=buffering, encoding=encoding)
            opened_file.write(data)
            opened_file.flush()
            opened_file.close()
        except Exception:
            return False
        return True
