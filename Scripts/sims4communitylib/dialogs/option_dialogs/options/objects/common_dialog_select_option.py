"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_object_option import CommonDialogObjectOption


class CommonDialogSelectOption(CommonDialogObjectOption):
    """CommonDialogSelectOption(option_identifier, value, context, on_chosen=CommonFunctionUtils.noop)

    An option that invokes a callback, passing in its value.

    """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def icon(self) -> Any:
        if super().icon is not None:
            return super().icon
        return CommonIconUtils.load_arrow_right_icon()
