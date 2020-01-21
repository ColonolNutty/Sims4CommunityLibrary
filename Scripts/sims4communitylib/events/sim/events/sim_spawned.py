"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.events.event_handling.common_event import CommonEvent


class S4CLSimSpawnedEvent(CommonEvent):
    """An Event that Occurs upon a Sim being spawned.

    """
    def __init__(self, sim_info: SimInfo):
        self._sim_info = sim_info

    @property
    def sim_info(self) -> SimInfo:
        """The SimInfo of a Sim.

        """
        return self._sim_info
