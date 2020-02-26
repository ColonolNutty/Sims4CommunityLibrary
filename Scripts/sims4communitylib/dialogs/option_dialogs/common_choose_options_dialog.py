"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Tuple, Any, Callable, List

from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_choose_dialog import CommonChooseDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_option_dialog import CommonChooseOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option import CommonDialogOption
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import DialogOptionValueType
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils


# noinspection PyMissingOrEmptyDocstring
class CommonChooseOptionsDialog(CommonChooseOptionDialog):
    """CommonChooseOptionsDialog(\
        internal_dialog,\
        on_close=CommonFunctionUtils.noop\
    )

    A dialog that displays a list of options and prompts to select multiple items.

    .. warning:: Unless you know what you are doing, do not create an instance of this class directly!

    :param internal_dialog: The dialog this option dialog wraps.
    :type internal_dialog: CommonChooseDialog
    :param on_close: A callback invoked upon the dialog closing.
    :type on_close: Callable[..., Any], optional
    """
    def __init__(
        self,
        internal_dialog: CommonChooseDialog,
        on_close: Callable[..., Any]=CommonFunctionUtils.noop
    ):
        super().__init__(
            internal_dialog,
            on_close=on_close
        )

    def show(
        self,
        *_,
        on_submit: Callable[[Tuple[DialogOptionValueType]], Any]=CommonFunctionUtils.noop,
        min_selectable: int=1,
        max_selectable: int=1,
        **__
    ):
        """show(\
            *_,\
            on_submit=CommonFunctionUtils.noop,\
            min_selectable=1,\
            max_selectable=1,\
            **__\
        )

        Show the dialog.

        .. note:: Override this function to provide your own arguments.

        :param on_submit: When the dialog is submit, this callback will be invoked with the selected options.
        :type on_submit: Callable[[Tuple[DialogOptionValueType]], Any], optional
        :param min_selectable: The minimum number of options that can be chosen.
        :type min_selectable: int, optional
        :param max_selectable: The maximum number of options that can be chosen.
        :type max_selectable: int, optional
        """
        @CommonExceptionHandler.catch_exceptions(self.mod_identity.name, fallback_return=False)
        def _on_chosen(chosen_options: Union[Tuple[CommonDialogOption], None], outcome: CommonChoiceOutcome) -> Any:
            if chosen_options is None or len(chosen_options) == 0 or CommonChoiceOutcome.is_error_or_cancel(outcome):
                self.close()
                return None
            chosen_values: List[DialogOptionValueType] = list()
            for chosen_option in chosen_options:
                chosen_values.append(chosen_option.value)
                chosen_option.choose()
            return on_submit(tuple(chosen_values))

        self._internal_dialog.show(*_, on_chosen=_on_chosen, min_selectable=min_selectable, max_selectable=max_selectable, **__)
