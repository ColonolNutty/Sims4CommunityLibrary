"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_object_option import CommonDialogObjectOption
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog


class CommonDialogOpenDialogOption(CommonDialogObjectOption):
    """An option that branches into other options.

    """
    def __init__(
        self,
        create_dialog_callback: Callable[..., CommonChooseObjectOptionDialog],
        context: CommonDialogOptionContext
    ):
        def _on_chosen(_, __):
            create_dialog_callback().show()

        super().__init__(
            'Dialog Branch',
            None,
            context,
            on_chosen=_on_chosen
        )

    @property
    def icon(self) -> Any:
        """The icon of the option.

        """
        if super().icon is not None:
            return super().icon
        return CommonIconUtils.load_arrow_navigate_into_icon()
