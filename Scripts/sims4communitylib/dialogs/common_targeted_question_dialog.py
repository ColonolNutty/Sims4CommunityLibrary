"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable, Union, Iterator

from event_testing.resolver import DoubleSimResolver
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_dialog import CommonDialog
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
from ui.ui_dialog import UiDialogOkCancel


class CommonTargetedQuestionDialog(CommonDialog):
    """CommonTargetedQuestionDialog(\
        question_text,\
        question_tokens=(),\
        ok_text_identifier=CommonStringId.OK,\
        ok_text_tokens=(),\
        cancel_text_identifier=CommonStringId.CANCEL,\
        cancel_text_tokens=(),\
        mod_identity=None\
    )

    A Sim to Sim question dialog.

    .. note:: To see an example dialog, run the command :class:`s4clib_testing.show_targeted_question_dialog` in the in-game console.

    .. highlight:: python
    .. code-block:: python

        def _common_testing_show_targeted_question_dialog():

            def _ok_chosen(_: UiDialogOkCancel):
                pass

            def _cancel_chosen(_: UiDialogOkCancel):
                pass

            # LocalizedStrings within other LocalizedStrings
            description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
            dialog = CommonTargetedQuestionDialog(
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                question_tokens=description_tokens,
                ok_text_identifier=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_ONE, text_color=CommonLocalizedStringColor.RED),
                cancel_text_identifier=CommonStringId.TESTING_TEST_BUTTON_TWO
            )
            dialog.show(
                CommonSimUtils.get_active_sim_info(),
                tuple(CommonSimUtils.get_sim_info_for_all_sims_generator())[0],
                on_ok_selected=_ok_chosen,
                on_cancel_selected=_cancel_chosen
            )


    :param question_text: A decimal identifier of the question text.
    :type question_text: Union[int, str, LocalizedString, CommonStringId]
    :param question_tokens: Tokens to format into the question text.
    :type question_tokens: Iterator[Any], optional
    :param ok_text_identifier: A decimal identifier for the Ok text.
    :type ok_text_identifier: Union[int, str, LocalizedString, CommonStringId], optional
    :param ok_text_tokens: Tokens to format into the Ok text.
    :type ok_text_tokens: Iterator[Any], optional
    :param cancel_text_identifier: A decimal identifier for the Cancel text.
    :type cancel_text_identifier: Union[int, str, LocalizedString, CommonStringId], optional
    :param cancel_text_tokens: Tokens to format into the Cancel text.
    :type cancel_text_tokens: Iterator[Any], optional
    :param mod_identity: The identity of the mod creating the dialog. See :class:`.CommonModIdentity` for more information.
    :type mod_identity: CommonModIdentity, optional
    """
    def __init__(
        self,
        question_text: Union[int, str, LocalizedString, CommonStringId],
        question_tokens: Iterator[Any]=(),
        ok_text_identifier: Union[int, str, LocalizedString, CommonStringId]=CommonStringId.OK,
        ok_text_tokens: Iterator[Any]=(),
        cancel_text_identifier: Union[int, str, LocalizedString, CommonStringId]=CommonStringId.CANCEL,
        cancel_text_tokens: Iterator[Any]=(),
        mod_identity: CommonModIdentity=None
    ):
        super().__init__(
            0,
            question_text,
            description_tokens=question_tokens,
            mod_identity=mod_identity
        )
        self.ok_text = CommonLocalizationUtils.create_localized_string(ok_text_identifier, tokens=tuple(ok_text_tokens))
        self.cancel_text = CommonLocalizationUtils.create_localized_string(cancel_text_identifier, tokens=tuple(cancel_text_tokens))

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cl_targeted_question_dialog'

    def show(
        self,
        sim_info: SimInfo,
        target_sim_info: SimInfo,
        on_ok_selected: Callable[[UiDialogOkCancel], Any]=CommonFunctionUtils.noop,
        on_cancel_selected: Callable[[UiDialogOkCancel], Any]=CommonFunctionUtils.noop
    ):
        """show(\
            sim_info,\
            target_sim_info,\
            on_ok_selected=CommonFunctionUtils.noop,\
            on_cancel_selected=CommonFunctionUtils.noop\
        )

        Show the dialog and invoke the callbacks upon the player making a choice.

        :param sim_info: The Sim that is the source of the question.
        :type sim_info: SimInfo
        :param target_sim_info: The Sim that is the target of the question.
        :type target_sim_info: SimInfo
        :param on_ok_selected: Invoked upon the player clicking the Ok button in the dialog.
        :type on_ok_selected: Callable[[UiDialogOkCancel], Any], optional
        :param on_cancel_selected: Invoked upon the player clicking the Cancel button in the dialog.
        :type on_cancel_selected: Callable[[UiDialogOkCancel], Any], optional
        """
        try:
            return self._show(
                sim_info,
                target_sim_info,
                on_ok_selected=on_ok_selected,
                on_cancel_selected=on_cancel_selected
            )
        except Exception as ex:
            self.log.error('show', exception=ex)

    def _show(
        self,
        sim_info: SimInfo,
        target_sim_info: SimInfo,
        on_ok_selected: Callable[[UiDialogOkCancel], bool]=CommonFunctionUtils.noop,
        on_cancel_selected: Callable[[UiDialogOkCancel], bool]=CommonFunctionUtils.noop
    ):
        self.log.format_with_message(
            'Attempting to display dialog.',
            sim=CommonSimNameUtils.get_full_name(sim_info),
            target=CommonSimNameUtils.get_full_name(target_sim_info)
        )
        _dialog = self._create_dialog(sim_info, target_sim_info)
        if _dialog is None:
            self.log.debug('Failed to create dialog.')
            return

        def _on_option_selected(dialog: UiDialogOkCancel) -> bool:
            try:
                self.log.debug('Option selected.')
                if dialog.accepted:
                    self.log.debug('Ok chosen.')
                    return on_ok_selected(dialog)
                self.log.debug('Cancel chosen.')
                return on_cancel_selected(dialog)
            except Exception as ex:
                self.log.error('Error occurred on choosing an option.', exception=ex)
            return False

        _dialog.add_listener(_on_option_selected)
        self.log.debug('Displaying dialog.')
        _dialog.show_dialog()

    def _create_dialog(
        self,
        sim_info: SimInfo,
        target_sim_info: SimInfo
    ) -> Union[UiDialogOkCancel, None]:
        try:
            return UiDialogOkCancel.TunableFactory().default(
                sim_info,
                text=lambda *_, **__: self.description,
                text_ok=lambda *_, **__: self.ok_text,
                text_cancel=lambda *_, **__: self.cancel_text,
                target_sim_id=CommonSimUtils.get_sim_id(target_sim_info),
                resolver=DoubleSimResolver(sim_info, target_sim_info)
            )
        except Exception as ex:
            self.log.error('_create_dialog', exception=ex)
        return None


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.show_targeted_question_dialog',
    'Show an example of CommonTargetedQuestionDialog.'
)
def _common_testing_show_targeted_question_dialog(output: CommonConsoleCommandOutput):
    output('Showing test targeted question dialog.')

    def _ok_chosen(_: UiDialogOkCancel):
        output('Ok option chosen.')

    def _cancel_chosen(_: UiDialogOkCancel):
        output('Cancel option chosen.')

    # LocalizedStrings within other LocalizedStrings
    description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
    dialog = CommonTargetedQuestionDialog(
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        question_tokens=description_tokens,
        ok_text_identifier=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_ONE, text_color=CommonLocalizedStringColor.RED),
        cancel_text_identifier=CommonStringId.TESTING_TEST_BUTTON_TWO
    )
    dialog.show(
        CommonSimUtils.get_active_sim_info(),
        tuple(CommonSimUtils.get_sim_info_for_all_sims_generator())[0],
        on_ok_selected=_ok_chosen,
        on_cancel_selected=_cancel_chosen
    )
    output('Done showing.')
