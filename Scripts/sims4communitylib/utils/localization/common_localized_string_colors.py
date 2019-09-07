"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.int_enum import CommonEnumIntBase
from sims4communitylib.enums.strings_enum import CommonStringId


class CommonLocalizedStringColor(CommonEnumIntBase):
    """ Colors for adding color to the text of LocalizedStrings. """
    DEFAULT = -1
    BLUE = CommonStringId.TEXT_WITH_BLUE_COLOR
    GREEN = CommonStringId.TEXT_WITH_GREEN_COLOR
    RED = CommonStringId.TEXT_WITH_RED_COLOR
