"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable, Union, Iterator

from pprint import pformat
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs._common_ui_dialog_text_input_ok_cancel import _CommonUiDialogTextInputOkCancel
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_dialog import CommonDialog
from sims4communitylib.dialogs.utils.common_dialog_utils import CommonDialogUtils
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog_generic import UiDialogTextInput
from sims4communitylib.modinfo import ModInfo


class CommonInputIntegerDialog(CommonDialog):
    """CommonInputIntegerDialog(\
        title_identifier,\
        description_identifier,\
        initial_value,\
        min_value=0,\
        max_value=2147483647,\
        title_tokens=(),\
        description_tokens=(),\
        mod_identity=None\
    )

    Create a dialog that prompts the player to enter an integer value.

    .. note:: To see an example dialog, run the command :class:`s4clib_testing.show_input_integer_dialog` in the in-game console.

    .. highlight:: python
    .. code-block:: python

        def _common_testing_show_input_integer_dialog():

            def _on_submit(input_value: integer, outcome: CommonChoiceOutcome):
                pass

            # LocalizedStrings within other LocalizedStrings
            title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
            description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
            from sims4communitylib.utils.common_icon_utils import CommonIconUtils
            dialog = CommonInputIntegerDialog(
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                2,
                title_tokens=title_tokens,
                description_tokens=description_tokens
            )
            dialog.show(on_submit=_on_submit)

    :param title_identifier: A decimal identifier of the title text.
    :type title_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param description_identifier: A decimal identifier of the description text.
    :type description_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param initial_value: The initial value that will appear in the input box.
    :type initial_value: int
    :param min_value: The minimum value allowed to be entered by the player. Default is 0.0
    :type min_value: int, optional
    :param max_value: The maximum value allowed to be entered by the player. Default is Max Int.
    :type max_value: int, optional
    :param title_tokens: Tokens to format into the title.
    :type title_tokens: Iterator[Any], optional
    :param description_tokens: Tokens to format into the description.
    :type description_tokens: Iterator[Any], optional
    :param mod_identity: The identity of the mod creating the dialog. See :class:`.CommonModIdentity` for more information.
    :type mod_identity: CommonModIdentity, optional
    """
    def __init__(
        self,
        title_identifier: Union[int, str, LocalizedString, CommonStringId],
        description_identifier: Union[int, str, LocalizedString, CommonStringId],
        initial_value: int,
        min_value: int=0,
        max_value: int=2147483647,
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=(),
        mod_identity: CommonModIdentity=None
    ):
        super().__init__(
            title_identifier,
            description_identifier,
            title_tokens=title_tokens,
            description_tokens=description_tokens,
            mod_identity=mod_identity
        )
        self.initial_value = initial_value
        self.min_value = min_value
        self.max_value = max_value

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cl_input_integer_dialog'

    def show(
        self,
        sim_info: SimInfo=None,
        on_submit: Callable[[Union[int, None], CommonChoiceOutcome], Any]=CommonFunctionUtils.noop
    ):
        """show(\
            sim_info=None,\
            on_submit=CommonFunctionUtils.noop\
        )

        Show the dialog and invoke the callbacks upon the player submitting a value.

        :param sim_info: The Sim that owns the dialog. Set to None to use the Active Sim. Default is None.
        :type sim_info: SimInfo, optional
        :param on_submit: A callback invoked upon the player submitting a value. Default is CommonFunctionUtils.noop.
        :type on_submit: Callable[[Union[int, None], CommonChoiceOutcome], Any], optional
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
        sim_info: SimInfo=None,
        on_submit: Callable[[Union[int, None], CommonChoiceOutcome], bool]=CommonFunctionUtils.noop
    ):
        self.log.debug('Attempting to display input integer dialog.')

        if on_submit is None:
            raise ValueError('\'on_submit\' was None.')

        _dialog = self._create_dialog(sim_info=sim_info)
        if _dialog is None:
            self.log.error('_dialog was None for some reason.')
            return

        # noinspection PyBroadException
        def _on_submit(dialog: UiDialogTextInput) -> bool:
            try:
                input_value = CommonDialogUtils.get_input_value(dialog)
                if not input_value or not dialog.accepted:
                    self.log.debug('Dialog cancelled.')
                    return on_submit(None, CommonChoiceOutcome.CANCEL)
                self.log.format_with_message('Value entered, attempting to convert it to an integer.', value=input_value)

                try:
                    input_value = int(input_value)
                    self.log.debug('Conversion successful.')
                    input_value = max(self.min_value, input_value)
                    input_value = min(self.max_value, input_value)
                except:
                    self.log.format_with_message('Failed to convert value', value=input_value)
                    return on_submit(None, CommonChoiceOutcome.ERROR)

                self.log.format_with_message('Value entered.', input_value=input_value)
                result = on_submit(input_value, CommonChoiceOutcome.CHOICE_MADE)
                self.log.format_with_message('Finished handling input.', result=result)
                return result
            except Exception as ex:
                self.log.error('Error occurred on submitting a value.', exception=ex)
            return False

        _dialog.add_listener(_on_submit)
        if self.initial_value is not None:
            _dialog.show_dialog(additional_tokens=(self.initial_value,))
        else:
            _dialog.show_dialog()

    def _create_dialog(self, sim_info: SimInfo=None) -> Union[_CommonUiDialogTextInputOkCancel, None]:
        try:
            return _CommonUiDialogTextInputOkCancel.TunableFactory().default(
                sim_info or CommonSimUtils.get_active_sim_info(),
                text=lambda *_, **__: self.description,
                title=lambda *_, **__: self.title
            )
        except Exception as ex:
            self.log.error('_create_dialog', exception=ex)
        return None


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.show_input_integer_dialog',
    'Show an example of CommonInputIntegerDialog.'
)
def _common_testing_show_input_integer_dialog(output: CommonConsoleCommandOutput):
    output('Showing test input integer dialog.')

    def _on_submit(input_value: int, outcome: CommonChoiceOutcome):
        output('Input {} with result: {}.'.format(pformat(input_value), pformat(outcome)))

    # LocalizedStrings within other LocalizedStrings
    title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
    description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
    dialog = CommonInputIntegerDialog(
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        2,
        title_tokens=title_tokens,
        description_tokens=description_tokens
    )
    dialog.show(on_submit=_on_submit)
    output('Done showing.')
