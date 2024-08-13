"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict, Union

from sims.global_gender_preference_tuning import GenderPreferenceType
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonGenderPreferenceType(CommonInt):
    """Custom Gender Preference Type enum.

    """
    INVALID: 'CommonGenderPreferenceType' = 0
    ROMANTIC: 'CommonGenderPreferenceType' = 1
    WOOHOO: 'CommonGenderPreferenceType' = 2

    @staticmethod
    def convert_to_vanilla(value: 'CommonGenderPreferenceType') -> Union[GenderPreferenceType, None]:
        """convert_to_vanilla(value)

        Convert a CommonGenderPreferenceType into the vanilla GenderPreferenceType enum.

        :param value: An instance of Common Gender Preference Type
        :type value: CommonGenderPreferenceType
        :return: The specified CommonGenderPreferenceType translated to GenderPreferenceType or None if the value could not be translated.
        :rtype: Union[GenderPreferenceType, None]
        """
        if value is None or value == CommonGenderPreferenceType.INVALID:
            return GenderPreferenceType.INVALID
        if isinstance(value, GenderPreferenceType):
            return value
        conversion_mapping: Dict[CommonGenderPreferenceType, GenderPreferenceType] = {
            CommonGenderPreferenceType.INVALID: GenderPreferenceType.INVALID,
            CommonGenderPreferenceType.ROMANTIC: GenderPreferenceType.ROMANTIC,
            CommonGenderPreferenceType.WOOHOO: GenderPreferenceType.WOOHOO,
        }
        return conversion_mapping.get(value, None)

    @staticmethod
    def convert_from_vanilla(value: Union[int, GenderPreferenceType]) -> 'CommonGenderPreferenceType':
        """convert_from_vanilla(value)

        Convert a vanilla GenderPreferenceType to a CommonGenderPreferenceType.

        :param value: An instance of Gender Preference Type
        :type value: GenderPreferenceType
        :return: The specified GenderPreferenceType translated to CommonGenderPreferenceType or INVALID if the value could not be translated.
        :rtype: CommonGenderPreferenceType
        """
        if value is None or value == GenderPreferenceType.INVALID:
            return CommonGenderPreferenceType.INVALID
        if isinstance(value, CommonGenderPreferenceType):
            return value
        conversion_mapping: Dict[int, CommonGenderPreferenceType] = {
            int(GenderPreferenceType.INVALID): CommonGenderPreferenceType.INVALID,
            int(GenderPreferenceType.ROMANTIC): CommonGenderPreferenceType.ROMANTIC,
            int(GenderPreferenceType.WOOHOO): CommonGenderPreferenceType.WOOHOO
        }
        value = int(value)
        if value not in conversion_mapping:
            return CommonGenderPreferenceType.INVALID
        return conversion_mapping[value]
