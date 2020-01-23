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
    """An Event that Occurs upon a Sim running an interaction.

    """
    def __init__(self, interaction: Interaction, interaction_queue: InteractionQueue):
        self._interaction = interaction
        self._interaction_queue = interaction_queue

    @property
    def interaction(self) -> Interaction:
        """An instance of an Interaction.

        """
        return self._interaction

    @property
    def interaction_queue(self) -> InteractionQueue:
        """The Interaction Queue of the Sim running the interaction.

        """
        return self._interaction_queue
