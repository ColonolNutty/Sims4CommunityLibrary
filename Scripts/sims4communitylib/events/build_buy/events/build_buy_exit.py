"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.events.event_handling.common_event import CommonEvent
from zone import Zone


class S4CLBuildBuyExitEvent(CommonEvent):
    """ An Event that Occurs upon exiting Build/Buy on a lot. """
    def __init__(self, zone: Zone):
        self._zone = zone

    @property
    def zone(self) -> Zone:
        """ The zone that was modified. """
        return self._zone
