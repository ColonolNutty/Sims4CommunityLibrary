"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Tuple

from interactions.base.picker_interaction import PickerInteractionDeliveryMethod
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonObjectDeliveryMethod(CommonInt):
    """A method of delivery for objects."""
    NONE: 'CommonObjectDeliveryMethod' = ...
    DELIVERY_SERVICE: 'CommonObjectDeliveryMethod' = ...
    INVENTORY: 'CommonObjectDeliveryMethod' = ...
    MAIL: 'CommonObjectDeliveryMethod' = ...

    @classmethod
    def get_all(cls, exclude_values: Iterator['CommonObjectDeliveryMethod'] = None) -> Tuple['CommonObjectDeliveryMethod']:
        """get_all(exclude_values=None)

        Get a collection of all values.

        :param exclude_values: These values will be excluded. If set to None, NONE will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonObjectDeliveryMethod], optional
        :return: A collection of all values.
        :rtype: Tuple[CommonObjectDeliveryMethod]
        """
        if exclude_values is None:
            exclude_values = (cls.NONE,)
        # noinspection PyTypeChecker
        value_list: Tuple[CommonObjectDeliveryMethod, ...] = tuple([value for value in cls.values if value not in exclude_values])
        return value_list

    @classmethod
    def get_all_names(cls, exclude_values: Iterator['CommonObjectDeliveryMethod'] = None) -> Tuple[str]:
        """get_all_names(exclude_values=None)

        Retrieve a collection of the names of all values.

        :param exclude_values: These values will be excluded. If set to None, NONE will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonObjectDeliveryMethod], optional
        :return: A collection of the names of all values.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all(exclude_values=exclude_values)])
        return name_list

    @classmethod
    def get_comma_separated_names_string(cls, exclude_values: Iterator['CommonObjectDeliveryMethod'] = None) -> str:
        """get_comma_separated_names_string(exclude_values=None)

        Create a string containing all names of all values, separated by a comma.

        :param exclude_values: These values will be excluded. If set to None, NONE will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonObjectDeliveryMethod], optional
        :return: A string containing all names of all values, separated by a comma.
        :rtype: str
        """
        return ', '.join(cls.get_all_names(exclude_values=exclude_values))

    @staticmethod
    def convert_to_vanilla(value: 'CommonObjectDeliveryMethod') -> PickerInteractionDeliveryMethod:
        """convert_to_vanilla(value)

        Convert a value into the vanilla PickerInteractionDeliveryMethod enum.

        :param value: An instance of CommonObjectDeliveryMethod
        :type value: CommonObjectDeliveryMethod
        :return: The specified value translated to PickerInteractionDeliveryMethod or INVENTORY if the value could not be translated.
        :rtype: PickerInteractionDeliveryMethod
        """
        if value is None or value == CommonObjectDeliveryMethod.NONE:
            return PickerInteractionDeliveryMethod.INVENTORY
        if isinstance(value, PickerInteractionDeliveryMethod):
            # noinspection PyTypeChecker
            return value
        mapping = {
            CommonObjectDeliveryMethod.INVENTORY: PickerInteractionDeliveryMethod.INVENTORY,
            CommonObjectDeliveryMethod.MAIL: PickerInteractionDeliveryMethod.MAILMAN,
            CommonObjectDeliveryMethod.DELIVERY_SERVICE: PickerInteractionDeliveryMethod.DELIVERY_SERVICE_NPC,
        }
        return mapping.get(value, PickerInteractionDeliveryMethod.INVENTORY)

    @staticmethod
    def convert_from_vanilla(value: PickerInteractionDeliveryMethod) -> 'CommonObjectDeliveryMethod':
        """convert_from_vanilla(value)

        Convert a value into a CommonObjectDeliveryMethod enum.

        :param value: An instance of PickerInteractionDeliveryMethod
        :type value: PickerInteractionDeliveryMethod
        :return: The specified value translated to CommonObjectDeliveryMethod or INVENTORY if the value could not be translated.
        :rtype: CommonObjectDeliveryMethod
        """
        if value is None or value == CommonObjectDeliveryMethod.NONE:
            return PickerInteractionDeliveryMethod.INVENTORY
        if isinstance(value, PickerInteractionDeliveryMethod):
            # noinspection PyTypeChecker
            return value
        mapping = {
            PickerInteractionDeliveryMethod.INVENTORY: CommonObjectDeliveryMethod.INVENTORY,
            PickerInteractionDeliveryMethod.MAILMAN: CommonObjectDeliveryMethod.MAIL,
            PickerInteractionDeliveryMethod.DELIVERY_SERVICE_NPC: CommonObjectDeliveryMethod.DELIVERY_SERVICE,
        }
        return mapping.get(value, CommonObjectDeliveryMethod.INVENTORY)
