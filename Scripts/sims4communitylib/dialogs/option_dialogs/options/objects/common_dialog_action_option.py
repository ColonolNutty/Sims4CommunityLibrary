"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable

from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import CommonDialogSelectOption


class CommonDialogActionOption(CommonDialogSelectOption):
    """An option that invokes a callback upon being chosen.

    """
    def __init__(
        self,
        context: CommonDialogOptionContext,
        on_chosen: Callable[..., Any]=CommonFunctionUtils.noop,
    ):
        def _on_chosen(_, __):
            on_chosen()

        super().__init__(
            'Dialog Action',
            None,
            context,
            on_chosen=_on_chosen
        )
