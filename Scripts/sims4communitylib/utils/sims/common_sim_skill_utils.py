"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union
from sims.sim_info import SimInfo
from sims4communitylib.modinfo import ModInfo
from statistics.skill import Skill
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.sims.common_sim_statistic_utils import CommonSimStatisticUtils


class CommonSimSkillUtils:
    """ Utilities for manipulating the Skills of Sims. """
    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def has_skill(sim_info: SimInfo, skill_id: int) -> bool:
        """ Determine if the specified Sim has a Skill. """
        return CommonSimStatisticUtils.has_statistic(sim_info, skill_id)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def is_at_max_skill_level(sim_info: SimInfo, skill_id: int) -> bool:
        """ Determine if a Sim has reached the Maximum Level of a Skill. """
        from statistics.skill import Skill
        statistic: Skill = CommonSimStatisticUtils.get_statistic(sim_info, skill_id)
        if statistic is None:
            return False
        return statistic.reached_max_level

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def remove_skill(sim_info: SimInfo, skill_id: int) -> bool:
        """ Remove a Skill from the specified Sim. """
        return CommonSimStatisticUtils.remove_statistic(sim_info, skill_id)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def set_progress_toward_max_skill_level(sim_info: SimInfo, skill_id: int, value: float, add: bool=True) -> bool:
        """ Set the amount of progress a Sim has made toward the max level of a Skill.  """
        return CommonSimStatisticUtils.set_statistic_value(sim_info, skill_id, value, add=add)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def set_current_skill_level(sim_info: SimInfo, skill_id: int, level: float, add: bool=True) -> bool:
        """ Set the Skill Level of the Skill for the specified Sim. """
        return CommonSimStatisticUtils.set_statistic_user_value(sim_info, skill_id, level, add=add)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def translate_skill_progress(sim_info: SimInfo, skill_id_from: int, skill_id_to: int, add: bool=True) -> bool:
        """
            Translate the total progress of one Skill to the total progress of another Skill for the specified Sim.
        :return: True if successful.
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
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def change_progress_toward_max_skill_level(sim_info: SimInfo, skill_id: int, value: float, add: bool=True) -> bool:
        """ Modify the amount of progress a Sim has made toward the max level of a Skill. """
        return CommonSimStatisticUtils.add_statistic_value(sim_info, skill_id, value, add=add)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=False)
    def change_progress_toward_next_skill_level(sim_info: SimInfo, skill_id: int, value: float, add: bool=True) -> bool:
        """
            Modify the amount of progress a Sim has made toward the next level of a Skill.
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
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=-1.0)
    def get_progress_toward_max_skill_level(sim_info: SimInfo, skill_id: int, add: bool=True) -> float:
        """ Retrieve the amount of progress a Sim has made toward the max level of a Skill.  """
        return CommonSimStatisticUtils.get_statistic_value(sim_info, skill_id, add=add)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=-1.0)
    def get_current_skill_level(sim_info: SimInfo, skill_id: int) -> float:
        """ Retrieve the Skill Level of a sim. """
        return CommonSimStatisticUtils.get_statistic_level(sim_info, skill_id)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=-1.0)
    def get_progress_toward_next_skill_level(sim_info: SimInfo, skill_id: int, add: bool=False) -> float:
        """
            Retrieve the amount of progress a Sim has made toward the next level of a Skill.
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
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=None)
    def get_skill(sim_info: SimInfo, skill_id: int, add: bool=True) -> Union[Skill, None]:
        """ Retrieve a Skill for the specified Sim. """
        return CommonSimStatisticUtils.get_statistic(sim_info, skill_id, add=add)
