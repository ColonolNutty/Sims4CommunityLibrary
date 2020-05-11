"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from interactions.base.interaction import Interaction
from interactions.interaction_queue import InteractionQueue
from sims4communitylib.events.event_handling.common_event import CommonEvent


class S4CLInteractionQueuedEvent(CommonEvent):
    """S4CLInteractionQueuedEvent(interaction, interaction_queue)

    An event that occurs upon a Sim adding an interaction to their interaction queue.

    .. note:: This event fires BEFORE the interaction is actually queued. Like a Pre-Queue. If False or None is returned from any of the listeners of this event, the interaction will be prevented from queuing.

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
            def handle_event(event_data: S4CLInteractionQueuedEvent):
                # Return True here to allow the interaction to queue. Return False or None here to prevent the interaction from being queued.
                return True

    :param interaction: The interaction that was queued.
    :type interaction: Interaction
    :param interaction_queue: The interaction queue of the Sim.
    :type interaction_queue: InteractionQueue
    """

    def __init__(self, interaction: Interaction, interaction_queue: InteractionQueue):
        self._interaction = interaction
        self._interaction_queue = interaction_queue

    @property
    def interaction(self) -> Interaction:
        """The interaction that was queued.

        :return: The interaction that was queued.
        :rtype: Interaction
        """
        return self._interaction

    @property
    def interaction_queue(self) -> InteractionQueue:
        """The interaction queue of the Sim that queued the interaction.

        :return: The interaction queue of the Sim that queued the interaction.
        :rtype: InteractionQueue
        """
        return self._interaction_queue
