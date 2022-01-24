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
        reason,\
        tooltip_text=None,\
        tooltip_tokens=(),\
        icon=None,\
        influenced_by_active_mood=False,\
    )

    The result of executing something.

    .. note:: This class can be used in place of TestResult

    :param result: A value that indicates whether the execution was successful or not. If True, the execution was successful. If False, the execution was not successful.
    :type result: bool
    :param tooltip_text: The text that will be displayed. If not specified, then no tooltip will be displayed. Default is None.
    :type tooltip_text: Union[int, str, LocalizedString, CommonStringId, CommonLocalizedStringSeparator], optional
    :param tooltip_tokens: A collection of objects to format into the localized string. (They can be anything. LocalizedString, str, int, SimInfo, just to name a few)
    :type tooltip_tokens: Iterable[Any], optional
    :param icon: The icon to display. Default is None.
    :type icon: Any, optional
    :param influenced_by_active_mood: Indicate whether or not the result was influenced by a Sims active mood. Default is False.
    :type influenced_by_active_mood: bool, optional
    """
    TRUE = None
    FALSE = None
    NONE = None

    def __init__(self, result: bool, reason: str, tooltip_text: Union[int, str, LocalizedString, CommonStringId, CommonLocalizedStringSeparator, CommonLocalizationUtils.LocalizedTooltip]=None, tooltip_tokens: Iterator[Any]=(), icon: Any=None, influenced_by_active_mood: bool=False) -> None:
        tooltip = CommonLocalizationUtils.create_localized_tooltip(tooltip_text, tooltip_tokens=tooltip_tokens)
        super().__init__(result, reason, tooltip=tooltip, icon=icon, influence_by_active_mood=influenced_by_active_mood)

    @property
    def is_success(self) -> bool:
        """Whether or not the result is successful."""
        return bool(self.result)

    def __repr__(self) -> str:
        if self.reason:
            return f'<{self.__class__.__name__}: {bool(self.result)} ({self.reason})>'
        return f'<{self.__class__.__name__}: {bool(self.result)}>'


CommonExecutionResult.TRUE = CommonExecutionResult(True, 'Success')
CommonExecutionResult.FALSE = CommonExecutionResult(False, 'Failed')
CommonExecutionResult.NONE = CommonExecutionResult(False, 'Failed')
