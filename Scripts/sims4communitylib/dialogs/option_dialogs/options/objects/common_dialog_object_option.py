"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from ui.ui_dialog_picker import ObjectPickerRow
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option import CommonDialogOption
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext, \
    DialogOptionValueType


class CommonDialogObjectOption(CommonDialogOption):
    """A option the player can choose within a dialog.

    """
    def __init__(
        self,
        option_identifier: str,
        value: DialogOptionValueType,
        context: CommonDialogOptionContext,
        on_chosen: Callable[[str, DialogOptionValueType], Any]=CommonFunctionUtils.noop
    ):
        if option_identifier is None:
            raise AttributeError('Missing required argument \'option_identifier\'')

        self._option_identifier = option_identifier

        def _on_chosen(val: DialogOptionValueType) -> Any:
            return on_chosen(self.option_identifier, val)

        super().__init__(value, context, on_chosen=_on_chosen)

    @property
    def option_identifier(self) -> str:
        """Used to identify the option.

        """
        return self._option_identifier

    @property
    def value(self) -> DialogOptionValueType:
        """The value of the option.

        """
        return self._value

    def as_row(self, option_id: int) -> ObjectPickerRow:
        """Convert the option into a row.

        """
        return ObjectPickerRow(
            option_id=option_id,
            name=self.title,
            row_description=self.description,
            row_tooltip=self.tooltip,
            icon=self.icon,
            tag=self
        )
