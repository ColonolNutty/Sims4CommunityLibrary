"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from interactions.base.interaction import Interaction
from interactions.interaction_queue import InteractionQueue
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims4communitylib.events.event_handling.common_event import CommonEvent
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class S4CLInteractionQueuedEvent(CommonEvent):
    """S4CLInteractionQueuedEvent(interaction, interaction_queue)

    An event that occurs upon a Sim adding an interaction to their interaction queue.

    .. note:: This event fires BEFORE the interaction is actually queued. Like a Pre-Queue. If False or None is returned from any of the listeners of this event, the interaction will be prevented from queuing; All subsequent listeners will still receive the event, but their return will be ignored.

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
            # - The argument passed to "handle_events" is the name or identity of your Mod.
            @staticmethod
            @CommonEventRegistry.handle_events(ModInfo.get_identity())
            def handle_event(event_data: S4CLInteractionQueuedEvent) -> bool:
                # Return True here to allow the interaction to queue and to signify the event listener ran successfully. Return False or None here to prevent the interaction from being queued or to signify the event listener failed to run.
                return True

    :param interaction: The interaction that is being queued.
    :type interaction: Interaction
    :param interaction_queue: The interaction queue of the Sim.
    :type interaction_queue: InteractionQueue
    """

    def __init__(self, interaction: Interaction, interaction_queue: InteractionQueue):
        self._interaction = interaction
        self._interaction_queue = interaction_queue

    @property
    def queuing_sim(self) -> Union[Sim, None]:
        """The Sim that is putting the interaction into their queue."""
        if self._interaction is None:
            return None
        return self._interaction.context.sim

    @property
    def queuing_sim_info(self) -> Union[SimInfo, None]:
        """The SimInfo of the Sim that is putting the interaction into their queue."""
        return CommonSimUtils.get_sim_info(self.queuing_sim)

    @property
    def interaction(self) -> Interaction:
        """The interaction that is being queued.

        :return: The interaction that was queued.
        :rtype: Interaction
        """
        return self._interaction

    @property
    def interaction_queue(self) -> InteractionQueue:
        """The interaction queue of the Sim that is queuing the interaction.

        :return: The interaction queue of the Sim that is queuing the interaction.
        :rtype: InteractionQueue
        """
        return self._interaction_queue
