"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import random
import sims4.commands
from typing import Any, Union, Callable, Iterator

from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choose_sim_dialog import CommonChooseSimDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_option_dialog import CommonChooseOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.sims.common_dialog_sim_option_context import \
    CommonDialogSimOptionContext
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.dialogs.option_dialogs.options.sims.common_dialog_sim_option import CommonDialogSimOption
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


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

        # Create the dialog and only showing 2 options per page.
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
    :type title_identifier: Union[int, LocalizedString]
    :param description_identifier: A decimal identifier of the description text.
    :type description_identifier: Union[int, LocalizedString]
    :param title_tokens: An iterable of Tokens to format into the title.
    :type title_tokens: Iterator[Any], optional
    :param description_tokens: An iterable of Tokens to format into the description.
    :type description_tokens: Iterator[Any], optional
    :param on_close: A callback invoked upon the dialog closing.
    :type on_close: Callable[..., Any], optional
    :param mod_identity: The identity of the mod creating the dialog. See :class:`.CommonModIdentity` for more information.
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


@sims4.commands.Command('s4clib_testing.show_choose_sim_option_dialog', command_type=sims4.commands.CommandType.Live)
def _common_testing_show_choose_sim_option_dialog(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing test choose sim option dialog.')

    def _on_chosen(_sim_info: SimInfo):
        output('Chose Sim with name \'{}\''.format(CommonSimNameUtils.get_full_name(_sim_info)))

    try:
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

        # Create the dialog and only showing 2 options per page.
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
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to show dialog', exception=ex)
        output('Failed to show dialog, please locate your exception log file.')
    output('Done showing.')
