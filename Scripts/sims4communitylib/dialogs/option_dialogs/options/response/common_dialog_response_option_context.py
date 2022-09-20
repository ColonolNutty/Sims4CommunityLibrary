"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Any, TypeVar, Iterator
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils

DialogResponseOptionValueType = TypeVar('DialogResponseOptionValueType')


class CommonDialogResponseOptionContext:
    """CommonDialogResponseOptionContext(\
        text_identifier,\
        text_tokens=(),\
        subtext_identifier=None,\
        subtext_tokens=(),\
        disabled_text_identifier=None,\
        disabled_text_tokens=(),\
    )

    A context used by :class:`.CommonDialogResponseOption` that provides customization of options.

    :param text_identifier: The text of the option.
    :type text_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param text_tokens: An iterator of Tokens that will be formatted into the text.
    :type text_tokens: Iterator[Any], optional
    :param subtext_identifier: The subtext of the option. Default is None.
    :type subtext_identifier: Union[int, str, LocalizedString, CommonStringId], optional
    :param subtext_tokens: An iterator of Tokens that will be formatted into the description.
    :type subtext_tokens: Iterator[Any], optional
    :param disabled_text_identifier: The text that displays on the option as a tooltip. Setting this value will also disable the option. Default is None.
    :type disabled_text_identifier: Union[int, str, LocalizedString, CommonStringId], optional
    :param disabled_text_tokens: An iterator of Tokens that will be formatted into the description.
    :type disabled_text_tokens: Iterator[Any], optional
    """
    def __init__(
        self,
        text_identifier: Union[int, str, LocalizedString, CommonStringId],
        text_tokens: Iterator[Any]=(),
        subtext_identifier: Union[int, str, LocalizedString, CommonStringId]=None,
        subtext_tokens: Iterator[Any]=(),
        disabled_text_identifier: Union[int, str, LocalizedString, CommonStringId]=None,
        disabled_text_tokens: Iterator[Any]=()
    ):
        self._text = CommonLocalizationUtils.create_localized_string(text_identifier, tokens=tuple(text_tokens))
        self._subtext = CommonLocalizationUtils.create_localized_string(subtext_identifier, tokens=tuple(subtext_tokens)) if subtext_identifier is not None else None
        self._disabled_text = CommonLocalizationUtils.create_localized_string(disabled_text_identifier, tokens=tuple(disabled_text_tokens)) if disabled_text_identifier is not None else None

    @property
    def text(self) -> LocalizedString:
        """The text of the dialog option."""
        return self._text

    @property
    def subtext(self) -> Union[LocalizedString, None]:
        """The subtext that displays under the option."""
        return self._subtext

    @property
    def disabled_text(self) -> Union[LocalizedString, None]:
        """The text that displays on the option as a tooltip. If provided, the option will also be disabled."""
        return self._disabled_text
