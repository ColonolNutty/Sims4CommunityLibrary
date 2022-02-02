"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable, Union, Iterator

from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.dialogs.common_dialog import CommonDialog
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog import UiDialogOk


class CommonOkDialog(CommonDialog):
    """CommonOkDialog(\
        title_identifier,\
        description_identifier,\
        title_tokens=(),\
        description_tokens=(),\
        ok_text_identifier=CommonStringId.OK,\
        ok_text_tokens=(),
        mod_identity=None\
    )

    Use to create an acknowledgement dialog.

    .. note:: To see an example dialog, run the command :class:`s4clib_testing.show_ok_dialog` in the in-game console.

    .. highlight:: python
    .. code-block:: python

        def _common_testing_show_ok_dialog():

            def _on_acknowledged(_dialog: UiDialogOk):
                if _dialog.accepted:
                    pass
                else:
                    pass

            # LocalizedStrings within other LocalizedStrings
            title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
            description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
            dialog = CommonOkDialog(
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                title_tokens=title_tokens,
                description_tokens=description_tokens,
                ok_text_identifier=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_ONE, text_color=CommonLocalizedStringColor.RED)
            )
            dialog.show(on_acknowledged=_on_acknowledged)


    :param title_identifier: A decimal identifier of the title text.
    :type title_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param description_identifier: A decimal identifier of the description text.
    :type description_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param title_tokens: Tokens to format into the title.
    :type title_tokens: Iterator[Any], optional
    :param description_tokens: Tokens to format into the description.
    :type description_tokens: Iterator[Any], optional
    :param ok_text_identifier: A decimal identifier for the Ok button text.
    :type ok_text_identifier: Union[int, str, LocalizedString, CommonStringId], optional
    :param ok_text_tokens: Tokens to format into the Ok button text.
    :type ok_text_tokens: Iterator[Any], optional
    :param mod_identity: The identity of the mod creating the dialog. See :class:`.CommonModIdentity` for more information.
    :type mod_identity: CommonModIdentity, optional
    """
    def __init__(
        self,
        title_identifier: Union[int, str, LocalizedString, CommonStringId],
        description_identifier: Union[int, str, LocalizedString, CommonStringId],
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=(),
        ok_text_identifier: Union[int, str, LocalizedString, CommonStringId]=CommonStringId.OK,
        ok_text_tokens: Iterator[Any]=(),
        mod_identity: CommonModIdentity=None
    ):
        super().__init__(
            title_identifier,
            description_identifier,
            title_tokens=title_tokens,
            description_tokens=description_tokens,
            mod_identity=mod_identity
        )
        self.ok_text = CommonLocalizationUtils.create_localized_string(ok_text_identifier, tokens=tuple(ok_text_tokens))

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cl_ok_dialog'

    def show(
        self,
        on_acknowledged: Callable[[UiDialogOk], Any]=CommonFunctionUtils.noop
    ):
        """show(\
            on_acknowledged=CommonFunctionUtils.noop\
        )

        Show the dialog and invoke the callback upon the player acknowledging the dialog.

        :param on_acknowledged: Invoked upon the player acknowledging (Hitting Ok) or closing the dialog.
        :type on_acknowledged: Callable[[UiDialogOk], Any], optional
        """
        try:
            return self._show(
                on_acknowledged=on_acknowledged
            )
        except Exception as ex:
            self.log.error('show', exception=ex)

    def _show(
        self,
        on_acknowledged: Callable[[UiDialogOk], Any]=CommonFunctionUtils.noop
    ):
        self.log.format_with_message('Attempting to display dialog.')
        _dialog = self._create_dialog()
        if _dialog is None:
            self.log.debug('Failed to create dialog.')
            return

        _dialog.add_listener(on_acknowledged)
        self.log.debug('Displaying dialog.')
        _dialog.show_dialog()

    def _create_dialog(self) -> Union[UiDialogOk, None]:
        try:
            return UiDialogOk.TunableFactory().default(
                CommonSimUtils.get_active_sim_info(),
                text=lambda *_, **__: self.description,
                title=lambda *_, **__: self.title,
                text_ok=lambda *_, **__: self.ok_text
            )
        except Exception as ex:
            self.log.error('_create_dialog', exception=ex)
        return None


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.show_ok_dialog',
    'Show an example of CommonPurchaseObjectsDialog.'
)
def _common_testing_show_ok_dialog(output: CommonConsoleCommandOutput):
    output('Showing test ok dialog.')

    def _on_acknowledged(_dialog: UiDialogOk):
        if _dialog.accepted:
            output('Ok option chosen.')
        else:
            output('Dialog closed.')

    # LocalizedStrings within other LocalizedStrings
    title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
    description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
    dialog = CommonOkDialog(
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        title_tokens=title_tokens,
        description_tokens=description_tokens,
        ok_text_identifier=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_ONE, text_color=CommonLocalizedStringColor.RED)
    )
    dialog.show(on_acknowledged=_on_acknowledged)
    output('Done showing.')
