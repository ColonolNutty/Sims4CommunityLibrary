"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Tuple, Any

from protocolbuffers.Localization_pb2 import LocalizedString
from sims4.localization import LocalizationHelperTuning, _create_localized_string, create_tokens
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor


class CommonLocalizationUtils:
    """ Utilities for handling localization strings """
    @staticmethod
    def create_localized_string(identifier: Union[int, str, LocalizedString], tokens: Tuple[Any]=(), localize_tokens: bool=True, text_color: CommonLocalizedStringColor=CommonLocalizedStringColor.DEFAULT) -> LocalizedString:
        """
            Create a LocalizedString formatted with the specified tokens.
        :param identifier: An identifier to locate a LocalizedString with, text that will be turned into a LocalizedString, or a LocalizedString itself.
        :param tokens: A collection of objects to format into the localized string. (They can be anything. LocalizedString, str, int, SimInfo, just to name a few)
        :param localize_tokens: If True, the specified tokens will be localized. If False, the specified tokens will be formatted into the LocalizedString as they are. Default is True
        :param text_color: The color the text will be when displayed.
        :return: An object of type LocalizedString
        """
        if identifier is None:
            return CommonLocalizationUtils.create_localized_string(CommonStringId.STRING_NOT_FOUND_WITH_IDENTIFIER, tokens=('None',), text_color=text_color)
        if localize_tokens:
            tokens = CommonLocalizationUtils._normalize_tokens(*tokens)
        if isinstance(identifier, LocalizedString) and hasattr(identifier, 'tokens'):
            create_tokens(identifier.tokens, tokens)
            return CommonLocalizationUtils.colorize(identifier, text_color=text_color)
        if isinstance(identifier, int):
            return CommonLocalizationUtils.colorize(CommonLocalizationUtils.create_from_int(identifier, *tokens), text_color=text_color)
        if hasattr(identifier, 'sim_info'):
            return identifier.sim_info
        if hasattr(identifier, 'get_sim_info'):
            return identifier.get_sim_info()
        if isinstance(identifier, str):
            return CommonLocalizationUtils.create_localized_string(CommonLocalizationUtils.create_from_string(identifier), tokens=tokens, text_color=text_color)
        return CommonLocalizationUtils.create_localized_string(str(identifier), tokens=tokens, text_color=text_color)

    @staticmethod
    def create_from_string(string_text: str) -> LocalizedString:
        """
            Create a LocalizedString from a string.
        :param string_text: The string to localize. The resulting LocalizedString will be '{0.String}'
        :return: A LocalizedString created from the specified string.
        """
        return LocalizationHelperTuning.get_raw_text(string_text)

    @staticmethod
    def create_from_int(identifier: int, *tokens: Any) -> LocalizedString:
        """
            Locate a LocalizedString by an identifier and format tokens into it.
        :param identifier: A decimal number that identifies an existing LocalizedString.
        :param tokens: A collection of objects to format into the LocalizedString. (Example types: LocalizedString, str, int, etc.)
        :return: A LocalizedString with the specified tokens formatted into it.
        """
        return _create_localized_string(identifier, *tokens)

    @staticmethod
    def colorize(localized_string: LocalizedString, text_color: CommonLocalizedStringColor=CommonLocalizedStringColor.DEFAULT) -> LocalizedString:
        """
            Color the text of a LocalizedString with the specified color.
        :param localized_string: The LocalizedString to set the text color of.
        :param text_color: The text will become this color.
        :return: A LocalizedString with text in the specified color.
        """
        if text_color == CommonLocalizedStringColor.DEFAULT:
            return localized_string
        from sims4communitylib.enums.enumtypes.int_enum import CommonEnumInt
        text_color: CommonEnumInt = text_color
        return CommonLocalizationUtils.create_localized_string(text_color.value, tokens=(localized_string,))

    @staticmethod
    def _normalize_tokens(*tokens: Any) -> Tuple[LocalizedString]:
        new_tokens = []
        for token in tokens:
            new_tokens.append(CommonLocalizationUtils.create_localized_string(token))
        return tuple(new_tokens)
