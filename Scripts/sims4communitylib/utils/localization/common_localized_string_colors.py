"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.int_enum import CommonEnumIntBase
from sims4communitylib.enums.strings_enum import CommonStringId


class CommonLocalizedStringColor(CommonEnumIntBase):
    """Used to set the text color of LocalizedString.

    See the :func:`.CommonLocalizationUtils.colorize` function for more details.

    """
    DEFAULT = -1
    BLUE = CommonStringId.TEXT_WITH_BLUE_COLOR
    GREEN = CommonStringId.TEXT_WITH_GREEN_COLOR
    RED = CommonStringId.TEXT_WITH_RED_COLOR
