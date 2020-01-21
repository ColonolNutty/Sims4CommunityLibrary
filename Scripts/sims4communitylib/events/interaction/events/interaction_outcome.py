"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from interactions.base.interaction import Interaction
from interactions.utils.outcome import InteractionOutcome
from interactions.utils.outcome_enums import OutcomeResult
from sims4communitylib.events.event_handling.common_event import CommonEvent


class S4CLInteractionOutcomeEvent(CommonEvent):
    """An Event that Occurs upon a Sim running an interaction.

    """
    def __init__(self, interaction: Interaction, outcome: InteractionOutcome, outcome_result: OutcomeResult):
        self._interaction = interaction
        self._outcome = outcome
        self._outcome_result = outcome_result

    @property
    def interaction(self) -> Interaction:
        """An instance of an Interaction.

        """
        return self._interaction

    @property
    def outcome(self) -> InteractionOutcome:
        """The outcome of the interaction.

        """
        return self._outcome

    @property
    def outcome_result(self) -> OutcomeResult:
        """The result of an interaction.

        """
        return self._outcome_result

    def is_success(self) -> bool:
        """Determine if the outcome was a success.

        """
        return self.outcome_result == OutcomeResult.SUCCESS

    def is_failure(self) -> bool:
        """Determine if the outcome was a failure.

        """
        return self.outcome_result == OutcomeResult.FAILURE
