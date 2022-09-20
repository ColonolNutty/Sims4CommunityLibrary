"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Iterator

from server_commands.argument_helpers import TunableInstanceParam
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.enums.skills_enum import CommonSkillId
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.resources.common_skill_utils import CommonSkillUtils
from statistics.skill import Skill


class CommonSimSkillUtils:
    """Utilities for manipulating the Skills of Sims.

    """
    @staticmethod
    def has_skill(sim_info: SimInfo, skill: Union[int, CommonSkillId, Skill]) -> bool:
        """has_skill(sim_info, skill)

        Determine if a Sim has a Skill.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param skill: The identifier of the Skill to check.
        :type skill: Union[int, CommonSkillId, Skill]
        :return: True, if the Sim has the skill. False, if the Sim does not.
        :rtype: bool
        """
        return CommonSimSkillUtils.get_skill(sim_info, skill, add=False) is not None

    # noinspection PyUnusedLocal
    @staticmethod
    def set_current_skill_level(sim_info: SimInfo, skill: Union[int, CommonSkillId, Skill], level: float, add: bool = True) -> bool:
        """set_current_skill_level(sim_info, skill, level, add=True)

        Set the current skill level of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param skill: The decimal identifier of a Skill.
        :type skill: Union[int, CommonSkillId, Skill]
        :param level: The level to set the skill to.
        :type skill: Union[int, CommonSkillId, Skill]
        :param add: OBSOLETE AND IGNORED ARGUMENT! When setting the skill level for a Sim, the Skill will always be added first.
        :type add: bool, optional
        :return: True, if successful. False, if not successful, the skill does not exist, or the skill is not valid for the Sim.
        :rtype: bool
        """
        sim_skill: Skill = CommonSimSkillUtils.get_skill(sim_info, skill, add=add)
        if sim_skill is None:
            return False
        new_skill_experience = sim_skill.convert_from_user_value(level)
        sim_skill.set_value(new_skill_experience)
        return True

    @staticmethod
    def set_current_skill_level_to_max(sim_info: SimInfo, skill: Union[int, CommonSkillId, Skill]) -> bool:
        """set_current_skill_level_to_max(sim_info, skill, add=True)

        Set the current skill level of a Sim to its maximum value.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param skill: The decimal identifier of a Skill.
        :type skill: Union[int, CommonSkillId, Skill]
        :return: True, if successful. False, if not successful, the skill does not exist, or the skill is not valid for the Sim.
        :rtype: bool
        """
        skill: Skill = CommonSkillUtils.load_skill_by_id(skill)
        if skill is None:
            return False
        return CommonSimSkillUtils.set_current_skill_level(sim_info, skill, skill.max_level)

    @staticmethod
    def get_current_skill_level(sim_info: SimInfo, skill: Union[int, CommonSkillId, Skill], use_effective_skill_level: bool = True) -> float:
        """get_current_skill_level(\
            sim_info,\
            skill,\
            use_effective_skill_level=True\
        )

        Retrieve the current skill level of a Sim for a Skill.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param skill: The decimal identifier of a Skill.
        :type skill: Union[int, CommonSkillId, Skill]
        :param use_effective_skill_level: If True, any skill modifiers will be taken into account, such as buffs, traits, etc. If False, the skill level without modifiers will be returned. True only works if the Sim is instanced. Default is True.
        :type use_effective_skill_level: bool, optional
        :return: The current level the Sim is at for the specified Skill or 0.0 if the Skill is either not available or the Sim does not have it.
        :rtype: float
        """
        skill: Skill = CommonSkillUtils.load_skill_by_id(skill)
        if skill is None:
            return 0.0
        skill_or_skill_type = sim_info.get_statistic(skill, add=False) or skill
        if use_effective_skill_level and sim_info.is_instanced():
            skill_level: float = sim_info.get_effective_skill_level(skill_or_skill_type)
        else:
            skill_level: float = skill_or_skill_type.get_user_value()
        return skill_level

    @staticmethod
    def is_at_max_skill_level(sim_info: SimInfo, skill: Union[int, CommonSkillId, Skill], use_effective_skill_level: bool = True) -> bool:
        """is_at_max_skill_level(\
            sim_info,\
            skill,\
            use_effective_skill_level=True\
        )

        Determine if a Sim has reached the Maximum Level of a Skill.

        .. note:: Max level depends on the skill itself. Each skill can have a different max level.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param skill: The identifier of the Skill to check.
        :type skill: Union[int, CommonSkillId, Skill]
        :param use_effective_skill_level: If True, any skill modifiers will be taken into account, such as buffs, traits, etc. If False, the skill level without modifiers will be returned. True only works if the Sim is instanced. Default is True.
        :type use_effective_skill_level: bool, optional
        :return: True, if the Sim has the skill at the maximum level. False, if the Sim does not.
        :rtype: bool
        """
        skill: Skill = CommonSkillUtils.load_skill_by_id(skill)
        if skill is None:
            return False
        sim_skill_level = CommonSimSkillUtils.get_current_skill_level(
            sim_info,
            skill,
            use_effective_skill_level=use_effective_skill_level
        )
        return sim_skill_level >= skill.max_level

    @staticmethod
    def remove_skill(sim_info: SimInfo, skill: Union[int, CommonSkillId, Skill]) -> bool:
        """remove_skill(sim_info, skill)

        Remove a Skill from the specified Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param skill: The identifier of the Skill to remove.
        :type skill: Union[int, CommonSkillId, Skill]
        :return: True, if the skill was removed successfully. False, if not.
        :rtype: bool
        """
        skill: Skill = CommonSkillUtils.load_skill_by_id(skill)
        if skill is None:
            return False
        sim_info.remove_statistic(skill)
        return True

    @staticmethod
    def set_progress_toward_max_skill_level(sim_info: SimInfo, skill: Union[int, CommonSkillId, Skill], value: float, add: bool = True) -> bool:
        """set_progress_toward_max_skill_level(sim_info, skill, value, add=True)

        Set the amount of progress a Sim has made toward the max level of a Skill.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param skill: The identifier of the Skill to set.
        :type skill: Union[int, CommonSkillId, Skill]
        :param value: The amount to add.
        :type value: Union[int, CommonSkillId, Skill]
        :param add: If True, the skill will be added to the Sim before it is modified.
        :type add: bool, optional
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        sim_skill: Skill = CommonSimSkillUtils.get_skill(sim_info, skill, add=add)
        if sim_skill is None:
            return False
        sim_skill.set_value(value)
        return True

    @staticmethod
    def get_progress_toward_max_skill_level(sim_info: SimInfo, skill: Union[int, CommonSkillId, Skill], add: bool = True) -> float:
        """get_progress_toward_max_skill_level(sim_info, skill, add=True)

        Retrieve the amount of progress a Sim has made toward the max level of a Skill.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param skill: The identifier of the Skill to modify.
        :type skill: Union[int, CommonSkillId, Skill]
        :param add: If True, the skill will be added to the Sim before it is modified.
        :type add: bool, optional
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        sim_skill: Skill = CommonSimSkillUtils.get_skill(sim_info, skill, add=add)
        if sim_skill is None:
            return False
        sim_skill.get_value()
        return True

    @staticmethod
    def change_progress_toward_max_skill_level(sim_info: SimInfo, skill: Union[int, CommonSkillId, Skill], value: float, add: bool = True) -> bool:
        """change_progress_toward_max_skill_level(sim_info, skill, value, add=True)

        Modify the amount of progress a Sim has made toward the max level of a Skill.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param skill: The identifier of the Skill to modify.
        :type skill: Union[int, CommonSkillId, Skill]
        :param value: The level to add or subtract to/from the skill.
        :type value: Union[int, CommonSkillId, Skill]
        :param add: If True, the skill will be added to the Sim before it is modified.
        :type add: bool, optional
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        sim_skill: Skill = CommonSimSkillUtils.get_skill(sim_info, skill, add=add)
        if sim_skill is None:
            return False
        sim_skill.add_value(value)
        return True

    @staticmethod
    def change_progress_toward_next_skill_level(sim_info: SimInfo, skill: Union[int, CommonSkillId, Skill], value: float, add: bool = True) -> bool:
        """change_progress_toward_next_skill_level(sim_info, skill, value, add=True)

        Modify the amount of progress a Sim has made toward the next level of a Skill.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param skill: The identifier of the Skill to modify.
        :type skill: Union[int, CommonSkillId, Skill]
        :param value: The level to add or subtract to/from the skill.
        :type value: Union[int, CommonSkillId, Skill]
        :param add: If True, the skill will be added to the Sim before it is modified.
        :type add: bool, optional
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        return CommonSimSkillUtils.change_progress_toward_max_skill_level(sim_info, skill, value, add=add)

    @staticmethod
    def get_progress_toward_next_skill_level(sim_info: SimInfo, skill: Union[int, CommonSkillId, Skill], add: bool = False) -> float:
        """get_progress_toward_next_skill_level(sim_info, skill, add=False)

        Retrieve the amount of progress a Sim has made toward the next level of a Skill.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param skill: The identifier of the Skill to use.
        :type skill: Union[int, CommonSkillId, Skill]
        :param add: If True, the skill will be added to the Sim before it is checked.
        :type add: bool, optional
        :return: The progress to the next level of the specified Skill or `-1.0` if a problem occurs.
        :rtype: float
        """
        skill = CommonSimSkillUtils.get_skill(sim_info, skill, add=add)
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
    def translate_skill_progress(sim_info: SimInfo, skill_from: Union[int, CommonSkillId, Skill], skill_to: Union[int, CommonSkillId, Skill], add: bool = True) -> bool:
        """translate_skill_progress(sim_info, skill_from, skill_to, add=True)

        Translate the total progress of one Skill to the total progress of another Skill for the specified Sim.

        :param sim_info: The Sim to modify.
        :type sim_info: SimInfo
        :param skill_from: The identifier of the Skill being changed.
        :type skill_from: Union[int, CommonSkillId, Skill]
        :param skill_to: The identifier of the Skill being translated to.
        :type skill_to: Union[int, CommonSkillId, Skill]
        :param add: If True, the skill will be added to the Sim before it is modified.
        :type add: bool, optional
        :return: True, if successful. False, if not.
        :rtype: bool
        """
        skill_level_value_from = CommonSimSkillUtils.get_progress_toward_next_skill_level(sim_info, skill_from)
        skill_to = CommonSimSkillUtils.get_skill(sim_info, skill_to, add=add)
        if skill_to is None:
            return False
        level = skill_to.get_user_value()
        value_for_level = skill_to.get_skill_value_for_level(level)
        value_for_next_level = skill_to.get_skill_value_for_level(level + 1) - value_for_level
        level_of_new_skill = value_for_level + value_for_next_level * skill_level_value_from
        return CommonSimSkillUtils.set_progress_toward_max_skill_level(sim_info, skill_to, level_of_new_skill)

    @staticmethod
    def get_skill(sim_info: SimInfo, skill: Union[int, CommonSkillId, Skill], add: bool = True) -> Union[Skill, None]:
        """get_skill(sim_info, skill, add=True)

        Retrieve a Skill for the specified Sim.

        :param sim_info: The Sim to check.
        :type sim_info: SimInfo
        :param skill: The identifier of the Skill to use.
        :type skill: Union[int, CommonSkillId, Skill]
        :param add: If True, the skill will be added to the Sim before it is checked.
        :type add: bool, optional
        :return: An instance of a Skill of the Sim or None if the Skill does not exist.
        :rtype: Union[Skill, None]
        """
        skill: Skill = CommonSkillUtils.load_skill_by_id(skill)
        if skill is None:
            return None
        return sim_info.get_statistic(skill, add=add)

    @staticmethod
    def get_all_skills_available_for_sim_gen(sim_info: SimInfo) -> Iterator[Skill]:
        """get_all_skills_available_for_sim_gen(sim_info)

        Retrieve all Skills available to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: An iterator of Skills that are available for the specified Sim.
        :rtype: Iterator[Skill]
        """
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return tuple()

        def _is_skill_available_for_sim(skill: Skill) -> bool:
            return skill.can_add(sim)

        yield from CommonSkillUtils.get_all_skills_gen(include_skill_callback=_is_skill_available_for_sim)


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.print_skill_level',
    'Print information about the skill level of a Sim for a Skill.',
    command_arguments=(
        CommonConsoleCommandArgument('skill', 'Skill Id or Tuning Name', 'The tuning name or decimal identifier of a skill.'),
        CommonConsoleCommandArgument('use_effective_skill_level', 'True or False', 'If True, the skill level of the Sim will take into account any modifiers that are applied to them. If False, the skill level will be determined without modifiers.', is_optional=True, default_value=True),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to check.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_get_skill_level(output: CommonConsoleCommandOutput, skill: TunableInstanceParam(Types.STATISTIC), use_effective_skill_level: bool = True, sim_info: SimInfo = None):
    if skill is None:
        output('ERROR: Failed, Skill not specified or Skill did not exist!')
        return
    if sim_info is None:
        return
    output(f'Attempting to print skill level for skill {skill} with use_effective_skill_level {use_effective_skill_level} for Sim {sim_info}')
    skill_value = CommonSimSkillUtils.get_current_skill_level(sim_info, skill, use_effective_skill_level=use_effective_skill_level)
    output(f'Skill Level: {skill_value}')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.set_skill_level',
    'Set the current skill level of a Skill for a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('skill', 'Skill Id or Tuning Name', 'The tuning name or decimal identifier of a skill.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to change.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_set_skill_level(output: CommonConsoleCommandOutput, skill: TunableInstanceParam(Types.STATISTIC), level: int, sim_info: SimInfo = None):
    if sim_info is None:
        return
    if skill is None:
        output('ERROR: Skill not specified or the specified Skill did not exist!')
        return
    if level < 0:
        output('ERROR: level must be a positive number or zero.')
        return
    output(f'Attempting to set the skill level for skill {skill} to level {level} for Sim {sim_info}')
    if CommonSimSkillUtils.set_current_skill_level(sim_info, skill, level):
        output(f'SUCCESS: Successfully set the skill level of skill {skill} for Sim {sim_info}.')
    else:
        output(f'FAILED: Failed to set the skill level of skill {skill} for Sim {sim_info}.')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.remove_skill',
    'Remove a skill from a Sim (effectively set it to zero)',
    command_arguments=(
        CommonConsoleCommandArgument('skill', 'Skill Id or Tuning Name', 'The tuning name or decimal identifier of a skill.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The name or instance id of the Sim to change.', is_optional=True, default_value='Active Sim'),
    )
)
def _common_remove_skill(output: CommonConsoleCommandOutput, skill: TunableInstanceParam(Types.STATISTIC), sim_info: SimInfo = None):
    if skill is None:
        output('ERROR: Skill not specified or the specified Skill did not exist!')
        return
    if sim_info is None:
        return
    output(f'Removing skill {skill} from Sim {sim_info}')
    if CommonSimSkillUtils.remove_skill(sim_info, skill):
        output(f'SUCCESS: Successfully removed skill {skill} from Sim {sim_info}.')
    else:
        output(f'FAILED: Failed to remove skill {skill} from Sim {sim_info}.')
