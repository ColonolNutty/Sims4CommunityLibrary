"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import sims4.commands
from typing import Tuple, Any, Callable, Union, Iterator

from pprint import pformat
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_dialog import CommonDialog
from sims4communitylib.dialogs.utils.common_dialog_utils import CommonDialogUtils
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog_generic import UiDialogTextInputOkCancel, UiDialogTextInput
from sims4communitylib.modinfo import ModInfo


class _CommonUiDialogTextInputOkCancel(UiDialogTextInputOkCancel):
    def __init__(
        self,
        sim_info: SimInfo,
        *args,
        title: Callable[..., LocalizedString]=None,
        text: Callable[..., LocalizedString]=None,
        **kwargs
    ):
        super().__init__(
            sim_info,
            *args,
            title=title,
            text=text,
            **kwargs
        )
        self.text_input_responses = {}

    def on_text_input(self, text_input_name: str='', text_input: str='') -> bool:
        """A callback that occurs upon text being entered.

        """
        self.text_input_responses[text_input_name] = text_input
        return False

    def build_msg(self, text_input_overrides=None, additional_tokens: Tuple[Any]=(), **kwargs):
        """Build the message.

        """
        msg = super().build_msg(additional_tokens=(), **kwargs)
        text_input_msg = msg.text_input.add()
        text_input_msg.text_input_name = 'text_input'
        if additional_tokens and additional_tokens[0] is not None:
            text_input_msg.initial_value = CommonLocalizationUtils.create_localized_string(additional_tokens[0])
        return msg


class CommonInputFloatDialog(CommonDialog):
    """CommonInputFloatDialog(\
        title_identifier,\
        description_identifier,\
        initial_value,\
        min_value=0.0,\
        max_value=2147483647.0,\
        title_tokens=(),\
        description_tokens=(),\
        mod_identity=None\
    )

    Create a dialog that prompts the player to enter a float value.

    .. note:: To see an example dialog, run the command :class:`s4clib_testing.show_input_float_dialog` in the in-game console.

    .. highlight:: python
    .. code-block:: python

        def _common_testing_show_input_float_dialog():

            def _on_chosen(choice: float, outcome: CommonChoiceOutcome):
                pass

            # LocalizedStrings within other LocalizedStrings
            title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
            description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
            from sims4communitylib.utils.common_icon_utils import CommonIconUtils
            dialog = CommonInputFloatDialog(
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                2.0,
                title_tokens=title_tokens,
                description_tokens=description_tokens
            )
            dialog.show(on_submit=_on_chosen)

    :param title_identifier: A decimal identifier of the title text.
    :type title_identifier: Union[int, LocalizedString]
    :param description_identifier: A decimal identifier of the description text.
    :type description_identifier: Union[int, LocalizedString]
    :param initial_value: The initial value that will appear in the input box.
    :type initial_value: float
    :param min_value: The minimum value allowed to be entered by the player. Default is 0.0
    :type min_value: float, optional
    :param max_value: The maximum value allowed to be entered by the player. Default is Max Int.
    :type max_value: float, optional
    :param title_tokens: Tokens to format into the title.
    :type title_tokens: Iterator[Any], optional
    :param description_tokens: Tokens to format into the description.
    :type description_tokens: Iterator[Any], optional
    :param mod_identity: The identity of the mod creating the dialog. See :class:`.CommonModIdentity` for more information.
    :type mod_identity: CommonModIdentity, optional
    """
    def __init__(
        self,
        title_identifier: Union[int, LocalizedString],
        description_identifier: Union[int, LocalizedString],
        initial_value: float,
        min_value: float=0.0,
        max_value: float=2147483647.0,
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
        return 's4cl_input_float_dialog'

    def show(
        self,
        on_submit: Callable[[Union[float, None], CommonChoiceOutcome], Any]=CommonFunctionUtils.noop
    ):
        """show(\
            on_submit=CommonFunctionUtils.noop\
        )

        Show the dialog and invoke the callbacks upon the player submitting a value.

        :param on_submit: A callback invoked upon the player submitting a value. Default is CommonFunctionUtils.noop.
        :type on_submit: Callable[[Union[float, None], CommonChoiceOutcome], Any], optional
        """
        try:
            return self._show(
                on_submit=on_submit
            )
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'show', exception=ex)

    def _show(
        self,
        on_submit: Callable[[Union[float, None], CommonChoiceOutcome], Any]=CommonFunctionUtils.noop
    ):
        self.log.debug('Attempting to display input float dialog.')

        if on_submit is None:
            raise ValueError('\'on_submit\' was None.')

        _dialog = self._create_dialog()
        if _dialog is None:
            self.log.error('_dialog was None for some reason.')
            return

        # noinspection PyBroadException
        @CommonExceptionHandler.catch_exceptions(self.mod_identity.name)
        def _on_submit(dialog: UiDialogTextInput):
            input_value = CommonDialogUtils.get_input_value(dialog)
            if not input_value or not dialog.accepted:
                self.log.debug('Dialog cancelled.')
                return on_submit(None, CommonChoiceOutcome.CANCEL)
            self.log.format_with_message('Value entered, attempting to convert it to a float.', value=input_value)

            try:
                input_value = float(input_value)
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

        _dialog.add_listener(_on_submit)
        if self.initial_value is not None:
            _dialog.show_dialog(additional_tokens=(self.initial_value,))
        else:
            _dialog.show_dialog()

    def _create_dialog(self) -> Union[_CommonUiDialogTextInputOkCancel, None]:
        try:
            return _CommonUiDialogTextInputOkCancel.TunableFactory().default(
                CommonSimUtils.get_active_sim_info(),
                text=lambda *_, **__: self.description,
                title=lambda *_, **__: self.title
            )
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, '_create_dialog', exception=ex)
        return None


@sims4.commands.Command('s4clib_testing.show_input_float_dialog', command_type=sims4.commands.CommandType.Live)
def _common_testing_show_input_float_dialog(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing test input float dialog.')

    def _on_chosen(choice: float, outcome: CommonChoiceOutcome):
        output('Chose {} with result: {}.'.format(pformat(choice), pformat(outcome)))

    try:
        # LocalizedStrings within other LocalizedStrings
        title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
        description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
        from sims4communitylib.utils.common_icon_utils import CommonIconUtils
        dialog = CommonInputFloatDialog(
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            2.0,
            title_tokens=title_tokens,
            description_tokens=description_tokens
        )
        dialog.show(on_submit=_on_chosen)
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to show dialog', exception=ex)
        output('Failed to show dialog, please locate your exception log file.')
    output('Done showing.')
