"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_object_option import CommonDialogObjectOption


class CommonDialogSelectOption(CommonDialogObjectOption):
    """ An option that invokes a callback, passing in its value. """
    @property
    def icon(self) -> Any:
        """ The icon of the option. """
        if super().icon is not None:
            return super().icon
        return CommonIconUtils.load_arrow_right_icon()
