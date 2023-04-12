"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union

from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.enums.common_character_restrictions import CommonCharacterRestriction
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.localization.common_localized_string_separators import CommonLocalizedStringSeparator


class CommonInputTextField:
    """CommonInputTextField(\
        identifier,\
        initial_value,\
        title=None,\
        character_restriction=CommonCharacterRestriction.NONE,\
        default_text=None\
    )

    A field intended for use with an input text dialog. It allows entering of text.

    :param identifier: The identifier of the input.
    :type identifier: str
    :param initial_value: The initial value of the text input.
    :type initial_value: str
    :param title: A title to display above the input. Default is None.
    :type title: Union[int, str, LocalizedString, CommonStringId, CommonLocalizedStringSeparator], optional
    :param character_restriction: A character restriction to enforce what can be entered or not. Default is NONE.
    :type character_restriction: CommonCharacterRestriction, optional
    :param default_text: The default text shown when nothing is entered into the field. Default is None.
    :type default_text: Union[int, str, LocalizedString, CommonStringId, CommonLocalizedStringSeparator], optional
    """
    def __init__(
        self,
        identifier: str,
        initial_value: str,
        title: Union[int, str, LocalizedString, CommonStringId, CommonLocalizedStringSeparator, None] = None,
        character_restriction: CommonCharacterRestriction = CommonCharacterRestriction.NONE,
        default_text: Union[int, str, LocalizedString, CommonStringId, CommonLocalizedStringSeparator, None] = None
    ):
        self._identifier = identifier
        self._initial_value = initial_value
        self._title = title
        self._character_restriction = character_restriction
        self._default_text = default_text

    # 'default_text',
    # 'height',
    # 'initial_value',
    # 'input_invalid_max_tooltip',
    # 'input_invalid_min_tooltip',
    # 'input_too_short_tooltip',
    # 'max_length',
    # 'max_value',
    # 'message_descriptor',
    # 'min_length',
    # 'min_value',
    # 'restricted_characters',
    # 'text_input_name',
    # 'title'
    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cl_input_text_dialog'

    @property
    def identifier(self) -> str:
        """The identifier of the input."""
        return self._identifier

    @property
    def initial_value(self) -> str:
        """The initial value the field will have entered."""
        return self._initial_value

    @property
    def default_text(self) -> Union[int, str, LocalizedString, CommonStringId, CommonLocalizedStringSeparator, None]:
        """The default text that will show in the field when nothing is entered."""
        return self._default_text

    @property
    def title(self) -> Union[int, str, LocalizedString, CommonStringId, CommonLocalizedStringSeparator, None]:
        """The title to display above the text field."""
        return self._title

    @property
    def character_restriction(self) -> CommonCharacterRestriction:
        """A character restriction to enforce what can be entered or not."""
        return self._character_restriction
