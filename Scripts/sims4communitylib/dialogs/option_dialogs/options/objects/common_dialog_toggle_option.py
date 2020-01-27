"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_object_option import CommonDialogObjectOption


class CommonDialogToggleOption(CommonDialogObjectOption):
    """CommonDialogObjectOption(option_identifier, value, context, on_chosen=CommonFunctionUtils.noop)

    An option with two states, on or off.
    """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def icon(self) -> Any:
        if super().icon is not None:
            return super().icon
        if self.value is True:
            return CommonIconUtils.load_checked_square_icon()
        return CommonIconUtils.load_unchecked_square_icon()

    # noinspection PyMissingOrEmptyDocstring
    def choose(self) -> Any:
        if self.on_chosen is None:
            return None
        return self.on_chosen(not bool(self.value))
