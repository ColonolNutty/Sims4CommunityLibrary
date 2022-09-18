"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable, Union, Tuple, Iterator

from pprint import pformat

import random

from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_choose_sim_dialog import CommonChooseSimDialog
from sims4communitylib.dialogs.option_dialogs.options.sims.common_dialog_sim_option import CommonDialogSimOption
from sims4communitylib.dialogs.utils.common_dialog_utils import CommonDialogUtils
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog_picker import UiSimPicker, SimPickerRow


class CommonChooseSimsDialog(CommonChooseSimDialog):
    """CommonChooseSimsDialog(\
        title_identifier,\
        description_identifier,\
        choices,\
        title_tokens=(),\
        description_tokens=(),\
        mod_identity=None,\
        required_tooltip=None,\
        required_tooltip_tokens=()\
    )

    Create a dialog that prompts the player to choose a number of Sims.

    .. note:: To see an example dialog, run the command :class:`s4clib_testing.show_choose_sims_dialog` in the in-game console.

    .. highlight:: python
    .. code-block:: python

       def _common_testing_show_choose_sims_dialog():

            def _on_chosen(choice: Union[Tuple[SimInfo], None], outcome: CommonChoiceOutcome):
                pass

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

    :param title_identifier: A decimal identifier of the title text.
    :type title_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param description_identifier: A decimal identifier of the description text.
    :type description_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param choices: The choices to display in the dialog.
    :type choices: Iterator[SimPickerRow]
    :param title_tokens: Tokens to format into the title.
    :type title_tokens: Iterator[Any], optional
    :param description_tokens: Tokens to format into the description.
    :type description_tokens: Iterator[Any], optional
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
        choices: Iterator[SimPickerRow],
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=(),
        mod_identity: CommonModIdentity=None,
        required_tooltip: Union[int, str, LocalizedString, CommonStringId]=None,
        required_tooltip_tokens: Iterator[Any]=()
    ):
        super().__init__(
            title_identifier,
            description_identifier,
            choices,
            title_tokens=title_tokens,
            description_tokens=description_tokens,
            mod_identity=mod_identity,
            required_tooltip=required_tooltip,
            required_tooltip_tokens=required_tooltip_tokens
        )

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cl_choose_sims_dialog'

    def show(
        self,
        on_chosen: Callable[[Union[Tuple[Any], None], CommonChoiceOutcome], Any]=CommonFunctionUtils.noop,
        sim_info: SimInfo=None,
        should_show_names: bool=True,
        hide_row_descriptions: bool=False,
        column_count: int=3,
        min_selectable: int=1,
        max_selectable: int=1
    ):
        """show(\
            on_chosen=CommonFunctionUtils.noop,\
            sim_info=None,\
            should_show_names=True,\
            hide_row_descriptions=False,\
            column_count=3,\
            min_selectable=1,\
            max_selectable=1\
        )

        Show the dialog and invoke the callbacks upon the player submitting their selection.

        :param on_chosen: A callback invoked upon the player submitting their chosen Sims from the list. Default is CommonFunctionUtils.noop.
        :type on_chosen: Callable[[Union[Tuple[Any], None], CommonChoiceOutcome], Any], optional
        :param sim_info: The SimInfo of the Sim that will appear in the dialog image. The default Sim is the active Sim. Default is None.
        :type sim_info: SimInfo, optional
        :param should_show_names: If True, then the names of the Sims will display in the dialog. Default is True.
        :type should_show_names: bool, optional
        :param hide_row_descriptions: A flag to hide the row descriptions. Default is False.
        :type hide_row_descriptions: bool, optional
        :param column_count: The number of columns to display Sims in. Default is 3.
        :type column_count: int, optional
        :param min_selectable: The minimum number of Sims that must be chosen. Default is 1.
        :type min_selectable: int, optional
        :param max_selectable: The maximum number of Sims that can be chosen. Default is 1.
        :type max_selectable: int, optional
        :exception AssertionError: When something is wrong with the arguments or no rows were added to the dialog.
        :exception AttributeError: When Min or Max Selectable are invalid.
        """
        try:
            self._rows = tuple(sorted(self._rows, key=lambda row: CommonSimNameUtils.get_full_name(CommonSimUtils.get_sim_info(row.sim_id))))
            return self._show(
                on_chosen=on_chosen,
                sim_info=sim_info,
                should_show_names=should_show_names,
                hide_row_descriptions=hide_row_descriptions,
                column_count=column_count,
                min_selectable=min_selectable,
                max_selectable=max_selectable
            )
        except Exception as ex:
            self.log.error('show', exception=ex)

    def _show(
        self,
        on_chosen: Callable[[Union[Tuple[CommonDialogSimOption], None], CommonChoiceOutcome], Any]=CommonFunctionUtils.noop,
        sim_info: SimInfo=None,
        should_show_names: bool=True,
        hide_row_descriptions: bool=False,
        column_count: int=3,
        min_selectable: int=1,
        max_selectable: int=1
    ):
        _dialog = self.build_dialog(
            on_chosen=on_chosen,
            sim_info=sim_info,
            should_show_names=should_show_names,
            hide_row_descriptions=hide_row_descriptions,
            column_count=column_count,
            min_selectable=min_selectable,
            max_selectable=max_selectable
        )
        self.log.debug('Showing dialog.')
        _dialog.show_dialog()

    # noinspection PyMissingOrEmptyDocstring
    def build_dialog(
        self,
        on_chosen: Callable[[Union[Tuple[CommonDialogSimOption], None], CommonChoiceOutcome], Any]=CommonFunctionUtils.noop,
        sim_info: SimInfo=None,
        should_show_names: bool=True,
        hide_row_descriptions: bool=False,
        column_count: int=3,
        min_selectable: int=1,
        max_selectable: int=1
    ):
        if min_selectable < 1:
            raise AttributeError('\'min_selectable\' must be at least 1.')
        if max_selectable < min_selectable:
            raise AttributeError('\'max_selectable\' must be greater than \'min_selectable\'.')
        self.log.format_with_message('Attempting to display Sims choices.')
        _dialog = self._create_dialog(
            sim_info=sim_info,
            should_show_names=should_show_names,
            hide_row_descriptions=hide_row_descriptions,
            column_count=column_count,
            min_selectable=min_selectable,
            max_selectable=max_selectable
        )
        if _dialog is None:
            self.log.error('_dialog was None for some reason.')
            return

        if on_chosen is None:
            raise AssertionError('on_chosen was None.')

        if len(self.rows) == 0:
            raise AssertionError('No rows have been provided. Add rows to the dialog before attempting to display it.')

        def _on_chosen(dialog: UiSimPicker):
            if not dialog.accepted:
                self.log.debug('Dialog cancelled.')
                return on_chosen(None, CommonChoiceOutcome.CANCEL)
            choices = tuple(CommonDialogUtils.get_chosen_items(dialog))
            self.log.format_with_message('Choice made.', choice=choices)
            result = on_chosen(choices, CommonChoiceOutcome.CHOICE_MADE)
            self.log.format_with_message('Finished handling choice.', result=result)
            return result

        self.log.debug('Adding all choices')
        for row in self.rows:
            _dialog.add_row(row)

        _dialog.add_listener(_on_chosen)
        return _dialog


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.show_choose_sims_dialog',
    'Show an example of CommonChooseSimsDialog.'
)
def _common_testing_show_choose_sims_dialog(output: CommonConsoleCommandOutput):
    output('Showing test choose sims dialog.')

    def _on_chosen(choice: Union[Tuple[SimInfo], None], outcome: CommonChoiceOutcome):
        output('Chose {} with result: {}.'.format(CommonSimNameUtils.get_full_names(choice), pformat(outcome)))

    # LocalizedStrings within other LocalizedStrings
    title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
    description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
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
    output('Done showing.')
