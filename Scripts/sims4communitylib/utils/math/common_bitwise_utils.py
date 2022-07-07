"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Tuple, TypeVar

from sims4communitylib.enums.enumtypes.common_int_flags import CommonIntFlags
from sims4communitylib.utils.common_collection_utils import CommonCollectionUtils

CommonEnumFlagsTypeValueType = TypeVar('CommonEnumFlagsTypeValueType', int, CommonIntFlags)


class CommonBitwiseUtils:
    """Utilities for performing bitwise operations, so you do not have to remember how they are done."""

    @staticmethod
    def add_flags(value: CommonEnumFlagsTypeValueType, flags: Union[CommonEnumFlagsTypeValueType, Tuple[CommonEnumFlagsTypeValueType]]) -> CommonEnumFlagsTypeValueType:
        """add_flags(value, flags)

        Add Flags to a value.

        :param value: A flags enum or an integer.
        :type value: CommonEnumFlagsTypeValueType
        :param flags: A flags enum, an integer, or a collection of flags enums or integers.
        :type flags: Union[CommonIntFlags, int, Tuple[CommonEnumFlagsTypeValueType]]
        :return: The new value.
        :rtype: CommonEnumFlagsTypeValueType
        """
        if CommonCollectionUtils.is_collection(value):
            for _flags in flags:
                value = CommonBitwiseUtils.add_flags(value, _flags)
            return value
        return value | flags

    @staticmethod
    def remove_flags(value: CommonEnumFlagsTypeValueType, flags: Union[CommonIntFlags, int, Tuple[CommonEnumFlagsTypeValueType]]) -> CommonEnumFlagsTypeValueType:
        """remove_flags(value, flags)

        Remove Flags from a value.

        :param value: A flags enum or an integer.
        :type value: CommonEnumFlagsTypeValueType
        :param flags: A flags enum, an integer, or a collection of flags enums or integers.
        :type flags: Union[CommonIntFlags, int, Tuple[CommonEnumFlagsTypeValueType]]
        :return: The new value.
        :rtype: CommonEnumFlagsTypeValueType
        """
        if CommonCollectionUtils.is_collection(flags):
            for _flags in flags:
                value = CommonBitwiseUtils.remove_flags(value, _flags)
            return value
        return value & ~flags

    @staticmethod
    def contains_all_flags(value: CommonEnumFlagsTypeValueType, flags: Union[CommonIntFlags, int, Tuple[CommonEnumFlagsTypeValueType]]) -> bool:
        """contains_all_flags(value, flags)

        Determine if all of the Flags are found within a value.

        :param value: A flags enum or an integer.
        :type value: CommonEnumFlagsTypeValueType
        :param flags: A flags enum, an integer, or a collection of flags enums or integers.
        :type flags: Union[CommonIntFlags, int, Tuple[CommonEnumFlagsTypeValueType]]
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
    def contains_any_flags(value: CommonEnumFlagsTypeValueType, flags: Union[CommonIntFlags, int, Tuple[CommonEnumFlagsTypeValueType]]) -> bool:
        """contains_any_flags(value, flags)

        Determine if any of the Flags are found within a value.

        :param value: A flags enum or an integer.
        :type value: CommonEnumFlagsTypeValueType
        :param flags: A flags enum, an integer, or a collection of flags enums or integers.
        :type flags: Union[CommonIntFlags, int, Tuple[CommonEnumFlagsTypeValueType]]
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
    def contains_no_flags(value: CommonEnumFlagsTypeValueType, flags: Union[CommonIntFlags, int, Tuple[CommonEnumFlagsTypeValueType]]) -> bool:
        """contains_no_flags(value, flags)

        Determine if none of the Flags are found within a value.

        :param value: A flags enum or an integer.
        :type value: CommonEnumFlagsTypeValueType
        :param flags: A flags enum, an integer, or a collection of flags enums or integers.
        :type flags: Union[CommonIntFlags, int, Tuple[CommonEnumFlagsTypeValueType]]
        :return: True, if none of the specified Flags are found within the value. False, if not.
        :rtype: bool
        """
        return not CommonBitwiseUtils.contains_any_flags(value, flags)
