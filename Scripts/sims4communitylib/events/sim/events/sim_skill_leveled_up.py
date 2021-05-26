"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.events.event_handling.common_event import CommonEvent
from sims4communitylib.utils.resources.common_skill_utils import CommonSkillUtils
from statistics.skill import Skill


class S4CLSimSkillLeveledUpEvent(CommonEvent):
    """S4CLSimSkillLeveledUpEvent(sim_info, skill, old_skill_level, new_skill_level)

    An event that occurs when a Sim levels up in a Skill.

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
        from sims4communitylib.modinfo import ModInfo

        class ExampleEventListener:

            # In order to listen to an event, your function must match these criteria:
            # - The function is static (staticmethod).
            # - The first and only required argument has the name "event_data".
            # - The first and only required argument has the Type Hint for the event you are listening for.
            # - The argument passed to "handle_events" is the name of your Mod.
            @staticmethod
            @CommonEventRegistry.handle_events(ModInfo.get_identity())
            def handle_event(event_data: S4CLSimSkillLeveledUpEvent):
                pass

    :param sim_info: The Sim that changed.
    :type sim_info: SimInfo
    :param skill: The Skill that was leveled up.
    :type skill: Skill
    :param old_skill_level: The level the Sim was at before leveling up.
    :type old_skill_level: int
    :param new_skill_level: The level the Sim will be after leveling up.
    :type new_skill_level: int
    """

    def __init__(self, sim_info: SimInfo, skill: Skill, old_skill_level: int, new_skill_level: int):
        self._sim_info = sim_info
        self._skill = skill
        self._old_skill_level = old_skill_level
        self._new_skill_level = new_skill_level

    @property
    def new_skill_level(self) -> int:
        """The level the Sim will be after leveling up."""
        return self._new_skill_level

    @property
    def old_skill_level(self) -> int:
        """The level the Sim was at before leveling up."""
        return self._old_skill_level

    @property
    def sim_info(self) -> SimInfo:
        """The Sim that leveled up in a Skill."""
        return self._sim_info

    @property
    def skill(self) -> Skill:
        """The Skill that was leveled up."""
        return self._skill

    @property
    def skill_id(self) -> int:
        """The decimal identifier of the Skill."""
        return CommonSkillUtils.get_skill_id(self.skill)
