"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from interactions.base.interaction import Interaction
from interactions.utils.outcome import InteractionOutcome
from interactions.utils.outcome_enums import OutcomeResult
from sims4communitylib.events.event_handling.common_event import CommonEvent


class S4CLInteractionOutcomeEvent(CommonEvent):
    """S4CLInteractionOutcomeEvent(interaction, outcome, outcome_result)

    An event that occurs after a Sim has performed an interaction.

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
            def handle_event(event_data: S4CLInteractionOutcomeEvent) -> bool:
                # Return True from here to signify the event listener ran successfully. Return False or None here to signify the event listener failed to run.
                return True

    :param interaction: The interaction that was performed.
    :type interaction: Interaction
    :param outcome: The outcome of the interaction that was performed.
    :type outcome: InteractionOutcome
    :param outcome_result: The result of the interaction that was performed.
    :type outcome_result: OutcomeResult
    """

    def __init__(self, interaction: Interaction, outcome: InteractionOutcome, outcome_result: OutcomeResult):
        self._interaction = interaction
        self._outcome = outcome
        self._outcome_result = outcome_result

    @property
    def interaction(self) -> Interaction:
        """The interaction that was performed.

        :return: The interaction that was performed.
        :rtype: Interaction
        """
        return self._interaction

    @property
    def outcome(self) -> InteractionOutcome:
        """The outcome of the interaction that was performed.

        :return: The outcome of the interaction that was performed.
        :rtype: InteractionOutcome
        """
        return self._outcome

    @property
    def outcome_result(self) -> OutcomeResult:
        """The result of the interaction that was performed.

        :return: The result of the interaction that was performed.
        :rtype: OutcomeResult
        """
        return self._outcome_result

    def is_success(self) -> bool:
        """Determine if the outcome was a success.

        :return: True, if the interaction was performed successfully. False, if the interaction was not performed successfully.
        :rtype: bool
        """
        return self.outcome_result == OutcomeResult.SUCCESS

    def is_failure(self) -> bool:
        """Determine if the outcome was a failure.

        :return: True, if the interaction was not performed successfully. False, if the interaction was performed successfully.
        :rtype: bool
        """
        return self.outcome_result == OutcomeResult.FAILURE
