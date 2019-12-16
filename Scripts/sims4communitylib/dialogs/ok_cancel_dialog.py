"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import sims4.commands
from typing import Tuple, Any, Callable, Union

from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog import UiDialogOkCancel
log = CommonLogRegistry.get().register_log(ModInfo.get_identity().name, 'ok_cancel_dialog')


class CommonOkCancelDialog:
    """
        Use to create a prompt dialog.
    """
    def __init__(self,
                 title_identifier: Union[int, LocalizedString],
                 description_identifier: Union[int, LocalizedString],
                 title_tokens: Tuple[Any]=(),
                 description_tokens: Tuple[Any]=(),
                 ok_text_identifier: Union[int, LocalizedString]=CommonStringId.OK,
                 ok_text_tokens: Tuple[Any]=(),
                 cancel_text_identifier: Union[int, LocalizedString]=CommonStringId.CANCEL,
                 cancel_text_tokens: Tuple[Any]=()):
        """
            Create a dialog with two buttons: Ok and Cancel.
        :param title_identifier: A decimal identifier of the title text.
        :param description_identifier: A decimal identifier of the description text.
        :param title_tokens: Tokens to format into the title.
        :param description_tokens: Tokens to format into the description.
        :param ok_text_identifier: A decimal identifier for the Ok text.
        :param ok_text_tokens: Tokens to format into the Ok text.
        :param cancel_text_identifier: A decimal identifier for the Cancel text.
        :param cancel_text_tokens: Tokens to format into the Cancel text.
        """
        self.title = CommonLocalizationUtils.create_localized_string(title_identifier, tokens=title_tokens)
        self.description = CommonLocalizationUtils.create_localized_string(description_identifier, tokens=description_tokens)
        self.ok_text = CommonLocalizationUtils.create_localized_string(ok_text_identifier, tokens=ok_text_tokens)
        self.cancel_text = CommonLocalizationUtils.create_localized_string(cancel_text_identifier, tokens=cancel_text_tokens)

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name)
    def show(self, on_ok_selected: Callable[[UiDialogOkCancel], Any]=CommonFunctionUtils.noop, on_cancel_selected: Callable[[UiDialogOkCancel], Any]=CommonFunctionUtils.noop):
        """
            Show the dialog and invoke the callbacks upon the player selecting an option.
        :param on_ok_selected: Invoked upon the player selecting Ok in the dialog.
        :param on_cancel_selected: Invoked upon the player selecting Cancel in the dialog.
        """
        _dialog = self._create_dialog()
        if _dialog is None:
            return

        def _on_option_selected(dialog: UiDialogOkCancel):
            if dialog.accepted:
                return on_ok_selected(dialog)
            return on_cancel_selected(dialog)

        _dialog.add_listener(_on_option_selected)
        _dialog.show_dialog()

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=None)
    def _create_dialog(self) -> Union[UiDialogOkCancel, None]:
        return UiDialogOkCancel.TunableFactory().default(CommonSimUtils.get_active_sim_info(),
                                                         text=lambda *_, **__: self.description,
                                                         title=lambda *_, **__: self.title,
                                                         text_ok=lambda *_, **__: self.ok_text,
                                                         text_cancel=lambda *_, **__: self.cancel_text)


@sims4.commands.Command('s4clib_testing.show_ok_cancel_dialog', command_type=sims4.commands.CommandType.Live)
def _common_testing_show_ok_cancel_dialog(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing test ok cancel dialog.')

    def _ok_chosen(_: UiDialogOkCancel):
        output('Ok option chosen.')

    def _cancel_chosen(_: UiDialogOkCancel):
        output('Cancel option chosen.')

    try:
        # LocalizedStrings within other LocalizedStrings
        title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
        description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
        dialog = CommonOkCancelDialog(CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                                      CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                                      title_tokens=title_tokens,
                                      description_tokens=description_tokens,
                                      ok_text_identifier=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_ONE, text_color=CommonLocalizedStringColor.RED),
                                      cancel_text_identifier=CommonStringId.TESTING_TEST_BUTTON_TWO)
        dialog.show(on_ok_selected=_ok_chosen, on_cancel_selected=_cancel_chosen)
    except Exception as ex:
        log.format_error_with_message('Failed to show ok cancel dialog', exception=ex)
        output('Failed to show ok cancel dialog, please locate your exception log file.')
    output('Done showing.')
