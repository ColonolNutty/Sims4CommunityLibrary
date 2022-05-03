"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Tuple

from sims4communitylib.enums.enumtypes.common_int_flags import CommonIntFlags
from sims4communitylib.utils.common_collection_utils import CommonCollectionUtils


class CommonBitwiseUtils:
    """Utilities for performing bitwise operations, so you do not have to remember how they are done."""

    @staticmethod
    def add_flags(value: Union[CommonIntFlags, int], flags: Union[CommonIntFlags, int, Tuple[Union[CommonIntFlags, int]]]) -> Union[CommonIntFlags, int]:
        """add_flags(value, flags)

        Add Flags to a value.

        :param value: A flags enum or an integer.
        :type value: Union[CommonIntFlags, int]
        :param flags: A flags enum, an integer, or a collection of flags enums or integers.
        :type flags: Union[CommonIntFlags, int, Tuple[Union[CommonIntFlags, int]]]
        :return: The new value.
        :rtype: Union[CommonIntFlags, int]
        """
        if CommonCollectionUtils.is_collection(value):
            for _flags in flags:
                value = CommonBitwiseUtils.add_flags(value, _flags)
            return value
        return value | flags

    @staticmethod
    def remove_flags(value: Union[CommonIntFlags, int], flags: Union[CommonIntFlags, int, Tuple[Union[CommonIntFlags, int]]]) -> Union[CommonIntFlags, int]:
        """remove_flags(value, flags)

        Remove Flags from a value.

        :param value: A flags enum or an integer.
        :type value: Union[CommonIntFlags, int]
        :param flags: A flags enum, an integer, or a collection of flags enums or integers.
        :type flags: Union[CommonIntFlags, int, Tuple[Union[CommonIntFlags, int]]]
        :return: The new value.
        :rtype: Union[CommonIntFlags, int]
        """
        if CommonCollectionUtils.is_collection(flags):
            for _flags in flags:
                value = CommonBitwiseUtils.remove_flags(value, _flags)
            return value
        return value & ~flags

    @staticmethod
    def contains_all_flags(value: Union[CommonIntFlags, int], flags: Union[CommonIntFlags, int, Tuple[Union[CommonIntFlags, int]]]) -> bool:
        """contains_all_flags(value, flags)

        Determine if all of the Flags are found within a value.

        :param value: A flags enum or an integer.
        :type value: Union[CommonIntFlags, int]
        :param flags: A flags enum, an integer, or a collection of flags enums or integers.
        :type flags: Union[CommonIntFlags, int, Tuple[Union[CommonIntFlags, int]]]
        :return: True, if all of the specified Flags are found within the value. False, if not.
        :rtype: bool
        """
        if CommonCollectionUtils.is_collection(flags):
            for _flags in flags:
                if not CommonBitwiseUtils.contains_all_flags(value, _flags):
                    return False
            return True
        return flags == (flags & value)

    @staticmethod
    def contains_any_flags(value: Union[CommonIntFlags, int], flags: Union[CommonIntFlags, int, Tuple[Union[CommonIntFlags, int]]]) -> bool:
        """contains_any_flags(value, flags)

        Determine if any of the Flags are found within a value.

        :param value: A flags enum or an integer.
        :type value: Union[CommonIntFlags, int]
        :param flags: A flags enum, an integer, or a collection of flags enums or integers.
        :type flags: Union[CommonIntFlags, int, Tuple[Union[CommonIntFlags, int]]]
        :return: True, if any of the specified Flags are found within the value. False, if not.
        :rtype: bool
        """
        if CommonCollectionUtils.is_collection(flags):
            for _flags in flags:
                if CommonBitwiseUtils.contains_any_flags(value, _flags):
                    return True
            return False
        return (flags & value) != 0

    @staticmethod
    def contains_no_flags(value: Union[CommonIntFlags, int], flags: Union[CommonIntFlags, int, Tuple[Union[CommonIntFlags, int]]]) -> bool:
        """contains_no_flags(value, flags)

        Determine if none of the Flags are found within a value.

        :param value: A flags enum or an integer.
        :type value: Union[CommonIntFlags, int]
        :param flags: A flags enum, an integer, or a collection of flags enums or integers.
        :type flags: Union[CommonIntFlags, int, Tuple[Union[CommonIntFlags, int]]]
        :return: True, if none of the specified Flags are found within the value. False, if not.
        :rtype: bool
        """
        return not CommonBitwiseUtils.contains_any_flags(value, flags)
