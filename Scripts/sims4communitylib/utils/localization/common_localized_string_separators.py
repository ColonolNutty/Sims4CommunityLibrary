"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.enums.strings_enum import CommonStringId


class CommonLocalizedStringSeparator(CommonInt):
    """Used to separate multiple LocalizedString.

    See the :func:`.CommonLocalizationUtils.combine_localized_strings` function for more details.

    .. note:: The values are as follows:

    NO_SEPARATOR = "StringString"
    COLON_SPACE = "String: String"
    COMMA_SPACE = "String, String"
    SPACE = "String String"
    SPACE_PARENTHESIS_SURROUNDED = "String (String)"
    NEWLINE = "String\nString"
    HYPHEN = "String-String"
    ARE = "String are String"
    IS = "String is String"
    PLUS = "String+String"

    """
    # {String}{String}
    NO_SEPARATOR: 'CommonLocalizedStringSeparator' = CommonStringId.S4CL_COMBINE_TWO_STRINGS
    # {String}: {String}
    COLON_SPACE: 'CommonLocalizedStringSeparator' = CommonStringId.STRING_COLON_SPACE_STRING
    # {String}, {String}
    COMMA_SPACE: 'CommonLocalizedStringSeparator' = CommonStringId.STRING_COMMA_SPACE_STRING
    # {String} {String}
    SPACE: 'CommonLocalizedStringSeparator' = CommonStringId.STRING_SPACE_STRING
    # {String} ({String})
    SPACE_PARENTHESIS_SURROUNDED: 'CommonLocalizedStringSeparator' = CommonStringId.STRING_SPACE_PARENTHESIS_SURROUNDED_STRING
    # {String}\n{String}
    NEWLINE: 'CommonLocalizedStringSeparator' = CommonStringId.STRING_NEWLINE_STRING
    # {String}-{String}
    HYPHEN: 'CommonLocalizedStringSeparator' = CommonStringId.STRING_HYPHEN_STRING
    # {String} are {String}
    ARE: 'CommonLocalizedStringSeparator' = CommonStringId.S4CL_STRING_ARE_STRING
    # {String} is {String}
    IS: 'CommonLocalizedStringSeparator' = CommonStringId.S4CL_STRING_IS_STRING
    # {String}+{String}
    PLUS: 'CommonLocalizedStringSeparator' = CommonStringId.S4CL_STRING_PLUS_STRING
