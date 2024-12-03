"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Union, Iterator

from event_testing.results import TestResult
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_separators import CommonLocalizedStringSeparator


class CommonExecutionResult(TestResult):
    """CommonExecutionResult(\
        result,\
        reason=None,\
        success_override=None,\
        tooltip_text=None,\
        tooltip_tokens=(),\
        icon=None,\
        influenced_by_active_mood=False,\
        hide_tooltip=False,\
    )

    The result of executing something.

    .. note:: This class can be used in place of TestResult

    :param result: The result of execution. This value can be any type.
    :type result: Any
    :param reason: The reason for the success or failure of the execution result. Default is None.
    :type reason: Union[str, None], optional
    :param success_override: If True, the execution will be indicated as being a success. If False, the execution will be indicated as being a failure. If None, the execution success will be indicated by whether result is set or not, if result is a bool, success is True and failure is False. Default is None.
    :type success_override: bool
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
        result: Any,
        reason: Union[str, None] = None,
        success_override: bool = None,
        tooltip_text: Union[int, str, LocalizedString, CommonStringId, CommonLocalizedStringSeparator, CommonLocalizationUtils.LocalizedTooltip] = None,
        tooltip_tokens: Iterator[Any] = (),
        icon: Any = None,
        influenced_by_active_mood: bool = False,
        hide_tooltip: bool = False
    ) -> None:
        self._tooltip_text = None
        self._tooltip_tokens = None
        self._hide_tooltip = hide_tooltip
        tooltip = None
        if not hide_tooltip:
            self._tooltip_text = tooltip_text
            self._tooltip_tokens = tooltip_tokens
            if tooltip_text is not None:
                tooltip = CommonLocalizationUtils.create_localized_tooltip(tooltip_text, tooltip_tokens=tooltip_tokens)
            elif reason is not None:
                tooltip = CommonLocalizationUtils.create_localized_tooltip(reason, tooltip_tokens=tooltip_tokens)
        super().__init__(result, reason, tooltip=tooltip, icon=icon, influence_by_active_mood=influenced_by_active_mood)
        self._success_override = success_override
        if success_override is None:
            if result:
                success_override = True
            else:
                success_override = False
        self._success = success_override

    @property
    def tooltip_text(self) -> Union[int, str, LocalizedString, CommonStringId, CommonLocalizedStringSeparator, CommonLocalizationUtils.LocalizedTooltip]:
        """The text of the tooltip."""
        return self._tooltip_text

    @property
    def tooltip_tokens(self) -> Iterator[Any]:
        """The tokens of the tooltip."""
        return self._tooltip_tokens

    def reverse_result(self) -> 'CommonExecutionResult':
        """reverse_result()

        Create a CommonExecutionResult that has a reversed result of this one, but with the same reason and tooltip information.

        .. note:: This function works best when the result value has an opposite, such as a boolean.

        :return: This CommonExecutionResult, but with a reversed result value.
        :rtype: CommonExecutionResult
        """
        return CommonExecutionResult(not self.result, reason=self.reason, success_override=self._success, tooltip_text=self._tooltip_text, tooltip_tokens=self._tooltip_tokens, icon=self.icon, influenced_by_active_mood=self.influence_by_active_mood, hide_tooltip=self._hide_tooltip)

    @property
    def is_success(self) -> bool:
        """True, if the result of execution is successful. False, if not."""
        return self._success

    @property
    def is_failure(self) -> bool:
        """False, if the result of execution is a failure. False, if not."""
        return not self.is_success

    def __repr__(self) -> str:
        if self.reason:
            return f'<{self.__class__.__name__}: {bool(self.result)} ({self.reason})>'
        return f'<{self.__class__.__name__}: {bool(self.result)}>'

    def __str__(self) -> str:
        if self.reason:
            return self.reason
        return str(self.result)

    def __eq__(self, other) -> bool:
        if isinstance(other, bool):
            return self.is_success is other
        if isinstance(other, CommonExecutionResult):
            return self.result == other.result and self.is_success == other.is_success
        if isinstance(other, TestResult):
            return self.is_success == other.result
        return self.result == other

    def __ne__(self, other) -> bool:
        return not self == other

    def __bool__(self) -> bool:
        return self._success

    def __or__(self, other) -> 'CommonExecutionResult':
        if isinstance(other, CommonExecutionResult):
            is_success = self.is_success or other.is_success
            result = self.result or other.result
            tooltip_text = self._tooltip_text or other._tooltip_text
            tooltip_tokens = self._tooltip_tokens or other._tooltip_tokens
        elif isinstance(other, TestResult):
            is_success = self.is_success or other.result
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
        return CommonExecutionResult(result, reason=reason, success_override=is_success, tooltip_text=tooltip_text, tooltip_tokens=tooltip_tokens, icon=icon, influenced_by_active_mood=influence_by_active_mood)

    def __and__(self, other: 'CommonExecutionResult') -> 'CommonExecutionResult':
        if isinstance(other, CommonExecutionResult):
            is_success = self.is_success and other.is_success
            result = self.result or other.result
            tooltip_text = self._tooltip_text or other._tooltip_text
            tooltip_tokens = self._tooltip_tokens or other._tooltip_tokens
        elif isinstance(other, TestResult):
            is_success = self.is_success and other.result
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
        return CommonExecutionResult(result, reason=reason, success_override=is_success, tooltip_text=tooltip_text, tooltip_tokens=tooltip_tokens, icon=icon, influenced_by_active_mood=influence_by_active_mood)


CommonExecutionResult.TRUE = CommonExecutionResult(True, hide_tooltip=True)
CommonExecutionResult.FALSE = CommonExecutionResult(False, reason='Failure Unknown', hide_tooltip=True)
CommonExecutionResult.NONE = CommonExecutionResult(False, hide_tooltip=True)
