"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.events.event_handling.common_event import CommonEvent
from zone import Zone


class S4CLBuildBuyExitEvent(CommonEvent):
    """S4CLBuildBuyEnterEvent(zone)

    An event that occurs upon exiting Build/Buy on a lot.

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
            def handle_event(event_data: S4CLBuildBuyExitEvent):
                pass

    :param zone: The zone the player has exited Build/Buy on.
    :type zone: Zone
    """

    def __init__(self, zone: Zone):
        self._zone = zone

    @property
    def zone(self) -> Zone:
        """The zone the event occurred on.

        :return: The zone the event occurred on.
        :rtype: Zone
        """
        return self._zone
