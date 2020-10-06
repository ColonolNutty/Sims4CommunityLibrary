"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from interactions.base.interaction import Interaction
from interactions.interaction_queue import InteractionQueue
from sims4communitylib.events.event_handling.common_event import CommonEvent


class S4CLInteractionRunEvent(CommonEvent):
    """S4CLInteractionRunEvent(interaction, interaction_queue, run_result)

    An event that occurs after a Sim has run an interaction.

    .. note:: This event fires AFTER the interaction is actually run. Like a Post-Run. If False or None is returned from any of the listeners of this event, the interaction will be prevented from running; All subsequent listeners will still receive the event, but their return will be ignored.

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
            def handle_event(event_data: S4CLInteractionRunEvent) -> bool:
                # Return True here to signify the event listener ran successfully. Return False or None here to signify the event listener failed to run.
                return True

    :param interaction: The interaction that was run.
    :type interaction: Interaction
    :param interaction_queue: The interaction queue of the Sim.
    :type interaction_queue: InteractionQueue
    :param run_result: The result of the interaction being run.
    :type run_result: bool
    """

    def __init__(self, interaction: Interaction, interaction_queue: InteractionQueue, run_result: bool):
        self._interaction = interaction
        self._interaction_queue = interaction_queue
        self._run_result = run_result

    @property
    def interaction(self) -> Interaction:
        """The interaction that was run.

        :return: The interaction that was run.
        :rtype: Interaction
        """
        return self._interaction

    @property
    def interaction_queue(self) -> InteractionQueue:
        """The interaction queue of the Sim that ran the interaction.

        :return: The interaction queue of the Sim ran the interaction.
        :rtype: InteractionQueue
        """
        return self._interaction_queue

    @property
    def run_result(self) -> bool:
        """The result of the interaction being run.

        :return: True, if the interaction was run successfully. False, if not.
        :rtype: bool
        """
        return self._run_result
