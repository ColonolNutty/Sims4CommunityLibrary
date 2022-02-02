"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.dialogs.common_ui_dialog_response import CommonUiDialogResponse
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from ui.ui_dialog import UiDialog, UiDialogOption
from typing import Tuple, Any, Iterator

from event_testing.resolver import Resolver
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonUiResponseDialog(UiDialog, HasClassLog):
    """CommonUiResponseDialog(owner, responses, *args, resolver=None, target_sim_id=None, dialog_options=UiDialogOption.DISABLE_CLOSE_BUTTON, **kwargs)

    A dialog that displays various responses for the player to choose from.

    :param owner: The owner of the dialog.
    :type owner: Any
    :param responses: An iteration of responses the player may choose.
    :type responses: Iterator[CommonUiDialogResponse]
    :param resolver: A resolver used to determine the display name of responses. Default is None.
    :type resolver: Resolver, optional
    :param target_sim_id: The Sim Id of the Target the response is directed at. Default is None.
    :type target_sim_id: int, optional
    :param dialog_options: Flags used to change how the dialog appears or functions. Default is UiDialogOption.DISABLE_CLOSE_BUTTON.
    :type dialog_options: UiDialogOption, optional
    """
    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_ui_response_dialog'

    def __init__(
        self,
        owner: Any,
        responses: Iterator[CommonUiDialogResponse],
        *args,
        resolver: Resolver=None,
        target_sim_id: int=None,
        dialog_options: UiDialogOption=UiDialogOption.DISABLE_CLOSE_BUTTON,
        **kwargs
    ):
        super().__init__(
            owner,
            *args,
            resolver=resolver,
            target_sim_id=target_sim_id,
            dialog_options=dialog_options,
            **kwargs
        )
        HasClassLog.__init__(self)
        self._response_value = None
        self._responses = tuple(responses)

    @property
    def accepted(self) -> bool:
        """Whether or not a response was chosen."""
        return self.response != CommonUiResponseDialog._PREVIOUS_BUTTON_ID and self.response != CommonUiResponseDialog._NEXT_BUTTON_ID

    @property
    def cancelled(self) -> bool:
        """Whether not the dialog was cancelled."""
        return self.response < 0

    def add_response(self, response: CommonUiDialogResponse):
        """add_response(response)

        Add a response to the dialog.

        :param response: The response to add.
        :type response: CommonUiDialogResponse
        """
        self._responses += (response,)

    def get_response(self) -> Any:
        """Retrieve the chosen response. If there is one."""
        return self.response

    def get_response_value(self) -> Any:
        """Retrieve the chosen response value. If there is one."""
        return self._response_value

    def respond(self, chosen_response: int) -> bool:
        """When the player makes a choice, this function is invoked."""
        try:
            self.log.format_with_message('Chosen response', response=chosen_response)
            self.response = chosen_response
            if chosen_response < 0:
                self._response_value = None
            else:
                self._response_value = None
                for response in self._get_responses_gen():
                    if response.response_id == chosen_response:
                        self._response_value = response.value
            self._listeners(self)
            return True
        except Exception as ex:
            self.log.error('Error occurred while attempting to respond.', exception=ex)
            return False
        finally:
            self.on_response_received()

    def _get_responses_gen(self) -> Iterator[CommonUiDialogResponse]:
        yield from super()._get_responses_gen()

    @property
    def responses(self) -> Tuple[CommonUiDialogResponse]:
        """The responses of the dialog."""
        result: Tuple[CommonUiDialogResponse] = (
            *self._responses,
        )
        return result


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib_testing.show_ui_response_dialog', 'Show an example of UI Response Dialog.', show_with_help_command=False)
def _common_testing_show_ui_response_dialog(output: CommonConsoleCommandOutput):
    output('Showing test ui response dialog.')

    def _on_chosen(_: CommonUiResponseDialog):
        response_value = _.get_response_value()
        output('Chosen value {}'.format(response_value if response_value is not None else 'No value chosen.'))

    responses: Tuple[CommonUiDialogResponse] = (
        CommonUiDialogResponse(0, 'one', text='Button one'),
        CommonUiDialogResponse(1, 'two', text='Button two')
    )
    title = CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN, tokens=(CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN), ))
    description = CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN, tokens=(CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE), ))

    active_sim_info = CommonSimUtils.get_active_sim_info()
    dialog = CommonUiResponseDialog.TunableFactory().default(
        active_sim_info,
        responses,
        # Having a value of 0 means that we want to display the Close button with no other dialog options.
        dialog_options=0,
        text=lambda *_, **__: description,
        title=lambda *_, **__: title
    )
    dialog.add_listener(_on_chosen)
    dialog.show_dialog()
