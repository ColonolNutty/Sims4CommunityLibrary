"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Union, Iterator

from event_testing.results import TestResult
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_separators import CommonLocalizedStringSeparator


class CommonTestResult(CommonExecutionResult):
    """CommonTestResult(\
        result,\
        reason=None,\
        tooltip_text=None,\
        tooltip_tokens=(),\
        icon=None,\
        influenced_by_active_mood=False,\
        hide_tooltip=False,\
    )

    The result of testing something.

    .. note:: This class can be used in place of TestResult and CommonExecutionResult

    :param result: A value that indicates whether the test was successful or not. If True, the test was successful. If False, the test was not successful.
    :type result: bool
    :param reason: The reason for the success or failure of the test result. Default is None.
    :type reason: Union[str, None], optional
    :param tooltip_text: The text that will be displayed. If not specified, then no tooltip will be displayed. Default is None.
    :type tooltip_text: Union[int, str, LocalizedString, CommonStringId, CommonLocalizedStringSeparator], optional
    :param tooltip_tokens: A collection of objects to format into the localized tooltip. (They can be anything. LocalizedString, str, int, SimInfo, just to name a few). Default is an empty collection.
    :type tooltip_tokens: Iterator[Any], optional
    :param icon: The icon to display. Default is None.
    :type icon: Any, optional
    :param influenced_by_active_mood: Indicate whether or not the result was influenced by a Sims active mood. Default is False.
    :type influenced_by_active_mood: bool, optional
    :param hide_tooltip: If True, no tooltip will be shown to the Player, even if a tooltip is specified. If False, a tooltip will be shown to the Player and if not specified, will be created from the reason  (Assuming a reason is specified). Default is False.
    :type hide_tooltip: bool, optional
    """
    TRUE = None
    FALSE = None
    NONE = None

    def __init__(
        self,
        result: bool,
        reason: Union[str, None] = None,
        tooltip_text: Union[int, str, LocalizedString, CommonStringId, CommonLocalizedStringSeparator, CommonLocalizationUtils.LocalizedTooltip] = None,
        tooltip_tokens: Iterator[Any] = (),
        icon: Any = None,
        influenced_by_active_mood: bool = False,
        hide_tooltip: bool = False
    ) -> None:
        super().__init__(result, reason=reason, success_override=result, tooltip_text=tooltip_text, tooltip_tokens=tooltip_tokens, icon=icon, influenced_by_active_mood=influenced_by_active_mood, hide_tooltip=hide_tooltip)

    @classmethod
    def convert_from_vanilla(cls, test_result: TestResult) -> 'CommonTestResult':
        """convert_from_vanilla(test_result)

        Convert a vanilla TestResult into a CommonTestResult.

        :param test_result: An instance of TestResult
        :type test_result: TestResult
        :return: The specified TestResult translated to CommonTestResult.
        :rtype: CommonTestResult
        """
        return CommonTestResult(test_result.result, reason=test_result.reason, tooltip_text=test_result.tooltip, icon=test_result.icon, influenced_by_active_mood=test_result.influence_by_active_mood)

    def reverse_result(self) -> 'CommonTestResult':
        """reverse_result()

        Create a CommonTestResult that has a reversed result of this one, but with the same reason and tooltip information.

        .. note:: This function works best when the result value has an opposite, such as a boolean.

        :return: This CommonTestResult, but with a reversed result value.
        :rtype: CommonTestResult
        """
        return self.__class__(not self.result, self.reason, tooltip_text=self._tooltip_text, tooltip_tokens=self._tooltip_tokens)

    def __eq__(self, other) -> bool:
        if isinstance(other, bool):
            return self.is_success is other
        if isinstance(other, CommonTestResult):
            return self.result == other.result and self.is_success == other.is_success
        if isinstance(other, TestResult):
            return self.is_success == other.result
        return self.result == other

    def __or__(self, other) -> 'CommonTestResult':
        if isinstance(other, CommonTestResult):
            result = self.result or other.result
            tooltip_text = self._tooltip_text or other._tooltip_text
            tooltip_tokens = self._tooltip_tokens or other._tooltip_tokens
        elif isinstance(other, TestResult):
            result = self.result or other.result
            if self._tooltip_text:
                tooltip_text = self._tooltip_text
                tooltip_tokens = self._tooltip_tokens
            else:
                tooltip_text = other.tooltip
                tooltip_tokens = tuple()
        else:
            return self

        if self._reason:
            reason = self._reason
        else:
            reason = other._reason
        icon = self.icon or other.icon
        influence_by_active_mood = self.influence_by_active_mood or other.influence_by_active_mood
        return self.__class__(result, reason, tooltip_text=tooltip_text, tooltip_tokens=tooltip_tokens, icon=icon, influenced_by_active_mood=influence_by_active_mood)

    def __and__(self, other: 'CommonTestResult') -> 'CommonTestResult':
        if isinstance(other, CommonTestResult):
            result = self.result and other.result
            tooltip_text = self._tooltip_text or other._tooltip_text
            tooltip_tokens = self._tooltip_tokens or other._tooltip_tokens
        elif isinstance(other, TestResult):
            result = self.result and other.result
            if self._tooltip_text:
                tooltip_text = self._tooltip_text
                tooltip_tokens = self._tooltip_tokens
            else:
                tooltip_text = other.tooltip
                tooltip_tokens = tuple()
        else:
            return self

        if self._reason:
            reason = self._reason
        else:
            reason = other._reason
        icon = self.icon or other.icon
        influence_by_active_mood = self.influence_by_active_mood or other.influence_by_active_mood
        return self.__class__(result, reason, tooltip_text=tooltip_text, tooltip_tokens=tooltip_tokens, icon=icon, influenced_by_active_mood=influence_by_active_mood)


CommonTestResult.TRUE = CommonTestResult(True, hide_tooltip=True)
CommonTestResult.FALSE = CommonTestResult(False, reason='Failure Unknown', hide_tooltip=True)
CommonTestResult.NONE = CommonTestResult(False, hide_tooltip=True)
