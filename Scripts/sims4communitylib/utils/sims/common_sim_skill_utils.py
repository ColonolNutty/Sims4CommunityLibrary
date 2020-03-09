"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union
from sims.sim_info import SimInfo
from sims4communitylib.modinfo import ModInfo
from statistics.skill import Skill
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.sims.common_sim_statistic_utils import CommonSimStatisticUtils


class CommonSimSkillUtils:
    """Utilities for manipulating the Skills of Sims.

    """
    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=False)
    def has_skill(sim_info: SimInfo, skill_id: int) -> bool:
        """has_skill(sim_info, skill_id)

        Determine if a Sim has a Skill.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param skill_id: The identifier of the Skill to check.
        :type skill_id: int
        :return: True, if the Sim has the skill. False, if the Sim does not.
        :rtype: bool
        """
        return CommonSimStatisticUtils.has_statistic(sim_info, skill_id)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=False)
    def is_at_max_skill_level(sim_info: SimInfo, skill_id: int) -> bool:
        """is_at_max_skill_level(sim_info, skill_id)

        Determine if a Sim has reached the Maximum Level of a Skill.

        .. note:: Max level depends on the skill itself. Each skill can have a different max level.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param skill_id: The identifier of the Skill to check.
        :type skill_id: int
        :return: True, if the Sim has the skill at the maximum level. False, if the Sim does not.
        :rtype: bool
        """
        from statistics.skill import Skill
        statistic: Skill = CommonSimStatisticUtils.get_statistic(sim_info, skill_id)
        if statistic is None:
            return False
        return statistic.reached_max_level

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=False)
    def remove_skill(sim_info: SimInfo, skill_id: int) -> bool:
        """remove_skill(sim_info, skill_id)

        Remove a Skill from the specified Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param skill_id: The identifier of the Skill to remove.
        :type skill_id: int
        :return: True, if the skill was removed successfully. False, if not.
        :rtype: bool
        """
        return CommonSimStatisticUtils.remove_statistic(sim_info, skill_id)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=False)
    def set_progress_toward_max_skill_level(sim_info: SimInfo, skill_id: int, value: float, add: bool=True) -> bool:
        """set_progress_toward_max_skill_level(sim_info, skill_id, value, add=True)

        Set the amount of progress a Sim has made toward the max level of a Skill.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param skill_id: The identifier of the Skill to set.
        :type skill_id: int
        :param value: The amount to add.
        :type value: int
        :param add: If True, the skill will be added to the Sim before it is modified.
        :type add: bool, optional
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        return CommonSimStatisticUtils.set_statistic_value(sim_info, skill_id, value, add=add)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=False)
    def set_current_skill_level(sim_info: SimInfo, skill_id: int, level: float, add: bool=True) -> bool:
        """set_current_skill_level(sim_info, skill_id, level, add=True)

        Set the Skill Level of the Skill for the specified Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param skill_id: The identifier of the Skill to set.
        :type skill_id: int
        :param level: The level to set the skill to.
        :type level: int
        :param add: If True, the skill will be added to the Sim before it is modified.
        :type add: bool, optional
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        return CommonSimStatisticUtils.set_statistic_user_value(sim_info, skill_id, level, add=add)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=False)
    def translate_skill_progress(sim_info: SimInfo, skill_id_from: int, skill_id_to: int, add: bool=True) -> bool:
        """translate_skill_progress(sim_info, skill_id_from, skill_id_to, add=True)

        Translate the total progress of one Skill to the total progress of another Skill for the specified Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param skill_id_from: The identifier of the Skill being changed.
        :type skill_id_from: int
        :param skill_id_to: The identifier of the Skill being translated to.
        :type skill_id_to: int
        :param add: If True, the skill will be added to the Sim before it is modified.
        :type add: bool, optional
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        skill_level_value_from = CommonSimSkillUtils.get_progress_toward_next_skill_level(skill_id_from)
        skill_to = CommonSimSkillUtils.get_skill(sim_info, skill_id_to, add=add)
        if skill_to is None:
            return False
        level = skill_to.get_user_value()
        value_for_level = skill_to.get_skill_value_for_level(level)
        value_for_next_level = skill_to.get_skill_value_for_level(level + 1) - value_for_level
        level_of_new_skill = value_for_level + value_for_next_level * skill_level_value_from
        return CommonSimSkillUtils.set_progress_toward_max_skill_level(sim_info, skill_id_to, level_of_new_skill)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=False)
    def change_progress_toward_max_skill_level(sim_info: SimInfo, skill_id: int, value: float, add: bool=True) -> bool:
        """change_progress_toward_max_skill_level(sim_info, skill_id, value, add=True)

        Modify the amount of progress a Sim has made toward the max level of a Skill.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param skill_id: The identifier of the Skill to modify.
        :type skill_id: int
        :param value: The level to add or subtract to/from the skill.
        :type value: int
        :param add: If True, the skill will be added to the Sim before it is modified.
        :type add: bool, optional
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        return CommonSimStatisticUtils.add_statistic_value(sim_info, skill_id, value, add=add)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=False)
    def change_progress_toward_next_skill_level(sim_info: SimInfo, skill_id: int, value: float, add: bool=True) -> bool:
        """change_progress_toward_next_skill_level(sim_info, skill_id, value, add=True)

        Modify the amount of progress a Sim has made toward the next level of a Skill.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param skill_id: The identifier of the Skill to modify.
        :type skill_id: int
        :param value: The level to add or subtract to/from the skill.
        :type value: int
        :param add: If True, the skill will be added to the Sim before it is modified.
        :type add: bool, optional
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        skill = CommonSimSkillUtils.get_skill(sim_info, skill_id, add=add)
        if skill is None or skill.reached_max_level:
            return False
        current_skill_level = skill.get_user_value()
        current_skill_experience = skill.get_value()
        total_experience_for_level = skill.get_skill_value_for_level(current_skill_level)
        relative_experience_needed_for_next_level = skill.get_skill_value_for_level(current_skill_level + 1) - total_experience_for_level
        experience_gained_or_lost = relative_experience_needed_for_next_level / 100 * value
        skill_initial_value = getattr(skill, 'initial_value', 0.0)
        if current_skill_experience < skill_initial_value:
            experience_gained_or_lost = max(skill_initial_value, experience_gained_or_lost)
        return CommonSimSkillUtils.change_progress_toward_max_skill_level(sim_info, skill_id, experience_gained_or_lost)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=-1.0)
    def get_progress_toward_max_skill_level(sim_info: SimInfo, skill_id: int, add: bool=True) -> float:
        """get_progress_toward_max_skill_level(sim_info, skill_id, add=True)

        Retrieve the amount of progress a Sim has made toward the max level of a Skill.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param skill_id: The identifier of the Skill to modify.
        :type skill_id: int
        :param add: If True, the skill will be added to the Sim before it is modified.
        :type add: bool, optional
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        return CommonSimStatisticUtils.get_statistic_value(sim_info, skill_id, add=add)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=-1.0)
    def get_current_skill_level(sim_info: SimInfo, skill_id: int) -> float:
        """get_current_skill_level(sim_info, skill_id)

        Retrieve the Skill Level of a sim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param skill_id: The identifier of the Skill to use.
        :type skill_id: int
        :return: The current skill level of the specified Skill or `-1.0` if a problem occurs.
        :rtype: float
        """
        return CommonSimStatisticUtils.get_statistic_level(sim_info, skill_id)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=-1.0)
    def get_progress_toward_next_skill_level(sim_info: SimInfo, skill_id: int, add: bool=False) -> float:
        """get_progress_toward_next_skill_level(sim_info, skill_id, add=False)

        Retrieve the amount of progress a Sim has made toward the next level of a Skill.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param skill_id: The identifier of the Skill to use.
        :type skill_id: int
        :param add: If True, the skill will be added to the Sim before it is checked.
        :type add: bool, optional
        :return: The progress to the next level of the specified Skill or `-1.0` if a problem occurs.
        :rtype: float
        """
        skill = CommonSimSkillUtils.get_skill(sim_info, skill_id, add=add)
        if skill is None:
            return -1.0
        current_skill_level = skill.get_user_value()
        current_skill_experience = skill.get_value()
        experience_for_level = skill.get_skill_value_for_level(current_skill_level)
        experience_for_next_level = skill.get_skill_value_for_level(current_skill_level + 1) - experience_for_level
        if experience_for_level > 0.0 and experience_for_next_level > 0.0:
            return (current_skill_experience - experience_for_level) / experience_for_next_level
        return 0.0

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=None)
    def get_skill(sim_info: SimInfo, skill_id: int, add: bool=True) -> Union[Skill, None]:
        """get_skill(sim_info, skill_id, add=True)

        Retrieve a Skill for the specified Sim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param skill_id: The identifier of the Skill to use.
        :type skill_id: int
        :param add: If True, the skill will be added to the Sim before it is checked.
        :type add: bool, optional
        :return: An instance of a Skill of the Sim or None if the Skill does not exist.
        :rtype: Union[Skill, None]
        """
        return CommonSimStatisticUtils.get_statistic(sim_info, skill_id, add=add)
