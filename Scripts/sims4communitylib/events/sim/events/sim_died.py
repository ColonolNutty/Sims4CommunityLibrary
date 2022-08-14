"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.enums.common_death_types import CommonDeathType
from sims4communitylib.events.event_handling.common_event import CommonEvent


class S4CLSimDiedEvent(CommonEvent):
    """S4CLSimDiedEvent(sim_info, death_type, died_off_lot)

    An event that occurs when a Sim has died.

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
            def handle_event(event_data: S4CLSimDiedEvent):
                pass

    :param sim_info: The Sim that died.
    :type sim_info: SimInfo
    :param death_type: The type of Death that befell the Sim.
    :type death_type: CommonDeathType
    :param died_off_lot: True, if the Sim died off the active lot. False, if not.
    :type died_off_lot: bool
    """

    def __init__(self, sim_info: SimInfo, death_type: CommonDeathType, died_off_lot: bool):
        self._sim_info = sim_info
        self._death_type = death_type
        self._died_off_lot = died_off_lot

    @property
    def sim_info(self) -> SimInfo:
        """The Sim that died.

        :return: The Sim that died.
        :rtype: SimInfo
        """
        return self._sim_info

    @property
    def death_type(self) -> CommonDeathType:
        """The type of Death that befell the Sim."""
        return self._death_type

    @property
    def died_off_lot(self) -> bool:
        """True, if the Sim died off the active lot. False, if not."""
        return self._died_off_lot
