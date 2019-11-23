"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import math

import sims4.commands
from typing import Tuple, Any, Callable, Union

from pprint import pformat
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.utils.common_dialog_utils import CommonDialogUtils
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog_picker import UiObjectPicker, ObjectPickerRow

log = CommonLogRegistry.get().register_log(ModInfo.MOD_NAME, 'choose_object_dialog')


class CommonChooseObjectDialog:
    """
        Create a dialog that asks the player to make a choice.
    """
    def __init__(
        self,
        title_identifier: Union[int, LocalizedString],
        description_identifier: Union[int, LocalizedString],
        choices: Tuple[ObjectPickerRow],
        title_tokens: Tuple[Any]=(),
        description_tokens: Tuple[Any]=(),
        per_page: int=25
    ):
        """
            Create a dialog for displaying a list of objects.
        :param title_identifier: A decimal identifier of the title text.
        :param description_identifier: A decimal identifier of the description text.
        :param choices: The choices to display in the dialog.
        :param title_tokens: Tokens to format into the title.
        :param description_tokens: Tokens to format into the description.
        :param per_page: The number of rows to display per page. If the number of rows (including rows added after creation) exceeds this value, pagination will be added.
        """
        self.title = CommonLocalizationUtils.create_localized_string(title_identifier, tokens=title_tokens)
        self.description = CommonLocalizationUtils.create_localized_string(description_identifier, tokens=description_tokens)
        self._choices = choices
        if per_page <= 0:
            raise AssertionError('per_page must be greater than zero.')
        self._per_page = per_page

    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME)
    def add_row(self, choice: ObjectPickerRow):
        """
            Add a choice to the dialog.
        """
        self._choices += (choice,)

    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME)
    def show(
        self,
        on_chosen: Callable[[Any, CommonChoiceOutcome], Any]=CommonFunctionUtils.noop,
        picker_type: UiObjectPicker.UiObjectPickerObjectPickerType=UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT,
        page: int=1
    ):
        """
            Show the dialog and invoke the callbacks upon the player making a choice.
        :param on_chosen: A callback invoked upon the player choosing something from the list.
        :param picker_type: The layout of the dialog.
        :param page: The page to display. Ignored if there is only one page of choices.
        """
        log.format_with_message('Attempting to display choices.', page=page)
        _dialog = self._create_dialog(picker_type=picker_type)
        if _dialog is None:
            log.error('_dialog was None for some reason.')
            return

        if on_chosen is None:
            raise ValueError('on_chosen was None.')

        if len(self._choices) == 0:
            raise AssertionError('No rows have been provided. Add rows to the dialog before attempting to display it.')

        if page < 0:
            raise AssertionError('page cannot be less than zero.')

        @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME)
        def _on_chosen(dialog: UiObjectPicker):
            if not dialog.accepted:
                log.debug('Dialog cancelled.')
                return on_chosen(None, CommonChoiceOutcome.CANCEL)
            choice = CommonDialogUtils.get_chosen_item(dialog)
            if choice == 'S4CL_NEXT':
                log.debug('Next chosen.')
                self.show(on_chosen=on_chosen, picker_type=picker_type, page=page + 1)
                return True
            elif choice == 'S4CL_PREVIOUS':
                log.debug('Previous chosen.')
                self.show(on_chosen=on_chosen, picker_type=picker_type, page=page - 1)
                return True
            log.format_with_message('Choice made.', choice=choice)
            result = on_chosen(choice, CommonChoiceOutcome.CHOICE_MADE)
            log.format_with_message('Finished handling choice.', result=result)
            return result

        number_of_rows = len(self._choices)
        log.format(number_of_rows=number_of_rows, per_page=self._per_page)
        if number_of_rows > self._per_page:
            number_of_pages = math.ceil(number_of_rows / self._per_page)

            if page > number_of_pages:
                raise AssertionError('page was out of range. Number of Pages: {}, Requested Page: {}'.format(str(number_of_pages), str(page)))

            start_index = (page - 1) * self._per_page
            end_index = page * self._per_page
            log.format(start_index=start_index, end_index=end_index)
            current_choices = self._choices[start_index:end_index]
            log.format(current_rows=current_choices)
            for row in current_choices:
                _dialog.add_row(row)

            if page < number_of_pages:
                log.format_with_message('Adding Next.', page=page, number_of_pages=number_of_pages)
                next_choice = ObjectPickerRow(
                    option_id=len(self._choices) + 1,
                    name=CommonLocalizationUtils.create_localized_string(CommonStringId.NEXT),
                    row_description=None,
                    row_tooltip=None,
                    icon=CommonIconUtils.load_arrow_right_icon(),
                    tag='S4CL_NEXT'
                )
                _dialog.add_row(next_choice)
            else:
                log.format_with_message('Not adding Next.', page=page, number_of_pages=number_of_pages)
            if page > 1:
                log.format_with_message('Adding Previous.', page=page, number_of_pages=number_of_pages)
                previous_choice = ObjectPickerRow(
                    option_id=len(self._choices) + 2,
                    name=CommonLocalizationUtils.create_localized_string(CommonStringId.PREVIOUS),
                    row_description=None,
                    row_tooltip=None,
                    icon=CommonIconUtils.load_arrow_right_icon(),
                    tag='S4CL_PREVIOUS'
                )
                _dialog.add_row(previous_choice)
            else:
                log.format_with_message('Not adding Previous.', page=page)
        else:
            log.debug('Adding all choices')
            for row in self._choices:
                _dialog.add_row(row)

        _dialog.add_listener(_on_chosen)
        _dialog.show_dialog()

    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME, fallback_return=None)
    def _create_dialog(
        self,
        picker_type: UiObjectPicker.UiObjectPickerObjectPickerType=UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT
    ) -> Union[UiObjectPicker, None]:
        return UiObjectPicker.TunableFactory().default(
            CommonSimUtils.get_active_sim_info(),
            text=lambda *_, **__: self.description,
            title=lambda *_, **__: self.title,
            min_selectable=1,
            max_selectable=1,
            picker_type=picker_type
        )


@sims4.commands.Command('s4clib_testing.show_choose_object_dialog', command_type=sims4.commands.CommandType.Live)
def _common_testing_show_choose_object_dialog(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing test choose object dialog.')

    def _on_chosen(choice: str, outcome: CommonChoiceOutcome):
        output('Chose {} with result: {}.'.format(pformat(choice), pformat(outcome)))

    try:
        # LocalizedStrings within other LocalizedStrings
        title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
        description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
        from sims4communitylib.utils.common_icon_utils import CommonIconUtils
        options = [
            ObjectPickerRow(
                option_id=1,
                name=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING),
                row_description=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_ONE),
                row_tooltip=None,
                icon=CommonIconUtils.load_checked_square_icon(),
                tag='Value 1'
            ),
            ObjectPickerRow(
                option_id=2,
                name=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING),
                row_description=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_TWO),
                row_tooltip=None,
                icon=CommonIconUtils.load_arrow_navigate_into_icon(),
                tag='Value 2'
            ),
            ObjectPickerRow(
                option_id=3,
                name=CommonLocalizationUtils.create_localized_string('Value 3'),
                row_description=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_TWO),
                row_tooltip=None,
                icon=CommonIconUtils.load_arrow_navigate_into_icon(),
                tag='Value 3'
            )
        ]
        dialog = CommonChooseObjectDialog(
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            tuple(options),
            title_tokens=title_tokens,
            description_tokens=description_tokens,
            per_page=2
        )
        dialog.show(on_chosen=_on_chosen, keep_open_after_choice=True)
    except Exception as ex:
        log.format_error_with_message('Failed to show dialog', exception=ex)
        output('Failed to show dialog, please locate your exception log file.')
    output('Done showing.')
