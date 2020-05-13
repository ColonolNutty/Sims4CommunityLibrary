"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Dict
from interactions.base.interaction import Interaction
from interactions.interaction_finisher import FinishingType
from sims4communitylib.events.event_handling.common_event import CommonEvent


class S4CLInteractionCancelledEvent(CommonEvent):
    """S4CLInteractionCancelledEvent(interaction, finishing_type, cancel_reason, ignore_must_run=False, **kwargs)

    An event that occurs upon an interaction being cancelled.

    .. note:: This event fires BEFORE the interaction is actually cancelled. Like a Pre-Cancel.

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
            def handle_event(event_data: S4CLInteractionCancelledEvent) -> bool:
                # Return True from here to signify the event listener ran successfully. Return False or None here to signify the event listener failed to run successfully.
                return True

    :param interaction: The interaction that is being cancelled.
    :type interaction: Interaction
    :param finishing_type: The finishing type of the interaction.
    :type finishing_type: FinishingType
    :param cancel_reason_msg: The reason the interaction was cancelled.
    :type cancel_reason_msg: str
    :param ignore_must_run: If True, interactions flagged as "Must Run" will be ignored. Default is False.
    :type ignore_must_run: bool, optional
    """

    def __init__(self, interaction: Interaction, finishing_type: FinishingType, cancel_reason: str, ignore_must_run: bool=False, **kwargs):
        self._interaction = interaction
        self._finishing_type = finishing_type
        self._cancel_reason = cancel_reason
        self._ignore_must_run = ignore_must_run
        self._kwargs = kwargs

    @property
    def interaction(self) -> Interaction:
        """The interaction that is being cancelled.

        :return: The interaction that is being cancelled.
        :rtype: Interaction
        """
        return self._interaction

    @property
    def finishing_type(self) -> FinishingType:
        """The finishing type of the interaction.

        :return: The finishing type of the interaction.
        :rtype: FinishingType
        """
        return self._finishing_type

    @property
    def cancel_reason(self) -> str:
        """The reason the interaction was cancelled.

        :return: The reason the interaction was cancelled.
        :rtype: str
        """
        return self._cancel_reason

    @property
    def ignore_must_run(self) -> bool:
        """Whether or not interactions flagged as "Must Run" will be cancelled.

        :return: If True, interactions flagged as "Must Run" will be cancelled. If False, interactions flagged as "Must Run" will not be cancelled.
        :rtype: bool
        """
        return self._ignore_must_run

    @property
    def keyword_arguments(self) -> Dict[str, Any]:
        """Keyword arguments sent to the cancelled interaction.

        :return: Keyword arguments sent to the cancelled interaction.
        :rtype: Dict[str, Any]
        """
        return self._kwargs
