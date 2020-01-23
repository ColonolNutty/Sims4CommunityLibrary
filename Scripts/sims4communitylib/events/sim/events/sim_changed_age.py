"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims.sim_info_types import Age
from sims4communitylib.events.event_handling.common_event import CommonEvent


class S4CLSimChangedAgeEvent(CommonEvent):
    """An event that occurs upon a Sim changing to a different age.

    """
    def __init__(self, sim_info: SimInfo, old_age: Age, new_age: Age):
        self._sim_info = sim_info
        self._old_age = old_age
        self._new_age = new_age

    @property
    def sim_info(self) -> SimInfo:
        """The SimInfo of a Sim.

        """
        return self._sim_info

    @property
    def old_age(self) -> Age:
        """The Age the Sim used to be.

        """
        return self._old_age

    @property
    def new_age(self) -> Age:
        """The Age the Sim is now.

        """
        return self._new_age
