"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Iterator, Tuple, List, Callable
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
    def get_all_skills_gen(include_skill_callback: Callable[[Skill], bool] = None) -> Iterator[Skill]:
        """get_all_skills_gen(include_skill_callback=None)

        Retrieve all Skills.

        :param include_skill_callback: If the result of this callback is True, the Skill will be included in the results. If set to None, All Skills will be included.
        :type include_skill_callback: Callable[[Skill], bool], optional
        :return: An iterator of Skills that pass the specified include_skill_callback.
        :rtype: Iterator[Skill]
        """
        from sims4communitylib.utils.resources.common_statistic_utils import CommonStatisticUtils
        statistic_manager = CommonStatisticUtils.get_statistic_instance_manager()
        for skill in statistic_manager.get_ordered_types(only_subclasses_of=Skill):
            skill: Skill = skill
            skill_id = CommonSkillUtils.get_skill_id(skill)
            if skill_id is None:
                continue
            if include_skill_callback is not None and not include_skill_callback(skill):
                continue
            yield skill

    @staticmethod
    def load_skill_by_id(skill_id: Union[int, CommonSkillId, Skill]) -> Union[Skill, None]:
        """load_skill_by_id(skill_id)

        Load an instance of a Skill by its decimal identifier.

        :param skill_id: The decimal identifier of a Skill.
        :type skill_id: Union[int, CommonSkillId, Skill]
        :return: An instance of a Skill matching the decimal identifier or None if not found.
        :rtype: Union[Skill, None]
        """
        if isinstance(skill_id, Skill) or hasattr(skill_id, 'is_skill'):
            return skill_id
        # noinspection PyBroadException
        try:
            skill_id: int = int(skill_id)
        except:
            # noinspection PyTypeChecker
            skill_id: Skill = skill_id
            return skill_id

        from sims4communitylib.utils.resources.common_statistic_utils import CommonStatisticUtils
        return CommonStatisticUtils.load_statistic_by_id(skill_id)
