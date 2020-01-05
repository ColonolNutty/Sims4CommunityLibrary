"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import sims4.commands
from typing import Any, Callable, Union, Iterator

from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog import UiDialogOk

log = CommonLogRegistry.get().register_log(ModInfo.get_identity().name, 's4cl_ok_dialog')


class CommonOkDialog:
    """
        Use to create an acknowledgement dialog.
    """
    def __init__(
        self,
        title_identifier: Union[int, LocalizedString],
        description_identifier: Union[int, LocalizedString],
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=(),
        ok_text_identifier: Union[int, LocalizedString]=CommonStringId.OK,
        ok_text_tokens: Iterator[Any]=()
    ):
        """
            Create a dialog with a single button: Ok
        :param title_identifier: A decimal identifier of the title text.
        :param description_identifier: A decimal identifier of the description text.
        :param title_tokens: Tokens to format into the title.
        :param description_tokens: Tokens to format into the description.
        :param ok_text_identifier: A decimal identifier for the Ok button text.
        :param ok_text_tokens: Tokens to format into the Ok button text.
        """
        self.title = CommonLocalizationUtils.create_localized_string(title_identifier, tokens=tuple(title_tokens))
        self.description = CommonLocalizationUtils.create_localized_string(description_identifier, tokens=tuple(description_tokens))
        self.ok_text = CommonLocalizationUtils.create_localized_string(ok_text_identifier, tokens=tuple(ok_text_tokens))

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name)
    def show(self, on_acknowledged: Callable[[UiDialogOk], Any]=CommonFunctionUtils.noop):
        """
            Show the dialog and invoke the callback upon the player acknowledging the dialog.
        :param on_acknowledged: Invoked upon the player acknowledging (Hitting Ok) or closing the dialog.
        """
        _dialog = self._create_dialog()
        if _dialog is None:
            return

        _dialog.add_listener(on_acknowledged)
        _dialog.show_dialog()

    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity().name, fallback_return=None)
    def _create_dialog(self) -> Union[UiDialogOk, None]:
        return UiDialogOk.TunableFactory().default(
            CommonSimUtils.get_active_sim_info(),
            text=lambda *_, **__: self.description,
            title=lambda *_, **__: self.title,
            text_ok=lambda *_, **__: self.ok_text
        )


@sims4.commands.Command('s4clib_testing.show_ok_dialog', command_type=sims4.commands.CommandType.Live)
def _common_testing_show_ok_dialog(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing test ok dialog.')

    def _on_acknowledged(_: UiDialogOk):
        if _.accepted:
            output('Ok option chosen.')
        else:
            output('Dialog closed.')

    try:
        # LocalizedStrings within other LocalizedStrings
        title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
        description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
        dialog = CommonOkDialog(CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                                      CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                                      title_tokens=title_tokens,
                                      description_tokens=description_tokens,
                                      ok_text_identifier=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_ONE, text_color=CommonLocalizedStringColor.RED))
        dialog.show(on_acknowledged=_on_acknowledged)
    except Exception as ex:
        log.format_error_with_message('Failed to show ok dialog', exception=ex)
        output('Failed to show ok dialog, please locate your exception log file.')
    output('Done showing.')
