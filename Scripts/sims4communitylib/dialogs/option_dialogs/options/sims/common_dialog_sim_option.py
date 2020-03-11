"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

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
    """CommonDialogSimOption(sim_info, context, on_chosen=CommonFunctionUtils.noop)

    An option the player can choose within a dialog.

    :param sim_info: The Sim that will be chosen when the option is chosen.
    :type sim_info: SimInfo
    :param context: A context to customize the dialog option.
    :type context: CommonDialogOptionContext
    :param on_chosen: A callback invoked when the dialog option is chosen. args: (sim_info)
    :type on_chosen: Callable[[SimInfo], Any], optional
    """

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

    # noinspection PyMissingOrEmptyDocstring
    @property
    def value(self) -> SimInfo:
        return self._value

    @property
    def sim_id(self) -> int:
        """The id of the Sim in this option.

        :return: The id of the Sim within the option.
        :rtype: int
        """
        return CommonSimUtils.get_sim_id(self.value)

    def as_row(self, option_id: int) -> SimPickerRow:
        """as_row(option_id)

        Convert the option into a picker row.

        :param option_id: The index of the option.
        :type option_id: int
        :return: The option as a Picker Row
        :rtype: SimPickerRow
        """
        return SimPickerRow(
            self.sim_id,
            select_default=self.context.is_selected,
            is_enable=self.context.is_enabled,
            tag=self
        )
