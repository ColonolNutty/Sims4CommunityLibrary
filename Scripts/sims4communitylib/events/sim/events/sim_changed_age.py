"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.enums.common_age import CommonAge
from sims4communitylib.events.event_handling.common_event import CommonEvent


class S4CLSimChangedAgeEvent(CommonEvent):
    """S4CLSimChangedAgeEvent(sim_info, old_age, new_age)

    An event that occurs when a Sim has changed their current Age.

    .. note:: This can occur when a Child Sim becomes a Teen Sim, a Teen Sim becomes a Child Sim, etc.

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
            def handle_event(event_data: S4CLSimChangedAgeEvent):
                pass

    :param sim_info: The Sim that changed.
    :type sim_info: SimInfo
    :param old_age: The age the Sim has changed from.
    :type old_age: CommonAge
    :param new_age: The age the Sim has changed to.
    :type new_age: CommonAge
    """

    def __init__(self, sim_info: SimInfo, old_age: CommonAge, new_age: CommonAge):
        self._sim_info = sim_info
        self._old_age = old_age
        self._new_age = new_age

    @property
    def sim_info(self) -> SimInfo:
        """The Sim that changed."""
        return self._sim_info

    @property
    def old_age(self) -> CommonAge:
        """The age the Sim has changed from."""
        return self._old_age

    @property
    def new_age(self) -> CommonAge:
        """The age the Sim has changed to."""
        return self._new_age
