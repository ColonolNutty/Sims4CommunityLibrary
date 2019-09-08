"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import sims4.commands
from typing import Tuple, Any, Callable, Union

from pprint import pformat
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.dialogs.utils.common_dialog_utils import CommonDialogUtils
from sims4communitylib.enums.enumtypes.int_enum import CommonEnumIntBase
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog import UiDialogOkCancel
from ui.ui_dialog_picker import UiObjectPicker, ObjectPickerRow

log = CommonLogRegistry.get().register_log(ModInfo.MOD_NAME, 'choose_item_dialog')


class CommonChooseItemResult(CommonEnumIntBase):
    """ Different outcomes upon the player choosing or not choosing items in the dialog. """
    DIALOG_CANCELLED = 0
    ITEM_CHOSEN = 1
    ITEM_CHOSEN_WITH_ERROR = 2

    @staticmethod
    def is_error(result: 'CommonChooseItemResult'):
        """ Determine whether a result is an error or not. """
        return result == CommonChooseItemResult.DIALOG_CANCELLED or result == CommonChooseItemResult.ITEM_CHOSEN_WITH_ERROR


class CommonChooseItemDialog:
    """
        Use to create a dialog that prompts the player to choose a single item from a list of items.
    """
    def __init__(self,
                 title_identifier: Union[int, LocalizedString],
                 description_identifier: Union[int, LocalizedString],
                 list_items: Tuple[ObjectPickerRow],
                 title_tokens: Tuple[Any]=(),
                 description_tokens: Tuple[Any]=()):
        """
            Create a dialog displaying a list of items to choose from.
        :param title_identifier: A decimal identifier of the title text.
        :param description_identifier: A decimal identifier of the description text.
        :param list_items: The items to display in the dialog.
        :param title_tokens: Tokens to format into the title.
        :param description_tokens: Tokens to format into the description.
        """
        self.title = CommonLocalizationUtils.create_localized_string(title_identifier, tokens=title_tokens)
        self.description = CommonLocalizationUtils.create_localized_string(description_identifier, tokens=description_tokens)
        self.list_items = list_items

    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME)
    def add_item(self, item: ObjectPickerRow):
        """
            Add a new item to choose from.
        :param item: The item to add.
        """
        self.list_items += (item,)

    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME)
    def show(self, on_item_chosen: Callable[[Any, CommonChooseItemResult], Any]=CommonFunctionUtils.noop):
        """
            Show the dialog and invoke the callbacks upon the player selecting an item.
        :param on_item_chosen: Invoked upon the player choosing an item from the list.
        """
        _dialog = self._create_dialog()
        if _dialog is None:
            return

        def _on_item_chosen(dialog: UiDialogOkCancel):
            if not dialog.accepted:
                return on_item_chosen(None, CommonChooseItemResult(CommonChooseItemResult.DIALOG_CANCELLED))
            chosen_item = CommonDialogUtils.get_chosen_item(dialog)
            return on_item_chosen(chosen_item, CommonChooseItemResult(CommonChooseItemResult.ITEM_CHOSEN))

        for list_item in self.list_items:
            _dialog.add_row(list_item)

        _dialog.add_listener(_on_item_chosen)
        _dialog.show_dialog()

    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME, fallback_return=None)
    def _create_dialog(self) -> Union[UiObjectPicker, None]:
        return UiObjectPicker.TunableFactory().default(CommonSimUtils.get_active_sim_info(),
                                                       text=lambda *_, **__: self.description,
                                                       title=lambda *_, **__: self.title,
                                                       min_selectable=1,
                                                       max_selectable=1,
                                                       picker_type=UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT)


@sims4.commands.Command('s4clib_testing.show_choose_item_dialog', command_type=sims4.commands.CommandType.Live)
def _common_testing_show_choose_item_dialog(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing test choose item dialog.')

    def _item_chosen(chosen_item: str, result: CommonChooseItemResult):
        output('Item chosen {} with result: {}.'.format(pformat(chosen_item), pformat(result)))

    try:
        # LocalizedStrings within other LocalizedStrings
        title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
        description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
        options = [ObjectPickerRow(option_id=1, name=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING),
                                   row_description=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_ONE), row_tooltip=None, icon=None,
                                   tag='Value 1'),
                   ObjectPickerRow(option_id=2, name=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING),
                                   row_description=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_TWO), row_tooltip=None, icon=None,
                                   tag='Value 2')]
        dialog = CommonChooseItemDialog(CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                                        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                                        tuple(options),
                                        title_tokens=title_tokens,
                                        description_tokens=description_tokens)
        dialog.show(on_item_chosen=_item_chosen)
    except Exception as ex:
        log.format_error_with_message('Failed to show dialog', exception=ex)
        output('Failed to show dialog, please locate your exception log file.')
    output('Done showing.')
