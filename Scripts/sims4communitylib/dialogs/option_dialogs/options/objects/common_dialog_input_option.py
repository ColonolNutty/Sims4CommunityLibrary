"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable

from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_object_option import CommonDialogObjectOption
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.common_input_float_dialog import CommonInputFloatDialog


class CommonDialogInputFloatOption(CommonDialogObjectOption):
    """An option to open a dialog to input a float value.

    """
    def __init__(
        self,
        option_identifier: str,
        initial_value: float,
        context: CommonDialogOptionContext,
        min_value: float=0.0,
        max_value: float=2147483647.0,
        on_chosen: Callable[[str, float, CommonChoiceOutcome], Any]=CommonFunctionUtils.noop
    ):
        self._dialog = CommonInputFloatDialog(
            context.title,
            context.description,
            initial_value,
            min_value=min_value,
            max_value=max_value
        )

        def _on_submit(_: float, __: CommonChoiceOutcome):
            on_chosen(self.option_identifier, _, __)

        def _on_chosen(_, __):
            self._dialog.show(on_submit=_on_submit)

        super().__init__(
            option_identifier,
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
        return CommonIconUtils.load_arrow_right_icon()
