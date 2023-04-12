"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable, Union, Iterator, Dict

from pprint import pformat
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs._common_ui_dialog_multi_text_input_ok_cancel import _CommonUiDialogMultiTextInputOkCancel
from sims4communitylib.dialogs._common_ui_dialog_text_input_ok_cancel import _CommonUiDialogTextInputOkCancel
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_dialog import CommonDialog
from sims4communitylib.dialogs.common_input_text_field import CommonInputTextField
from sims4communitylib.enums.common_character_restrictions import CommonCharacterRestriction
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog_generic import UiDialogTextInput


class CommonInputMultiTextDialog(CommonDialog):
    """CommonInputMultiTextDialog(\
        mod_identity,\
        title_identifier,\
        description_identifier,\
        input_fields,\
        title_tokens=(),\
        description_tokens=()\
    )

    Create a dialog that prompts the player to enter a text value.

    .. note:: To see an example dialog, run the command :class:`s4clib_testing.show_input_multi_text_dialog` in the in-game console.

    .. highlight:: python
    .. code-block:: python

        def _common_testing_show_input_text_dialog():

            def _on_submit(input_value: str, outcome: CommonChoiceOutcome):
                pass

            # LocalizedStrings within other LocalizedStrings
            title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
            description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
            from sims4communitylib.utils.common_icon_utils import CommonIconUtils
            dialog = CommonInputMultiTextDialog(
                ModInfo.get_identity(),
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                (
                  CommonInputTextField('first_input_field', 'initial_text', title='First Input', default_text='default text stuff'),
                  CommonInputTextField('input_box_two', 'initial_text_two', default_text=CommonStringId.TESTING_TEST_TEXT_NO_TOKENS),
                  CommonInputTextField('input_box_three', 'initial_text_three', title='Numbers Only', character_restriction=CommonCharacterRestriction.NUMBERS_ONLY)
                ),
                title_tokens=title_tokens,
                description_tokens=description_tokens
            )
            dialog.show(on_submit=_on_submit)

    :param mod_identity: The identity of the mod creating the dialog. See :class:`.CommonModIdentity` for more information.
    :type mod_identity: CommonModIdentity
    :param title_identifier: A decimal identifier of the title text.
    :type title_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param description_identifier: A decimal identifier of the description text.
    :type description_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param input_fields: An iterator of input fields to display in the dialog.
    :type input_fields: Iterator[CommonInputTextField]
    :param title_tokens: Tokens to format into the title.
    :type title_tokens: Iterator[Any], optional
    :param description_tokens: Tokens to format into the description.
    :type description_tokens: Iterator[Any], optional
    """
    def __init__(
        self,
        mod_identity: CommonModIdentity,
        title_identifier: Union[int, str, LocalizedString, CommonStringId],
        description_identifier: Union[int, str, LocalizedString, CommonStringId],
        input_fields: Iterator[CommonInputTextField],
        title_tokens: Iterator[Any] = (),
        description_tokens: Iterator[Any] = ()
    ):
        super().__init__(
            title_identifier,
            description_identifier,
            title_tokens=title_tokens,
            description_tokens=description_tokens,
            mod_identity=mod_identity
        )
        self.input_fields = input_fields

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cl_input_text_dialog'

    def show(
        self,
        sim_info: SimInfo = None,
        on_submit: Callable[[Dict[str, str], CommonChoiceOutcome], Any] = CommonFunctionUtils.noop
    ) -> None:
        """show(\
            sim_info=None,\
            on_submit=CommonFunctionUtils.noop\
        )

        Show the dialog and invoke the callbacks upon the player submitting a value.

        :param sim_info: The Sim that owns the dialog. Set to None to use the Active Sim. Default is None.
        :type sim_info: SimInfo, optional
        :param on_submit: A callback invoked upon the player submitting a value. Default is CommonFunctionUtils.noop.
        :type on_submit: Callable[[Union[str, None], CommonChoiceOutcome], Any], optional
        """
        try:
            return self._show(
                sim_info=sim_info,
                on_submit=on_submit
            )
        except Exception as ex:
            self.log.error('show', exception=ex)

    def _show(
        self,
        sim_info: SimInfo = None,
        on_submit: Callable[[Dict[str, str], CommonChoiceOutcome], bool] = CommonFunctionUtils.noop
    ) -> None:
        self.log.debug('Attempting to display input text dialog.')

        if on_submit is None:
            raise ValueError('\'on_submit\' was None.')

        _dialog = self._create_dialog(sim_info=sim_info)
        if _dialog is None:
            self.log.error('_dialog was None for some reason.')
            return

        # noinspection PyBroadException
        def _on_submit(dialog: UiDialogTextInput) -> None:
            try:
                input_values = dict(dialog.text_input_responses)
                if not input_values or not dialog.accepted:
                    self.log.debug('Dialog cancelled.')
                    on_submit(dict(), CommonChoiceOutcome.CANCEL)
                    return
                self.log.format_with_message('Values entered.', input_values=input_values)
                result = on_submit(input_values, CommonChoiceOutcome.CHOICE_MADE)
                self.log.format_with_message('Finished handling input.', result=result)
            except Exception as ex:
                self.log.error('Error occurred on submitting values.', exception=ex)

        _dialog.add_listener(_on_submit)
        if self.input_fields is not None:
            _dialog.show_dialog(additional_tokens=tuple([input_field.initial_value for input_field in self.input_fields]))
        else:
            _dialog.show_dialog()

    def _create_dialog(self, sim_info: SimInfo = None) -> Union[_CommonUiDialogTextInputOkCancel, None]:
        try:
            return _CommonUiDialogMultiTextInputOkCancel.TunableFactory().default(
                sim_info or CommonSimUtils.get_active_sim_info(),
                self.input_fields,
                text=lambda *_, **__: self.description,
                title=lambda *_, **__: self.title
            )
        except Exception as ex:
            self.log.error('_create_dialog', exception=ex)
        return None


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.show_input_multi_text_dialog',
    'Show an example of CommonInputMultiTextDialog.'
)
def _common_testing_show_input_multi_text_dialog(output: CommonConsoleCommandOutput):
    output('Showing test input multi text dialog.')

    def _on_chosen(input_values: Dict[str, str], outcome: CommonChoiceOutcome):
        for (input_name, input_value) in input_values.items():
            output('Input {} Value {} with result: {}.'.format(pformat(input_name), pformat(input_value), pformat(outcome)))
        output('Done printing inputs.')

    # LocalizedStrings within other LocalizedStrings
    title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
    description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
    dialog = CommonInputMultiTextDialog(
        ModInfo.get_identity(),
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        (
          CommonInputTextField('first_input_field', 'initial_text', title='First Input', default_text='default text stuff'),
          CommonInputTextField('input_box_two', 'initial_text_two', default_text=CommonStringId.TESTING_TEST_TEXT_NO_TOKENS),
          CommonInputTextField('input_box_three', 'initial_text_three', title='Numbers Only', character_restriction=CommonCharacterRestriction.NUMBERS_ONLY)
        ),
        title_tokens=title_tokens,
        description_tokens=description_tokens
    )
    dialog.show(on_submit=_on_chosen)
    output('Done showing.')
