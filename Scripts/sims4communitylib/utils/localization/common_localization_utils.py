"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Any, Iterator

from protocolbuffers.Localization_pb2 import LocalizedString
from sims4.localization import LocalizationHelperTuning, _create_localized_string, create_tokens, \
    TunableLocalizedStringFactory
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.localization.common_localized_string_separators import CommonLocalizedStringSeparator


class CommonLocalizationUtils:
    """Utilities for handling localization strings.

    .. note:: Localized Strings are the python equivalent of values within a StringTable.

    """
    class LocalizedTooltip(TunableLocalizedStringFactory._Wrapper):
        """CommonLocalizationUtils.LocalizedTooltip(string_id, *tokens)

        A LocalizedTooltip used when displaying tooltips.

        :param string_id: The text that will display in the tooltip.
        :type string_id: Union[int, str, LocalizedString, CommonStringId, CommonLocalizedStringSeparator]
        :param tokens: A collection of objects to format into the `string_id`
        :type tokens: Any
        """
        def __init__(self, string_id: Union[int, str, LocalizedString, CommonStringId, CommonLocalizedStringSeparator], *tokens: Any):
            super().__init__(string_id)
            self._tokens = tokens

        def __call__(self, *_) -> LocalizedString:
            return CommonLocalizationUtils.create_localized_string(self._string_id, tokens=self._tokens)

    @staticmethod
    def create_localized_tooltip(tooltip_text: Union[int, str, LocalizedString, CommonStringId, CommonLocalizedStringSeparator], tooltip_tokens: Iterator[Any]=()) -> 'LocalizedTooltip':
        """create_localized_tooltip(tooltip_text, tooltip_tokens=())

        Create a LocalizedTooltip use this when you wish to display a tooltip on various things.

        :param tooltip_text: The text that will be displayed.
        :type tooltip_text: Union[int, str, LocalizedString, CommonStringId, CommonLocalizedStringSeparator]
        :param tooltip_tokens: A collection of objects to format into the localized string. (They can be anything. LocalizedString, str, int, SimInfo, just to name a few)
        :type tooltip_tokens: Iterator[Any], optional
        :return: A tooltip ready for display.
        :rtype: LocalizedTooltip
        """
        if isinstance(tooltip_text, CommonLocalizationUtils.LocalizedTooltip):
            return tooltip_text
        if tooltip_tokens is None:
            tooltip_tokens = tuple()
        return CommonLocalizationUtils.LocalizedTooltip(tooltip_text, *tuple(tooltip_tokens))

    @staticmethod
    def create_localized_string(identifier: Union[int, str, LocalizedString, CommonStringId, CommonLocalizedStringSeparator], tokens: Iterator[Any] = (), localize_tokens: bool = True, text_color: CommonLocalizedStringColor = CommonLocalizedStringColor.DEFAULT) -> LocalizedString:
        """create_localized_string(identifier, tokens=(), localize_tokens=True, text_color=CommonLocalizedStringColor.DEFAULT)

        Create a LocalizedString formatted with the specified tokens.

        :param identifier: An identifier to locate a LocalizedString with, text that will be turned into a LocalizedString, or a LocalizedString itself.
        :type identifier: Union[int, str, LocalizedString, CommonStringId, CommonLocalizedStringSeparator]
        :param tokens: A collection of objects to format into the localized string. (They can be anything. LocalizedString, str, int, SimInfo, just to name a few)
        :type tokens: Iterator[Any]
        :param localize_tokens: If True, the specified tokens will be localized. If False, the specified tokens will be formatted into the LocalizedString as they are. Default is True
        :type localize_tokens: bool
        :param text_color: The color the text will be when displayed.
        :type text_color: CommonLocalizedStringColor
        :return: A localized string ready for display.
        :rtype: LocalizedString
        """
        if identifier is None:
            return CommonLocalizationUtils.create_localized_string(CommonStringId.STRING_NOT_FOUND_WITH_IDENTIFIER, tokens=('None',), text_color=text_color)
        if tokens is None:
            tokens = tuple()
        if localize_tokens:
            tokens = tuple(CommonLocalizationUtils._normalize_tokens(*tokens))
        if isinstance(identifier, LocalizedString) and hasattr(identifier, 'tokens'):
            create_tokens(identifier.tokens, tokens)
            return CommonLocalizationUtils.colorize(identifier, text_color=text_color)
        if isinstance(identifier, TunableLocalizedStringFactory._Wrapper):
            if isinstance(identifier._string_id, str):
                string_id = CommonLocalizationUtils.create_from_string(identifier._string_id)
            else:
                string_id = CommonLocalizationUtils.create_from_int(identifier._string_id, *tuple(tokens))
            return CommonLocalizationUtils.colorize(string_id, text_color=text_color)
        if isinstance(identifier, int):
            return CommonLocalizationUtils.colorize(CommonLocalizationUtils.create_from_int(identifier, *tuple(tokens)), text_color=text_color)
        if hasattr(identifier, 'sim_info'):
            return identifier.sim_info
        if hasattr(identifier, 'get_sim_info'):
            return identifier.get_sim_info()
        if isinstance(identifier, str):
            return CommonLocalizationUtils.create_localized_string(CommonLocalizationUtils.create_from_string(identifier), tokens=tokens, text_color=text_color)
        return CommonLocalizationUtils.create_localized_string(str(identifier), tokens=tokens, text_color=text_color)

    @staticmethod
    def combine_localized_strings(identifier_list: Iterator[Union[int, str, LocalizedString, CommonStringId, CommonLocalizedStringSeparator]], separator: CommonLocalizedStringSeparator=CommonLocalizedStringSeparator.NO_SEPARATOR) -> LocalizedString:
        """combine_localized_strings(identifier_list, separator=CommonLocalizedStringSeparator.NO_SEPARATOR)

        Combine multiple localized strings by a separator.

        :param identifier_list: A collection of identifiers to locate LocalizedStrings with, text that will be turned into a LocalizedString and combined with the other strings in the collection.
        :type identifier_list: Union[int, str, LocalizedString, CommonStringId, CommonLocalizedStringSeparator]
        :param separator: The separator to use when combining the strings. Default is to combine all of the strings by no separator, i.e. an empty space.
        :type separator: CommonLocalizedStringSeparator, optional
        :return: A localized string with all Localized Strings combined by the specified separator.
        :rtype: LocalizedString
        """
        localized = None
        for identifier in identifier_list:
            if localized is None:
                localized = identifier
            else:
                localized = CommonLocalizationUtils.create_localized_string(separator, tokens=(localized, identifier))
        return localized

    @staticmethod
    def combine_localized_strings_with_comma_space_and(identifier_list: Iterator[Union[int, str, LocalizedString, CommonStringId, CommonLocalizedStringSeparator]]) -> LocalizedString:
        """combine_localized_strings_with_comma_space_and(identifier_list)

        Combine multiple localized strings and formulate a string that is of format "{0.String}", "{0.String} and {1.String}", or "{0.String}, and {1.String}". With {0.String} being the first strings in the collection and {1.String} being the last string in the collection.

        .. note:: Example: ['one'] will turn into "one". ['one', 'two'] will turn into "one and two". ['one', 'two', 'three'] will turn into "one, two, and three".

        :param identifier_list: A collection of identifiers to combine.
        :type identifier_list: Union[int, str, LocalizedString, CommonStringId, CommonLocalizedStringSeparator]
        :return: A localized string with all Localized Strings combined with a "comma space and" separator.
        :rtype: LocalizedString
        """
        identifier_list = tuple(identifier_list)
        if not identifier_list:
            return CommonStringId.S4CL_NONE

        if len(identifier_list) <= 1:
            return CommonLocalizationUtils.combine_localized_strings(identifier_list, separator=CommonLocalizedStringSeparator.COMMA_SPACE)

        last_tag_text = identifier_list[-1]
        combined_tags_text = CommonLocalizationUtils.combine_localized_strings(identifier_list[:-1], separator=CommonLocalizedStringSeparator.COMMA_SPACE)
        if len(identifier_list) == 2:
            return CommonLocalizationUtils.combine_localized_strings((combined_tags_text, last_tag_text), separator=CommonLocalizedStringSeparator.AND)
        else:
            return CommonLocalizationUtils.combine_localized_strings((combined_tags_text, last_tag_text), separator=CommonLocalizedStringSeparator.COMMA_SPACE_AND)

    @staticmethod
    def combine_localized_strings_with_comma_space_or(identifier_list: Iterator[Union[int, str, LocalizedString, CommonStringId, CommonLocalizedStringSeparator]]) -> LocalizedString:
        """combine_localized_strings_with_comma_space_or(identifier_list)

        Combine multiple localized strings and formulate a string that is of format "{0.String}", "{0.String} or {1.String}", or "{0.String}, or {1.String}". With {0.String} being the first strings in the collection and {1.String} being the last string in the collection.

        .. note:: Example: ['one'] will turn into "one". ['one', 'two'] will turn into "one or two". ['one', 'two', 'three'] will turn into "one, two, or three".

        :param identifier_list: A collection of identifiers to combine.
        :type identifier_list: Union[int, str, LocalizedString, CommonStringId, CommonLocalizedStringSeparator]
        :return: A localized string with all Localized Strings combined with a "comma space or" separator.
        :rtype: LocalizedString
        """
        identifier_list = tuple(identifier_list)
        if not identifier_list:
            return CommonStringId.S4CL_NONE

        if len(identifier_list) <= 1:
            return CommonLocalizationUtils.combine_localized_strings(identifier_list, separator=CommonLocalizedStringSeparator.COMMA_SPACE)

        last_tag_text = identifier_list[-1]
        combined_tags_text = CommonLocalizationUtils.combine_localized_strings(identifier_list[:-1], separator=CommonLocalizedStringSeparator.COMMA_SPACE)
        if len(identifier_list) == 2:
            return CommonLocalizationUtils.combine_localized_strings((combined_tags_text, last_tag_text), separator=CommonLocalizedStringSeparator.OR)
        else:
            return CommonLocalizationUtils.combine_localized_strings((combined_tags_text, last_tag_text), separator=CommonLocalizedStringSeparator.COMMA_SPACE_OR)

    @staticmethod
    def create_from_string(string_text: str) -> LocalizedString:
        """create_from_string(string_text)

        Create a LocalizedString from a string.

        :param string_text: The string to localize. The resulting LocalizedString will be '{0.String}'
        :type string_text: str
        :return: A LocalizedString created from the specified string.
        :rtype: LocalizedString
        """
        return LocalizationHelperTuning.get_raw_text(string_text)

    @staticmethod
    def create_from_int(identifier: int, *tokens: Any) -> LocalizedString:
        """create_from_int(identifier, *tokens)

        Locate a LocalizedString by an identifier and format tokens into it.

        :param identifier: A decimal number that identifies an existing LocalizedString.
        :type identifier: int
        :param tokens: A collection of objects to format into the LocalizedString. (Example types: LocalizedString, str, int, etc.)
        :type tokens: Iterator[Any]
        :return: A LocalizedString with the specified tokens formatted into it.
        :rtype: LocalizedString
        """
        return _create_localized_string(identifier, *tokens)

    @staticmethod
    def colorize(localized_string: Union[LocalizedString, CommonStringId], text_color: CommonLocalizedStringColor = CommonLocalizedStringColor.DEFAULT) -> LocalizedString:
        """colorize(localized_string, text_color=CommonLocalizedStringColor.DEFAULT)

        Set the text color of a LocalizedString.

        :param localized_string: The LocalizedString to set the text color of.
        :type localized_string: Union[LocalizedString, CommonStringId]
        :param text_color: The text will become this color.
        :type text_color: CommonLocalizedStringColor
        :return: A LocalizedString with text in the specified color.
        :rtype: LocalizedString
        """
        if text_color == CommonLocalizedStringColor.DEFAULT:
            # Calling create_localized_string here will cause infinite loop.
            return localized_string
        if not hasattr(text_color, 'value'):
            # Calling create_localized_string here will cause infinite loop.
            return localized_string
        return CommonLocalizationUtils.create_localized_string(text_color.value, tokens=(localized_string,))

    @staticmethod
    def get_localized_string_hash(localized_string: LocalizedString) -> int:
        """get_localized_string_hash(localized_string)

        Retrieve the hash value of a Localized String.

        :param localized_string: An instance of a Localized String.
        :type localized_string: LocalizedString
        :return: The hash value of the Localized String or 0 if a problem occurs.
        :rtype: int
        """
        if localized_string is None:
            return 0
        # noinspection PyBroadException
        try:
            # noinspection PyUnresolvedReferences
            return localized_string.hash
        except:
            return 0

    @staticmethod
    def _normalize_tokens(*tokens: Any) -> Iterator[LocalizedString]:
        new_tokens = []
        for token in tokens:
            new_tokens.append(CommonLocalizationUtils.create_localized_string(token))
        return tuple(new_tokens)
