"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import sims4.commands
from typing import Any, Callable, Union, Iterator, Tuple

from pprint import pformat

import random
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_choose_sim_dialog import CommonChooseSimDialog
from sims4communitylib.dialogs.utils.common_dialog_utils import CommonDialogUtils
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog_picker import UiSimPicker, SimPickerRow

log = CommonLogRegistry.get().register_log(ModInfo.get_identity().name, 's4cl_choose_sims_dialog')


class CommonChooseSimsDialog(CommonChooseSimDialog):
    """
        Create a dialog that asks the player to choose a number of Sims.
    """
    def __init__(
        self,
        title_identifier: Union[int, LocalizedString],
        description_identifier: Union[int, LocalizedString],
        choices: Iterator[SimPickerRow],
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=()
    ):
        """
            Create a dialog for displaying a list of Sims.
        :param title_identifier: A decimal identifier of the title text.
        :param description_identifier: A decimal identifier of the description text.
        :param choices: The choices to display in the dialog.
        :param title_tokens: Tokens to format into the title.
        :param description_tokens: Tokens to format into the description.
        """
        super().__init__(
            title_identifier,
            description_identifier,
            choices,
            title_tokens=title_tokens,
            description_tokens=description_tokens
        )

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name)
    def add_row(self, choice: SimPickerRow):
        """
            Add a choice to the dialog.
        """
        self._choices += (choice,)

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name)
    def show(
        self,
        on_chosen: Callable[[Union[Tuple[SimInfo], None], CommonChoiceOutcome], Any]=CommonFunctionUtils.noop,
        sim_info: SimInfo=None,
        should_show_names: bool=True,
        hide_row_descriptions: bool=False,
        column_count: int=3,
        min_selectable: int=1,
        max_selectable: int=1
    ):
        """
            Show the dialog and invoke the callbacks upon the player submitting their selection.
        :param on_chosen: A callback invoked upon the player submitting their chosen Sims from the list.
        :param sim_info: The SimInfo of the Sim that will appear in the dialog image. The default Sim is the active Sim.
        :param should_show_names: If True, then the names of the Sims will display in the dialog.
        :param hide_row_descriptions: A flag to hide the row descriptions.
        :param column_count: The number of columns to display Sims in.
        :param min_selectable: The minimum number of Sims that must be chosen.
        :param max_selectable: The maximum number of Sims that can be chosen.
        """
        if min_selectable < 1:
            raise AttributeError('\'min_selectable\' must be at least 1.')
        if max_selectable < min_selectable:
            raise AttributeError('\'max_selectable\' must be greater than \'min_selectable\'.')
        log.format_with_message('Attempting to display choices.')
        _dialog = self._create_dialog(
            sim_info=sim_info,
            should_show_names=should_show_names,
            hide_row_descriptions=hide_row_descriptions,
            column_count=column_count,
            min_selectable=min_selectable,
            max_selectable=max_selectable
        )
        if _dialog is None:
            log.error('_dialog was None for some reason.')
            return

        if on_chosen is None:
            raise ValueError('on_chosen was None.')

        if len(self._choices) == 0:
            raise AssertionError('No rows have been provided. Add rows to the dialog before attempting to display it.')

        @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name)
        def _on_chosen(dialog: UiSimPicker):
            if not dialog.accepted:
                log.debug('Dialog cancelled.')
                return on_chosen(None, CommonChoiceOutcome.CANCEL)
            choices = tuple(CommonDialogUtils.get_chosen_items(dialog))
            log.format_with_message('Choice made.', choice=choices)
            result = on_chosen(choices, CommonChoiceOutcome.CHOICE_MADE)
            log.format_with_message('Finished handling choice.', result=result)
            return result

        log.debug('Adding all choices')
        for row in self._choices:
            _dialog.add_row(row)

        _dialog.add_listener(_on_chosen)
        _dialog.show_dialog()


@sims4.commands.Command('s4clib_testing.show_choose_sims_dialog', command_type=sims4.commands.CommandType.Live)
def _common_testing_show_choose_sims_dialog(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing test choose sims dialog.')

    def _on_chosen(choice: Union[Tuple[SimInfo], None], outcome: CommonChoiceOutcome):
        output('Chose {} with result: {}.'.format(CommonSimNameUtils.get_full_names(choice), pformat(outcome)))

    try:
        # LocalizedStrings within other LocalizedStrings
        title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
        description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
        from sims4communitylib.utils.common_icon_utils import CommonIconUtils
        current_count = 0
        count = 25
        options = []
        for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
            if current_count >= count:
                break
            sim_id = CommonSimUtils.get_sim_id(sim_info)
            is_enabled = random.choice((True, False))
            options.append(
                SimPickerRow(
                    sim_id,
                    select_default=False,
                    tag=sim_info,
                    is_enable=is_enabled
                )
            )
            current_count += 1

        dialog = CommonChooseSimsDialog(
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            tuple(options),
            title_tokens=title_tokens,
            description_tokens=description_tokens
        )
        dialog.show(
            on_chosen=_on_chosen,
            column_count=5,
            min_selectable=2,
            max_selectable=6
        )
    except Exception as ex:
        log.format_error_with_message('Failed to show dialog', exception=ex)
        output('Failed to show dialog, please locate your exception log file and upload it to the appropriate thread.')
    output('Done showing.')
