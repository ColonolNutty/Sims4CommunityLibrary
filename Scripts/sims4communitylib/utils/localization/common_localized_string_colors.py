"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.enums.strings_enum import CommonStringId


class CommonLocalizedStringColor(CommonInt):
    """Used to set the text color of LocalizedString.

    See the :func:`.CommonLocalizationUtils.colorize` function for more details.

    """
    DEFAULT: 'CommonLocalizedStringColor' = -1
    BLUE: 'CommonLocalizedStringColor' = CommonStringId.TEXT_WITH_BLUE_COLOR
    GREEN: 'CommonLocalizedStringColor' = CommonStringId.TEXT_WITH_GREEN_COLOR
    RED: 'CommonLocalizedStringColor' = CommonStringId.TEXT_WITH_RED_COLOR
    YELLOW: 'CommonLocalizedStringColor' = CommonStringId.TEXT_WITH_YELLOW_COLOR
    ORANGE: 'CommonLocalizedStringColor' = CommonStringId.TEXT_WITH_ORANGE_COLOR
