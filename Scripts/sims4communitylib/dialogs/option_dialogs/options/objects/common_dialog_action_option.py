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
    """CommonDialogActionOption(context, on_chosen=CommonFunctionUtils.noop, always_visible=False)

    An option that invokes a callback upon being chosen.

    :param context: A context to customize the dialog option.
    :type context: CommonDialogOptionContext
    :param on_chosen: A callback invoked when the dialog option is chosen.
    :type on_chosen: Callable[..., Any], optional
    :param always_visible: If set to True, the option will always appear in the dialog no matter which page.\
    If False, the option will act as normal. Default is False.
    :type always_visible: bool, optional
    """
    def __init__(
        self,
        context: CommonDialogOptionContext,
        on_chosen: Callable[..., Any]=CommonFunctionUtils.noop,
        always_visible: bool=False
    ):
        def _on_chosen(_, __) -> None:
            on_chosen()

        super().__init__(
            'Dialog Action',
            None,
            context,
            on_chosen=_on_chosen,
            always_visible=always_visible
        )
