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
