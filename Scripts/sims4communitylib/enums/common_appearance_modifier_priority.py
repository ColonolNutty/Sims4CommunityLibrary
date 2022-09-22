"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Iterator, Tuple

from buffs.appearance_modifier.appearance_modifier import AppearanceModifierPriority
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonAppearanceModifierPriority(CommonInt):
    """Priorities for appearance modifiers. These priorities determine the order in which appearance modifiers are applied, which ones override which."""
    INVALID: 'CommonAppearanceModifierPriority' = ...
    FROZEN: 'CommonAppearanceModifierPriority' = ...
    MANNEQUIN: 'CommonAppearanceModifierPriority' = ...
    PATIENT: 'CommonAppearanceModifierPriority' = ...
    SICKNESS: 'CommonAppearanceModifierPriority' = ...
    TRANSFORMED: 'CommonAppearanceModifierPriority' = ...

    @classmethod
    def get_all(cls, exclude_values: Iterator['CommonAppearanceModifierPriority'] = None) -> Tuple['CommonAppearanceModifierPriority']:
        """get_all(exclude_values=None)

        Get a collection of all values.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonAppearanceModifierPriority], optional
        :return: A collection of all values.
        :rtype: Tuple[CommonAppearanceModifierPriority]
        """
        if exclude_values is None:
            exclude_values = (cls.INVALID,)
        # noinspection PyTypeChecker
        value_list: Tuple[CommonAppearanceModifierPriority, ...] = tuple([value for value in cls.values if value not in exclude_values])
        return value_list

    @classmethod
    def get_all_names(cls, exclude_values: Iterator['CommonAppearanceModifierPriority'] = None) -> Tuple[str]:
        """get_all_names(exclude_values=None)

        Retrieve a collection of the names of all values.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonAppearanceModifierPriority], optional
        :return: A collection of the names of all values.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all(exclude_values=exclude_values)])
        return name_list

    @classmethod
    def get_comma_separated_names_string(cls, exclude_values: Iterator['CommonAppearanceModifierPriority'] = None) -> str:
        """get_comma_separated_names_string(exclude_values=None)

        Create a string containing all names of all values, separated by a comma.

        :param exclude_values: These values will be excluded. If set to None, INVALID will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonAppearanceModifierPriority], optional
        :return: A string containing all names of all values, separated by a comma.
        :rtype: str
        """
        return ', '.join(cls.get_all_names(exclude_values=exclude_values))

    @staticmethod
    def convert_to_vanilla(value: 'CommonAppearanceModifierPriority') -> AppearanceModifierPriority:
        """convert_to_vanilla(value)

        Convert a value into the vanilla AppearanceModifierPriority enum.

        :param value: An instance of CommonAppearanceModifierPriority
        :type value: CommonAppearanceModifierPriority
        :return: The specified value translated to AppearanceModifierPriority or INVALID if the value could not be translated.
        :rtype: AppearanceModifierPriority
        """
        if value is None or value == CommonAppearanceModifierPriority.INVALID:
            return AppearanceModifierPriority.INVALID
        if isinstance(value, AppearanceModifierPriority):
            return value
        mapping = dict()
        if hasattr(AppearanceModifierPriority, 'MANNEQUIN'):
            mapping[CommonAppearanceModifierPriority.MANNEQUIN] = AppearanceModifierPriority.MANNEQUIN
        if hasattr(AppearanceModifierPriority, 'SICKNESS'):
            mapping[CommonAppearanceModifierPriority.SICKNESS] = AppearanceModifierPriority.SICKNESS
        if hasattr(AppearanceModifierPriority, 'PATIENT'):
            mapping[CommonAppearanceModifierPriority.PATIENT] = AppearanceModifierPriority.PATIENT
        if hasattr(AppearanceModifierPriority, 'TRANSFORMED'):
            mapping[CommonAppearanceModifierPriority.TRANSFORMED] = AppearanceModifierPriority.TRANSFORMED
        if hasattr(AppearanceModifierPriority, 'FROZEN'):
            mapping[CommonAppearanceModifierPriority.FROZEN] = AppearanceModifierPriority.FROZEN
        return mapping.get(value, AppearanceModifierPriority.INVALID)

    @staticmethod
    def convert_from_vanilla(value: Union[int, AppearanceModifierPriority]) -> 'CommonAppearanceModifierPriority':
        """convert_from_vanilla(value)

        Convert a value into a CommonAppearanceModifierPriority enum.

        :param value: An instance of AppearanceModifierPriority
        :type value: AppearanceModifierPriority
        :return: The specified value translated to CommonAppearanceModifierPriority or INVALID if the value could not be translated.
        :rtype: CommonAppearanceModifierPriority
        """
        if value is None or value == AppearanceModifierPriority.INVALID:
            return CommonAppearanceModifierPriority.INVALID
        if isinstance(value, CommonAppearanceModifierPriority):
            return value
        mapping = dict()
        if hasattr(AppearanceModifierPriority, 'MANNEQUIN'):
            mapping[AppearanceModifierPriority.MANNEQUIN] = CommonAppearanceModifierPriority.MANNEQUIN
        if hasattr(AppearanceModifierPriority, 'SICKNESS'):
            mapping[AppearanceModifierPriority.SICKNESS] = CommonAppearanceModifierPriority.SICKNESS
        if hasattr(AppearanceModifierPriority, 'PATIENT'):
            mapping[AppearanceModifierPriority.PATIENT] = CommonAppearanceModifierPriority.PATIENT
        if hasattr(AppearanceModifierPriority, 'TRANSFORMED'):
            mapping[AppearanceModifierPriority.TRANSFORMED] = CommonAppearanceModifierPriority.TRANSFORMED
        if hasattr(AppearanceModifierPriority, 'FROZEN'):
            mapping[AppearanceModifierPriority.FROZEN] = CommonAppearanceModifierPriority.FROZEN
        return mapping.get(value, CommonAppearanceModifierPriority.INVALID)
