"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""


class CommonTextUtils:
    """Utilities for manipulating text."""
    @staticmethod
    def capitalize(value: str) -> str:
        """capitalize(value)

        Capitalize the first character of a value.

        :param value: The value to modify.
        :type value: str
        :return: The text, but with the first character capitalized.
        :rtype: str
        """
        if not value:
            return value
        return value[:1].upper() + value[1:]

    @staticmethod
    def proper_case_hex(hex_value: str) -> str:
        """proper_case_hex(hex_value)

        Modify the casing of a hex value so that everything after the "0x" portion is capitalized.

        :param hex_value: The value to modify.
        :type hex_value: str
        :return: The value, but with everything after the "0x" portion capitalized.
        :rtype: str
        """
        if not hex_value:
            return hex_value
        return hex_value[:2] + hex_value[2:].upper()

    @staticmethod
    def convert_to_hex32_string(value: int) -> str:
        """convert_to_hex32_string(value)

        Convert a value into a 32 bit hexadecimal string. This function will keep any leading or trailing zeros.

        :param value: The value to convert.
        :type value: int
        :return: The value as a Hexadecimal string.
        :rtype: str
        """
        if value is None:
            raise AssertionError('value was None!')
        return f'0x{value:08X}'

    @staticmethod
    def to_truncated_decimal(value: float, num_of_decimal_points: int = 2) -> str:
        """to_truncated_decimal(value, num_of_decimal_points=2)

        Create a string of a float value with a number of decimal points truncated.

        :param value: The value to truncate.
        :type value: float
        :param num_of_decimal_points: The number of decimal places to leave in the string. Default is 2.
        :type num_of_decimal_points: int, optional
        :return: A string representation of the value truncated to the number of decimal places.
        :rtype: str
        """
        return f'{value:.{num_of_decimal_points}f}'
