"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Tuple, Any, Callable, List

from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.option_dialogs.common_choose_option_dialog import CommonChooseOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option import CommonDialogOption
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import DialogOptionValueType
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils


class CommonChooseOptionsDialog(CommonChooseOptionDialog):
    """ A dialog that displays a list of options. """
    def show(
        self,
        *_,
        on_submit: Callable[[Tuple[DialogOptionValueType]], Any]=CommonFunctionUtils.noop,
        min_selectable: int=1,
        max_selectable: int=1,
        **__
    ):
        """ Show the dialog. """
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
