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
    AND = "{String} and {String}"
    ARE = "String are String"
    COLON_SPACE = "String: String"
    COMMA_SPACE = "String, String"
    COMMA_SPACE_AND = "{String}, and {String}"
    COMMA_SPACE_OR = "{String}, or {String}"
    HYPHEN = "String-String"
    IS = "String is String"
    NEWLINE = "String\nString"
    NEWLINE_NEWLINE = "String\n\nString"
    OR = "String or String"
    PLUS = "String+String"
    SPACE = "String String"
    SPACE_PARENTHESIS_SURROUNDED = "String (String)"

    """
    # {String}{String}
    NO_SEPARATOR: 'CommonLocalizedStringSeparator' = CommonStringId.S4CL_COMBINE_TWO_STRINGS
    # {String} and {String}
    AND: 'CommonLocalizedStringSeparator' = CommonStringId.S4CL_STRING_AND_STRING
    # {String} are {String}
    ARE: 'CommonLocalizedStringSeparator' = CommonStringId.S4CL_STRING_ARE_STRING
    # {String}: {String}
    COLON_SPACE: 'CommonLocalizedStringSeparator' = CommonStringId.STRING_COLON_SPACE_STRING
    # {String}, {String}
    COMMA_SPACE: 'CommonLocalizedStringSeparator' = CommonStringId.STRING_COMMA_SPACE_STRING
    # {String}, and {String}
    COMMA_SPACE_AND: 'CommonLocalizedStringSeparator' = CommonStringId.S4CL_STRING_COMMA_SPACE_AND_STRING
    # {String}, or {String}
    COMMA_SPACE_OR: 'CommonLocalizedStringSeparator' = CommonStringId.S4CL_STRING_COMMA_SPACE_OR_STRING
    # {String}-{String}
    HYPHEN: 'CommonLocalizedStringSeparator' = CommonStringId.STRING_HYPHEN_STRING
    # {String} is {String}
    IS: 'CommonLocalizedStringSeparator' = CommonStringId.S4CL_STRING_IS_STRING
    # {String}\n{String}
    NEWLINE: 'CommonLocalizedStringSeparator' = CommonStringId.STRING_NEWLINE_STRING
    # {String}\n\n{String}
    NEWLINE_NEWLINE: 'CommonLocalizedStringSeparator' = CommonStringId.STRING_NEWLINE_NEWLINE_STRING
    # {String} or {String}
    OR: 'CommonLocalizedStringSeparator' = CommonStringId.S4CL_STRING_OR_STRING
    # {String}+{String}
    PLUS: 'CommonLocalizedStringSeparator' = CommonStringId.S4CL_STRING_PLUS_STRING
    # {String} {String}
    SPACE: 'CommonLocalizedStringSeparator' = CommonStringId.STRING_SPACE_STRING
    # {String} ({String})
    SPACE_PARENTHESIS_SURROUNDED: 'CommonLocalizedStringSeparator' = CommonStringId.STRING_SPACE_PARENTHESIS_SURROUNDED_STRING
