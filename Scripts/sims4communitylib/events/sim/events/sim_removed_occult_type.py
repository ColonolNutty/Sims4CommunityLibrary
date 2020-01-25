"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.occult.occult_enums import OccultType
from sims.occult.occult_tracker import OccultTracker
from sims.sim_info import SimInfo
from sims4communitylib.events.event_handling.common_event import CommonEvent


class S4CLSimRemovedOccultTypeEvent(CommonEvent):
    """S4CLSimRemovedOccultTypeEvent(sim_info, occult_type, occult_tracker)

    An event that occurs when an OccultType has been removed from a Sim.

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
            @CommonEventRegistry.handle_events(ModInfo.get_identity().name)
            def handle_event(event_data: S4CLSimRemovedOccultTypeEvent):
                pass

    :param sim_info: The Sim the Occult Type was removed from.
    :type sim_info: SimInfo
    :param occult_type: The OccultType that was removed.
    :type occult_type: OccultType
    :param occult_tracker: A tracker that keeps track of the occult status of the Sim.
    :type occult_tracker: OccultTracker
    """

    def __init__(self, sim_info: SimInfo, occult_type: OccultType, occult_tracker: OccultTracker):
        self._sim_info = sim_info
        self._occult_type = occult_type
        self._occult_tracker = occult_tracker

    @property
    def sim_info(self) -> SimInfo:
        """The Sim the OccultType was removed from.

        :return: The Sim the OccultType was removed from.
        :rtype: SimInfo
        """
        return self._sim_info

    @property
    def occult_type(self) -> OccultType:
        """The OccultType that was removed.

        :return: The OccultType that was removed.
        :rtype: OccultType
        """
        return self._occult_type

    @property
    def occult_tracker(self) -> OccultTracker:
        """A tracker that keeps track of the occult status of the Sim.

        :return: A tracker that keeps track of the occult status of the Sim.
        :rtype: OccultTracker
        """
        return self._occult_tracker
