"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from interactions.base.interaction import Interaction
from interactions.interaction_queue import InteractionQueue
from sims4communitylib.events.event_handling.common_event import CommonEvent

ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'

# If on Read The Docs, create fake versions of extended objects to fix the error of inheriting from multiple MockObjects.
if ON_RTD:
    # noinspection PyMissingOrEmptyDocstring
    class Timeline:
        pass

if not ON_RTD:
    from scheduling import Timeline


class S4CLInteractionPreRunEvent(CommonEvent):
    """S4CLInteractionPreRunEvent(interaction, interaction_queue, timeline)

    An event that occurs upon a Sim running an interaction.

    .. note:: This event fires BEFORE the interaction is actually run. Like a Pre-Run. If False or None is returned from any of the listeners of this event, the interaction will be prevented from running; All subsequent listeners will still receive the event, but their return will be ignored.

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
            def handle_event(event_data: S4CLInteractionPreRunEvent) -> bool:
                # Return True here to allow the interaction to run and to signify the event listener ran successfully. Return False or None here to prevent the interaction from being run or to signify the event listener failed to run.
                return True

    :param interaction: The interaction that is being run.
    :type interaction: Interaction
    :param interaction_queue: The interaction queue of the Sim.
    :type interaction_queue: InteractionQueue
    :param timeline: The timeline of the interaction.
    :type timeline: Timeline
    """

    def __init__(self, interaction: Interaction, interaction_queue: InteractionQueue, timeline: Timeline):
        self._interaction = interaction
        self._interaction_queue = interaction_queue
        self._timeline = timeline

    @property
    def interaction(self) -> Interaction:
        """The interaction that is being run.

        :return: The interaction that is being run.
        :rtype: Interaction
        """
        return self._interaction

    @property
    def interaction_queue(self) -> InteractionQueue:
        """The interaction queue of the Sim that is running the interaction.

        :return: The interaction queue of the Sim that is running the interaction.
        :rtype: InteractionQueue
        """
        return self._interaction_queue

    @property
    def timeline(self) -> Timeline:
        """The timeline of the interaction.

        :return: The timeline of the interaction.
        :rtype: Timeline
        """
        return self._timeline
