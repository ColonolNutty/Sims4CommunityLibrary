"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Iterator, Tuple, List
from sims4communitylib.enums.skills_enum import CommonSkillId
from statistics.skill import Skill


class CommonSkillUtils:
    """Utilities for manipulating Skills.

    """

    @staticmethod
    def get_skill_id(skill_identifier: Union[int, Skill]) -> Union[int, None]:
        """get_skill_id(skill_identifier)

        Retrieve the decimal identifier of a Skill.

        :param skill_identifier: The identifier or instance of a Skill.
        :type skill_identifier: Union[int, Skill]
        :return: The decimal identifier of the Skill or None if the Skill does not have an id.
        :rtype: Union[int, None]
        """
        if isinstance(skill_identifier, int):
            return skill_identifier
        return getattr(skill_identifier, 'guid64', None)

    @staticmethod
    def get_short_name(skill: Skill) -> Union[str, None]:
        """get_short_name(skill)

        Retrieve the Short Name of a Skill.

        :param skill: An instance of a Skill.
        :type skill: Skill
        :return: The short name of a Skill or None if a problem occurs.
        :rtype: Union[str, None]
        """
        if skill is None:
            return None
        # noinspection PyBroadException
        try:
            return skill.__class__.__name__
        except:
            return ''

    @staticmethod
    def get_short_names(skills: Iterator[Skill]) -> Tuple[str]:
        """get_short_names(skills)

        Retrieve the Short Names of a collection of Skills.

        :param skills: A collection of Skill instances.
        :type skills: Iterator[Skill]
        :return: A collection of short names of all Skill instances.
        :rtype: Tuple[str]
        """
        if skills is None or not skills:
            return tuple()
        short_names: List[str] = []
        for skill in skills:
            # noinspection PyBroadException
            try:
                short_name = CommonSkillUtils.get_short_name(skill)
                if not short_name:
                    continue
            except:
                continue
            short_names.append(short_name)
        return tuple(short_names)

    @staticmethod
    def load_skill_by_id(skill_id: Union[int, CommonSkillId, Skill]) -> Union[Skill, None]:
        """load_skill_by_id(skill_id)

        Load an instance of a Skill by its decimal identifier.

        :param skill_id: The decimal identifier of a Skill.
        :type skill_id: Union[int, CommonSkillId, Skill]
        :return: An instance of a Skill matching the decimal identifier or None if not found.
        :rtype: Union[Skill, None]
        """
        if hasattr(skill_id, 'is_skill'):
            return skill_id
        from sims4communitylib.utils.resources.common_statistic_utils import CommonStatisticUtils
        return CommonStatisticUtils.load_statistic_by_id(skill_id)
