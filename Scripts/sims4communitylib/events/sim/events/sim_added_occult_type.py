"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.occult.occult_enums import OccultType
from sims.occult.occult_tracker import OccultTracker
from sims.sim_info import SimInfo
from sims4communitylib.events.event_handling.common_event import CommonEvent


class S4CLSimAddedOccultTypeEvent(CommonEvent):
    """ An event that occurs upon an Occult Type being added to a Sim. """
    def __init__(self, sim_info: SimInfo, occult_type: OccultType, occult_tracker: OccultTracker):
        self._sim_info = sim_info
        self._occult_type = occult_type
        self._occult_tracker = occult_tracker

    @property
    def sim_info(self) -> SimInfo:
        """ The SimInfo of a Sim. """
        return self._sim_info

    @property
    def occult_type(self) -> OccultType:
        """ The type of occult that has been added to the Sim. """
        return self._occult_type

    @property
    def occult_tracker(self) -> OccultTracker:
        """ The tracker that keeps track of the occult status of a Sim. """
        return self._occult_tracker
