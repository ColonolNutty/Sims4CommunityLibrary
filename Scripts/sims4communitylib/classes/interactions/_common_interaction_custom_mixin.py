"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Any, Iterator, Tuple, List, Set

from interactions.base.interaction import Interaction
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils


class _CommonInteractionCustomMixin:
    """Custom functionality for interactions."""

    @classmethod
    def create_test_result(
        cls,
        result: bool,
        reason: str=None,
        text_tokens: Union[Tuple[Any], List[Any], Set[Any]]=(),
        tooltip: Union[int, str, CommonLocalizationUtils.LocalizedTooltip]=None,
        tooltip_tokens: Iterator[Any]=(),
        icon=None,
        influence_by_active_mood: bool=False
    ) -> CommonTestResult:
        """create_test_result(\
            result,\
            reason=None,\
            text_tokens=(),\
            tooltip=None,\
            tooltip_tokens=(),\
            icon=None,\
            influence_by_active_mood=False\
        )

        Create a CommonTestResult with the specified information.

        .. note:: CommonTestResult is an object used to disable, hide, or display tooltips on interactions. See :func:`~on_test` for more information.

        :param result: The result of a test. True for passed, False for failed.
        :type result: bool
        :param reason: The reason for the Test Result (This is displayed as a tooltip to the player when the interaction is disabled).
        :type reason: str, optional
        :param text_tokens: Any text tokens to include format into the reason.
        :type text_tokens: Union[Tuple[Any], List[Any], Set[Any]], optional
        :param tooltip: The tooltip displayed when hovering the interaction while it is disabled.
        :type tooltip: Union[int, str, LocalizedTooltip], optional
        :param tooltip_tokens: A collection of objects to format into the localized tooltip. (They can be anything. LocalizedString, str, int, SimInfo, just to name a few) Default is an empty collection.
        :type tooltip_tokens: Iterator[Any], optional
        :param icon: The icon of the outcome.
        :type icon: CommonResourceKey, optional
        :param influence_by_active_mood: If true, the Test Result will be influenced by the active mood.
        :type influence_by_active_mood: bool, optional
        :return: The desired outcome for a call of :func:`~on_test`.
        :rtype: CommonTestResult
        """
        return CommonTestResult(
            result,
            reason=reason.format(*text_tokens) if reason is not None else reason,
            tooltip_text=tooltip,
            tooltip_tokens=tooltip_tokens,
            icon=icon,
            influenced_by_active_mood=influence_by_active_mood
        )

    def set_current_progress_bar(self: Interaction, percent: float, rate_change: float, start_message: bool=True):
        """set_current_progress_bar(initial_value, progress_rate)

        Set the current progress rate of the interaction.

        :param percent: A percentage indicating the starting progress.
        :type percent: float
        :param rate_change: A value that indicates how fast progress will be made.
        :type rate_change: float
        :param start_message: If True, progress will begin changing immediately. If False, it will not. Default is True.
        :type start_message: bool, optional
        """
        self._send_progress_bar_update_msg(percent, rate_change, start_msg=start_message)
