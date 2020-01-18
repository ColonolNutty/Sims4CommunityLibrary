"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable
from sims.sim_info import SimInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog_picker import SimPickerRow
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option import CommonDialogOption
from sims4communitylib.dialogs.option_dialogs.options.sims.common_dialog_sim_option_context import CommonDialogSimOptionContext


class CommonDialogSimOption(CommonDialogOption):
    """ A option the player can choose within a dialog.  """
    def __init__(
        self,
        sim_info: SimInfo,
        context: CommonDialogSimOptionContext,
        on_chosen: Callable[[SimInfo], Any]=CommonFunctionUtils.noop
    ):
        super().__init__(
            sim_info,
            context,
            on_chosen=on_chosen
        )

    @property
    def value(self) -> SimInfo:
        """ The value of the option. """
        return self._value

    @property
    def sim_id(self) -> int:
        """ The id of the Sim in this option. """
        return CommonSimUtils.get_sim_id(self.value)

    def as_row(self, option_id: int) -> SimPickerRow:
        """ Convert the option into a row. """
        return SimPickerRow(
            self.sim_id,
            select_default=self.context.is_selected,
            is_enable=self.context.is_enabled,
            tag=self
        )
