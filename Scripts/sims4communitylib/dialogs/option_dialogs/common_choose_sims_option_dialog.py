"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Tuple, Union, Callable, Iterator

from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choose_sims_dialog import CommonChooseSimsDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_options_dialog import CommonChooseOptionsDialog
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.dialogs.option_dialogs.options.sims.common_dialog_sim_option import CommonDialogSimOption
from sims4communitylib.modinfo import ModInfo


class CommonChooseSimsOptionDialog(CommonChooseOptionsDialog):
    """A dialog that displays a list of Sims.

    """
    def __init__(
        self,
        title_identifier: Union[int, LocalizedString],
        description_identifier: Union[int, LocalizedString],
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=(),
        on_close: Callable[..., Any]=CommonFunctionUtils.noop,
        mod_identity: ModInfo=None
    ):
        """Create a dialog to display a list of Sims.

        :param title_identifier: A decimal identifier of the title text.
        :param description_identifier: A decimal identifier of the description text.
        :param title_tokens: Tokens to format into the title.
        :param description_tokens: Tokens to format into the description.
        :param on_close: A callback invoked upon the dialog closing.
        """
        super().__init__(
            CommonChooseSimsDialog(
                title_identifier,
                description_identifier,
                tuple(),
                title_tokens=title_tokens,
                description_tokens=description_tokens,
                mod_identity=mod_identity
            ),
            on_close=on_close
        )

    def add_option(self, option: CommonDialogSimOption):
        """Add an option to the dialog.

        """
        return super().add_option(option)

    def show(
        self,
        on_submit: Callable[[Tuple[SimInfo]], Any]=CommonFunctionUtils.noop,
        sim_info: SimInfo=None,
        should_show_names: bool=True,
        hide_row_descriptions: bool=False,
        column_count: int=3,
        min_selectable: int=1,
        max_selectable: int=1
    ):
        """Show the dialog and invoke the callbacks upon the player submitting their selection.

        :param on_submit: A callback invoked upon the player choosing Sims.
        :param sim_info: The SimInfo of the Sim that will appear in the dialog image. The default Sim is the active Sim.
        :param should_show_names: If True, then the names of the Sims will display in the dialog.
        :param hide_row_descriptions: A flag to hide the row descriptions.
        :param column_count: The number of columns to display Sims in.
        :param min_selectable: The minimum number of Sims that must be chosen.
        :param max_selectable: The maximum number of Sims that can be chosen.
        """
        return super().show(
            on_submit=on_submit,
            sim_info=sim_info,
            should_show_names=should_show_names,
            hide_row_descriptions=hide_row_descriptions,
            column_count=column_count,
            min_selectable=min_selectable,
            max_selectable=max_selectable
        )

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name)
    def has_options(self) -> bool:
        """Determine if the dialog has selectable options.

        """
        return self.option_count > 0
