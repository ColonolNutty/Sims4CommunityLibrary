"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from sims.sim_info import SimInfo
from sims.sim_info_types import Gender


class CommonGenderUtils:
    """Utilities for manipulating Genders of Sims.

    """
    @staticmethod
    def get_gender(sim_info: SimInfo) -> Union[Gender, None]:
        """get_gender(sim_info)

        Retrieve the Gender of a Sim.

        :param sim_info: The Sim to retrieve the gender of.
        :type sim_info: SimInfo
        :return: The Gender of the Sim or None if a problem occurs.
        :rtype: Union[Gender, None]
        """
        if sim_info is None:
            return None
        if hasattr(sim_info, 'gender'):
            # noinspection PyPropertyAccess
            return sim_info.gender
        if hasattr(sim_info, 'sim_info') and hasattr(sim_info.sim_info, 'gender'):
            return sim_info.siminfo.gender
        return None

    @staticmethod
    def set_gender(sim_info: SimInfo, gender: Union[int, Gender]) -> bool:
        """set_gender(sim_info, gender)

        Set the Gender of a Sim.

        :param sim_info: The Sim to set the Gender of.
        :type sim_info: SimInfo
        :param gender: The Gender to set the Sim to.
        :type gender: Union[int, Gender]
        :return: True, if the Gender of the Sim was set successfully. False, if not.
        :rtype: bool
        """
        sim_info.gender = gender
        from sims4communitylib.events.sim.common_sim_event_dispatcher import CommonSimEventDispatcherService
        CommonSimEventDispatcherService()._on_sim_change_gender(sim_info)
        return True

    @staticmethod
    def swap_gender(sim_info: SimInfo, update_gender_options: bool=True) -> bool:
        """swap_gender(sim_info, update_gender_options=True)

        Swap the Gender of a Sim to it's opposite. i.e. Change a Sim from Male to Female or from Female to Male.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param update_gender_options: If True, gender option traits such as Toilet Usage, Clothing Preference, Pregnancy, and Body Frame will be updated to reflect the vanilla settings for each gender\
        For example, if a Human Sim is swapping from Female to Male, their gender options will be updated to Toilet Standing, Cannot Be Impregnated, Can Impregnate, Mens Wear clothing preference, and Masculine Frame.\
        If False, gender option traits will not be updated.\
        Default is True.
        :type update_gender_options: bool, optional
        :return: True, if the Gender of the Sim was swapped successfully. False, if not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        if CommonGenderUtils.is_male(sim_info):
            result = CommonGenderUtils.set_gender(sim_info, Gender.FEMALE)
            if not update_gender_options:
                return result
            CommonSimGenderOptionUtils.update_gender_options_to_vanilla_female(sim_info)
            return result
        elif CommonGenderUtils.is_female(sim_info):
            result = CommonGenderUtils.set_gender(sim_info, Gender.MALE)
            if not update_gender_options:
                return result
            CommonSimGenderOptionUtils.update_gender_options_to_vanilla_male(sim_info)
            return result
        return False

    @staticmethod
    def are_same_gender(sim_info: SimInfo, other_sim_info: SimInfo) -> bool:
        """are_same_gender(sim_info, other_sim_info)

        Determine if two Sims are the same Gender.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param other_sim_info: The Sim to compare to.
        :type other_sim_info: SimInfo
        :return: True, if both Sims are the same Gender. False, if not.
        :rtype: bool
        """
        return CommonGenderUtils.get_gender(sim_info) == CommonGenderUtils.get_gender(other_sim_info)

    @staticmethod
    def is_female_gender(gender: Gender) -> bool:
        """is_female_gender(gender)

        Determine if a Gender is Female.

        :param gender: The gender to check.
        :type gender: Gender
        :return: True, if the gender is female. False, if the gender is not female.
        :rtype: bool
        """
        return gender == Gender.FEMALE

    @staticmethod
    def is_male_gender(gender: Gender) -> bool:
        """is_male_gender(gender)

        Determine if a Gender is Male.

        :param gender: The gender to check.
        :type gender: Gender
        :return: True, if the gender is male. False, if the gender is not male.
        :rtype: bool
        """
        return gender == Gender.MALE

    @staticmethod
    def is_female(sim_info: SimInfo) -> bool:
        """is_female(sim_info)

        Determine if a Sim is Female.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is female. False, if the Sim is not female.
        :rtype: bool
        """
        return CommonGenderUtils.is_female_gender(CommonGenderUtils.get_gender(sim_info))

    @staticmethod
    def is_male(sim_info: SimInfo) -> bool:
        """is_male(sim_info)

        Determine if a Sim is Male.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :return: True, if the Sim is male. False, if the Sim is not male.
        :rtype: bool
        """
        return CommonGenderUtils.is_male_gender(CommonGenderUtils.get_gender(sim_info))
