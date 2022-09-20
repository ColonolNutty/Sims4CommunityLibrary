"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import random
from typing import Any, Union, Callable, Iterator

from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choose_sim_dialog import CommonChooseSimDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_option_dialog import CommonChooseOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.sims.common_dialog_sim_option_context import \
    CommonDialogSimOptionContext
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.dialogs.option_dialogs.options.sims.common_dialog_sim_option import CommonDialogSimOption
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog import UiDialogBase


class CommonChooseSimOptionDialog(CommonChooseOptionDialog):
    """CommonChooseSimOptionDialog(\
        title_identifier,\
        description_identifier,\
        title_tokens=(),\
        description_tokens=(),\
        on_close=CommonFunctionUtils.noop,\
        mod_identity=None,\
        required_tooltip=None,\
        required_tooltip_tokens=()\
    )

    A dialog that displays a list of Sims for selection.

    .. note:: To see an example dialog, run the command :class:`s4clib_testing.show_choose_sim_option_dialog` in the in-game console.

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        def _on_chosen(_sim_info: SimInfo):
            pass

        # LocalizedStrings within other LocalizedStrings
        title_tokens = (
            CommonLocalizationUtils.create_localized_string(
                CommonStringId.TESTING_SOME_TEXT_FOR_TESTING,
                text_color=CommonLocalizedStringColor.GREEN
            ),
        )
        description_tokens = (
            CommonLocalizationUtils.create_localized_string(
                CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME,
                tokens=(CommonSimUtils.get_active_sim_info(),),
                text_color=CommonLocalizedStringColor.BLUE
            ),
        )

        # Create the dialog and show a number of Sims in 4 columns.
        option_dialog = CommonChooseSimOptionDialog(
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            title_tokens=title_tokens,
            description_tokens=description_tokens,
            mod_identity=ModInfo.get_identity()
        )

        current_count = 0
        count = 25

        for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
            if current_count >= count:
                break
            should_select = random.choice((True, False))
            is_enabled = random.choice((True, False))
            option_dialog.add_option(
                CommonDialogSimOption(
                    sim_info,
                    CommonDialogSimOptionContext(
                        is_enabled=is_enabled,
                        is_selected=should_select
                    ),
                    on_chosen=_on_chosen
                )
            )

        option_dialog.show(
            sim_info=CommonSimUtils.get_active_sim_info(),
            column_count=4
        )

    :param title_identifier: A decimal identifier of the title text.
    :type title_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param description_identifier: A decimal identifier of the description text.
    :type description_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param title_tokens: An iterator of Tokens to format into the title.
    :type title_tokens: Iterator[Any], optional
    :param description_tokens: An iterator of Tokens to format into the description.
    :type description_tokens: Iterator[Any], optional
    :param on_close: A callback invoked upon the dialog closing.
    :type on_close: Callable[[], None], optional
    :param mod_identity: The identity of the mod creating the dialog. See :class:`.CommonModIdentity` for more information.
    :type mod_identity: CommonModIdentity, optional
    :param required_tooltip: If provided, this text will display when the dialog requires at least one choice and a choice has not been made. Default is None.
    :type required_tooltip: Union[int, str, LocalizedString, CommonStringId], optional
    :param required_tooltip_tokens: Tokens to format into the required tooltip. Default is an empty collection.
    :type required_tooltip_tokens: Iterator[Any], optional
    """
    def __init__(
        self,
        title_identifier: Union[int, str, LocalizedString, CommonStringId],
        description_identifier: Union[int, str, LocalizedString, CommonStringId],
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=(),
        on_close: Callable[[], None]=CommonFunctionUtils.noop,
        mod_identity: CommonModIdentity=None,
        required_tooltip: Union[int, str, LocalizedString, CommonStringId]=None,
        required_tooltip_tokens: Iterator[Any]=()
    ):
        super().__init__(
            CommonChooseSimDialog(
                title_identifier,
                description_identifier,
                tuple(),
                title_tokens=title_tokens,
                description_tokens=description_tokens,
                mod_identity=mod_identity,
                required_tooltip=required_tooltip,
                required_tooltip_tokens=required_tooltip_tokens
            ),
            on_close=on_close
        )

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cl_choose_sim_option_dialog'

    def add_option(self, option: CommonDialogSimOption):
        """add_option(option)

        Add an option to the dialog.

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

        Show the dialog.

        :param sim_info: The SimInfo of the Sim that will appear in the dialog image. The default Sim is the active Sim.
        :type sim_info: SimInfo, optional
        :param should_show_names: If True, then the names of the Sims will display in the dialog.
        :type should_show_names: bool, optional
        :param hide_row_descriptions: A flag to hide the row descriptions.
        :type hide_row_descriptions: bool, optional
        :param column_count: The number of columns to display Sims in.
        :type column_count: int, optional
        """
        return super().show(
            sim_info=sim_info,
            should_show_names=should_show_names,
            hide_row_descriptions=hide_row_descriptions,
            column_count=column_count
        )

    def build_dialog(
        self,
        sim_info: SimInfo=None,
        should_show_names: bool=True,
        hide_row_descriptions: bool=False,
        column_count: int=3
    ) -> Union[UiDialogBase, None]:
        """build_dialog(sim_info=None, should_show_names=True, hide_row_descriptions=False, column_count=3)

        Build the dialog.

        :param sim_info: The SimInfo of the Sim that will appear in the dialog image. The default Sim is the active Sim. Default is None.
        :type sim_info: SimInfo, optional
        :param should_show_names: If True, then the names of the Sims will display in the dialog. Default is True.
        :type should_show_names: bool, optional
        :param hide_row_descriptions: A flag to hide the row descriptions. Default is False.
        :type hide_row_descriptions: bool, optional
        :param column_count: The number of columns to display Sims in. Default is 3.
        :type column_count: int, optional
        :return: The built dialog or None if a problem occurs.
        :rtype: Union[UiDialogBase, None]
        """
        return super().build_dialog(
            sim_info=sim_info,
            should_show_names=should_show_names,
            hide_row_descriptions=hide_row_descriptions,
            column_count=column_count
        )


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.show_choose_sim_option_dialog',
    'Show an example of CommonChooseSimOptionDialog.'
)
def _common_testing_show_choose_sim_option_dialog(output: CommonConsoleCommandOutput):
    output('Showing test choose sim option dialog.')

    def _on_chosen(_sim_info: SimInfo):
        output('Chose Sim with name \'{}\''.format(CommonSimNameUtils.get_full_name(_sim_info)))

    # LocalizedStrings within other LocalizedStrings
    title_tokens = (
        CommonLocalizationUtils.create_localized_string(
            CommonStringId.TESTING_SOME_TEXT_FOR_TESTING,
            text_color=CommonLocalizedStringColor.GREEN
        ),
    )
    description_tokens = (
        CommonLocalizationUtils.create_localized_string(
            CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME,
            tokens=(CommonSimUtils.get_active_sim_info(),),
            text_color=CommonLocalizedStringColor.BLUE
        ),
    )

    # Create the dialog and show a number of Sims in 4 columns.
    option_dialog = CommonChooseSimOptionDialog(
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        title_tokens=title_tokens,
        description_tokens=description_tokens,
        mod_identity=ModInfo.get_identity()
    )

    current_count = 0
    count = 25

    for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
        if current_count >= count:
            break
        should_select = random.choice((True, False))
        is_enabled = random.choice((True, False))
        option_dialog.add_option(
            CommonDialogSimOption(
                sim_info,
                CommonDialogSimOptionContext(
                    is_enabled=is_enabled,
                    is_selected=should_select
                ),
                on_chosen=_on_chosen
            )
        )

    option_dialog.show(
        sim_info=CommonSimUtils.get_active_sim_info(),
        column_count=4
    )
    output('Done showing.')
