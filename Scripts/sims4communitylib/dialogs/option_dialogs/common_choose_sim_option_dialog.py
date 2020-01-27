"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Union, Callable, Iterator

from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choose_sim_dialog import CommonChooseSimDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_option_dialog import CommonChooseOptionDialog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.dialogs.option_dialogs.options.sims.common_dialog_sim_option import CommonDialogSimOption


class CommonChooseSimOptionDialog(CommonChooseOptionDialog):
    """CommonChooseSimOptionDialog(
        title_identifier,\
        description_identifier,\
        title_tokens=(),\
        description_tokens=(),\
        on_close=CommonFunctionUtils.noop,\
        mod_identity=None\
    )

    A dialog that displays a list of Sims for selection.

    :param title_identifier: A decimal identifier of the title text.
    :type title_identifier: Union[int, LocalizedString]
    :param description_identifier: A decimal identifier of the description text.
    :type description_identifier: Union[int, LocalizedString]
    :param title_tokens: An iterable of Tokens to format into the title.
    :type title_tokens: Iterator[Any], optional
    :param description_tokens: An iterable of Tokens to format into the description.
    :type description_tokens: Iterator[Any], optional
    :param on_close: A callback invoked upon the dialog closing.
    :type on_close: Callable[..., Any], optional
    :param mod_identity: The identity of the Mod that created this dialog.
    :type mod_identity: CommonModIdentity, optional
    """
    def __init__(
        self,
        title_identifier: Union[int, LocalizedString],
        description_identifier: Union[int, LocalizedString],
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=(),
        on_close: Callable[..., Any]=CommonFunctionUtils.noop,
        mod_identity: CommonModIdentity=None
    ):
        super().__init__(
            CommonChooseSimDialog(
                title_identifier,
                description_identifier,
                tuple(),
                title_tokens=title_tokens,
                description_tokens=description_tokens,
                mod_identity=mod_identity
            ),
            on_close=on_close
        )

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cl_choose_sim_option_dialog'

    def add_option(self, option: CommonDialogSimOption):
        """Add an option to the dialog.

        :param option: The option to add.
        :type option: CommonDialogSimOption
        """
        return super().add_option(option)

    def show(
        self,
        sim_info: SimInfo=None,
        should_show_names: bool=True,
        hide_row_descriptions: bool=False,
        column_count: int=3
    ):
        """show(sim_info=None, should_show_names=True, hide_row_descriptions=False, column_count=3)

        Show the dialog and invoke the callbacks upon the player making a choice.

        :param sim_info: The SimInfo of the Sim that will appear in the dialog image. The default Sim is the active Sim.
        :type sim_info: SimInfo, optional
        :param should_show_names: If True, then the names of the Sims will display in the dialog.
        :type should_show_names: bool, optional
        :param hide_row_descriptions: A flag to hide the row descriptions.
        :type hide_row_descriptions: bool, optional
        :param column_count: The number of columns to display Sims in.
        :type column_count: int, optional
        """
        super().show(
            sim_info=sim_info,
            should_show_names=should_show_names,
            hide_row_descriptions=hide_row_descriptions,
            column_count=column_count
        )
