"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import math
import os

from typing import Tuple, Any, Callable, Union, Iterator

from pprint import pformat

from event_testing.resolver import DoubleSimResolver
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_dialog import CommonDialog
from sims4communitylib.dialogs.common_dialog_navigation_button_tag import CommonDialogNavigationButtonTag
from sims4communitylib.dialogs.common_ui_dialog_response import CommonUiDialogResponse
from sims4communitylib.dialogs.common_ui_response_dialog import CommonUiResponseDialog
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog import UiDialogOption, ButtonType

ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'


class CommonChooseResponseDialog(CommonDialog):
    """CommonChooseResponseDialog(\
        mod_identity,\
        title_identifier,\
        description_identifier,\
        responses,\
        title_tokens=(),\
        description_tokens=(),\
        next_button_text=CommonStringId.NEXT,\
        previous_button_text=CommonStringId.PREVIOUS,\
    )

    Create a dialog that prompts the player to choose a response.

    .. note:: To see an example dialog, run the command :class:`s4clib_testing.show_choose_response_dialog` in the in-game console.

    .. highlight:: python
    .. code-block:: python

        def _common_testing_show_choose_response_dialog():

            def _on_chosen(choice: str, outcome: CommonChoiceOutcome):
                pass

            responses: Tuple[CommonUiDialogResponse] = (
                CommonUiDialogResponse(
                    1,
                    'Value 1',
                    text=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_ONE)
                ),
                CommonUiDialogResponse(
                    2,
                    'Value 2',
                    text=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_TWO)
                ),
                CommonUiDialogResponse(
                    3,
                    'Value 3',
                    text=CommonLocalizationUtils.create_localized_string('Test Button 3')
                )
            )
            title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
            description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)

            active_sim_info = CommonSimUtils.get_active_sim_info()
            dialog = CommonChooseResponseDialog(
                ModInfo.get_identity(),
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                responses,
                title_tokens=title_tokens,
                description_tokens=description_tokens,
                per_page=2
            )
            dialog.show(
                on_chosen=_on_chosen,
                sim_info=active_sim_info,
                include_previous_button=False
            )

    :param title_identifier: The title to display in the dialog.
    :type title_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param description_identifier: The description to display in the dialog.
    :type description_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param responses: The choices that can be chosen.
    :type responses: Iterator[CommonUiDialogResponse]
    :param title_tokens: Tokens to format into the title. Default is no tokens.
    :type title_tokens: Iterator[Any], optional
    :param description_tokens: Tokens to format into the description. Default is no tokens.
    :type description_tokens: Iterator[Any], optional
    :param next_button_text: The text the Next button will display, if the Next button is added. Default is Next.
    :type next_button_text: Union[int, str, LocalizedString, CommonStringId], optional
    :param previous_button_text: The text the Previous button will display, if the Previous button is added. Default is Previous.
    :type previous_button_text: Union[int, str, LocalizedString, CommonStringId], optional
    :param per_page: The number of responses to display per page of the dialog. Default is 10.
    :type per_page: int, optional
    :param mod_identity: The identity of the mod creating the dialog. See :class:`.CommonModIdentity` for more information.
    :type mod_identity: CommonModIdentity, optional
    """
    # If on Read The Docs, create fake versions of extended objects to fix the error of inheriting from multiple MockObjects.
    if ON_RTD:
        _NEXT_BUTTON_ID = 10001
        _PREVIOUS_BUTTON_ID = 10002

    if not ON_RTD:
        _NEXT_BUTTON_ID: int = int(ButtonType.DIALOG_RESPONSE_OK)
        _PREVIOUS_BUTTON_ID: int = int(ButtonType.DIALOG_RESPONSE_CANCEL)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cl_choose_response_dialog'

    def __init__(
        self,
        mod_identity: CommonModIdentity,
        title_identifier: Union[int, str, LocalizedString, CommonStringId],
        description_identifier: Union[int, str, LocalizedString, CommonStringId],
        responses: Iterator[CommonUiDialogResponse],
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=(),
        next_button_text: Union[int, str, LocalizedString, CommonStringId]=CommonStringId.NEXT,
        previous_button_text: Union[int, str, LocalizedString, CommonStringId]=CommonStringId.PREVIOUS,
        per_page: int=10
    ):
        super().__init__(
            title_identifier,
            description_identifier,
            title_tokens=title_tokens,
            description_tokens=description_tokens,
            mod_identity=mod_identity
        )
        if per_page <= 0:
            raise AssertionError('\'per_page\' must be greater than zero.')
        self._responses = tuple(responses)
        self._per_page = per_page
        self._current_page = 1
        self._next_button_text = CommonLocalizationUtils.create_localized_string(next_button_text)
        self._previous_button_text = CommonLocalizationUtils.create_localized_string(previous_button_text)
        self._always_visible_responses = tuple()

    @property
    def current_page(self) -> int:
        """The current page shown of the dialog."""
        return self._current_page

    @property
    def responses(self) -> Tuple[CommonUiDialogResponse]:
        """The responses to display in the dialog."""
        return self._responses

    @property
    def always_visible_responses(self) -> Tuple[CommonUiDialogResponse]:
        """A collection of responses that will always appear in the dialog no matter which page.

        .. note:: These responses are added to the dialog before the normal responses are added to the dialog.

        :return: A collection of responses added to the dialog that will always appear.
        :rtype: Tuple[CommonUiDialogResponse]
        """
        return self._always_visible_responses

    def add_response(self, response: CommonUiDialogResponse, *_, always_visible: bool=False, **__):
        """add_response(response, *_, always_visible=False, **__)

        Add a response to the dialog.

        :param response: The response to add.
        :type response: CommonUiDialogResponse
        :param always_visible: If set to True, the response will always appear in the dialog no matter which page. If False, the response will act as normal. Default is False.
        :type always_visible: bool, optional
        """
        if not always_visible:
            self._responses += (response,)
            return
        try:
            self._always_visible_responses += (response,)
        except Exception as ex:
            self.log.error('An error occurred while running \'{}\''.format(self.add_response.__name__), exception=ex)

    def show(
        self,
        sim_info: SimInfo=None,
        target_sim_info: SimInfo=None,
        on_chosen: Callable[[Any, CommonChoiceOutcome], None]=CommonFunctionUtils.noop,
        on_previous: Callable[[], None]=CommonFunctionUtils.noop,
        dialog_options: UiDialogOption=0,
        include_previous_button: bool=True,
        include_pagination: bool=True,
        page: int=1
    ):
        """show(\
            sim_info=None,\
            target_sim_info=None,\
            on_chosen=CommonFunctionUtils.noop,\
            on_previous=CommonFunctionUtils.noop,\
            dialog_options=0,\
            include_previous_button=True,\
            include_pagination=True,\
            page=1\
        )

        Show the dialog and invoke the callbacks upon the player making a choice.

        :param sim_info: The Sim that will appear in the dialog image. The default Sim is the Active Sim. Default is None.
        :type sim_info: SimInfo, optional
        :param target_sim_info: If provided, the dialog will appear as if it were a conversation instead of the normal view. Default is None.
        :type target_sim_info: SimInfo, optional
        :param on_chosen: A callback invoked upon the player choosing something from the list. Default is CommonFunctionUtils.noop.
        :type on_chosen: Callable[[Any, CommonChoiceOutcome], optional
        :param on_previous: A callback performed when the previous response is chosen. Default is no operation.
        :type on_previous: Callable[[], None], optional
        :param dialog_options: Options to apply to the dialog, such as removing the close button. Default is no options.
        :type dialog_options: UiDialogOption, optional
        :param include_previous_button: If True, the Previous button will be appended to the end of the dialog, if False, the Previous button will not be shown unless the current page is greater than 1. Default is True.
        :type include_previous_button: bool, optional
        :param include_pagination: If True, pagination will be applied. If False, no pagination will be applied. Default is True. The `include_previous_button` argument will override this setting!
        :type include_pagination: bool, optional
        :param page: The page to show the dialog on. Default is the first page.
        :type page: int, optional
        """
        self._current_page = page
        try:
            return self._show(
                sim_info=sim_info,
                target_sim_info=target_sim_info,
                on_chosen=on_chosen,
                on_previous=on_previous,
                dialog_options=dialog_options,
                include_previous_button=include_previous_button,
                include_pagination=include_pagination,
                page=page
            )
        except Exception as ex:
            self.log.error('An error occurred while running \'{}\''.format(self.__class__.show.__name__), exception=ex)

    def _show(
        self,
        sim_info: SimInfo=None,
        target_sim_info: SimInfo=None,
        on_chosen: Callable[[Any, CommonChoiceOutcome], None]=CommonFunctionUtils.noop,
        on_previous: Callable[[], None]=CommonFunctionUtils.noop,
        dialog_options: UiDialogOption=0,
        include_previous_button: bool=True,
        include_pagination: bool=True,
        page: int=1
    ):
        def _on_chosen(choice: Any, outcome: CommonChoiceOutcome) -> None:
            try:
                self.log.debug('Choice made.')
                if choice == CommonDialogNavigationButtonTag.NEXT:
                    self.log.debug('Next chosen.')
                    self.show(on_chosen=on_chosen, on_previous=on_previous, dialog_options=dialog_options, include_previous_button=include_previous_button, sim_info=sim_info, target_sim_info=target_sim_info, page=page + 1)
                    return
                elif choice == CommonDialogNavigationButtonTag.PREVIOUS:
                    self.log.debug('Previous chosen.')
                    if page == 1:
                        on_previous()
                    else:
                        self.show(on_chosen=on_chosen, on_previous=on_previous, dialog_options=dialog_options, include_previous_button=include_previous_button, sim_info=sim_info, target_sim_info=target_sim_info, page=page - 1)
                    return
                self.log.format_with_message('Choice made.', choice=choice)
                on_chosen(choice, outcome)
                self.log.debug('Finished handling _show.')
            except Exception as ex:
                self.log.error('Error occurred on choosing a value.', exception=ex)

        _dialog = self.build_dialog(
            sim_info=sim_info,
            target_sim_info=target_sim_info,
            on_chosen=_on_chosen,
            on_previous=on_previous,
            dialog_options=dialog_options,
            include_previous_button=include_previous_button,
            include_pagination=include_pagination,
            page=page
        )
        if _dialog is None:
            self.log.error('An error occurred when building the dialog!')
            return
        self.log.debug('Showing dialog.')
        _dialog.show_dialog()

    def build_dialog(
        self,
        sim_info: SimInfo=None,
        target_sim_info: SimInfo=None,
        on_chosen: Callable[[Any, CommonChoiceOutcome], None]=CommonFunctionUtils.noop,
        on_previous: Callable[[], None]=CommonFunctionUtils.noop,
        dialog_options: Union[UiDialogOption, int]=0,
        include_previous_button: bool=True,
        include_pagination: bool=True,
        page: int=1
    ) -> Union[CommonUiResponseDialog, None]:
        """build_dialog(\
            sim_info=None,\
            target_sim_info=None,\
            on_chosen=CommonFunctionUtils.noop,\
            on_previous=CommonFunctionUtils.noop,\
            dialog_options=0,\
            include_previous_button=True,\
            include_pagination=True,\
            page=1\
        )

        Build the dialog.

        :param sim_info: A Sim that will appear in the top left image when the dialog is shown. If set to None, the active Sim will be used. Default is None.
        :type sim_info: SimInfo, optional
        :param target_sim_info: If provided, the dialog will appear as if it were a conversation instead of the normal view. Default is None.
        :type target_sim_info: SimInfo, optional
        :param on_chosen: A callback performed when a choice is made. Default is no operation.
        :type on_chosen: Callable[[Any, CommonChoiceOutcome], None], optional
        :param on_previous: A callback performed when the Previous response is chosen. Default is no operation.
        :type on_previous: Callable[[], None], optional
        :param dialog_options: Display options for the dialog, such as hiding the close button. Default is no display options.
        :type dialog_options: UiDialogOption, optional
        :param include_previous_button: If True, the Previous button will be appended to the end of the dialog. Default is True.
        :type include_previous_button: bool, optional
        :param include_pagination: If True, pagination will be applied. If False, no pagination will be applied. Default is True. The `include_previous_button` argument will override this setting!
        :type include_pagination: bool, optional
        :param page: The page to build the dialog on. Default is the first page.
        :type page: int, optional
        :return: The built dialog or None if a problem occurs.
        :rtype: Union[CommonUiResponseDialog, None]
        """
        self.log.format_with_message('Attempting to build dialog.', dialog_options=dialog_options)

        _dialog = self._create_dialog(
            dialog_options=dialog_options,
            sim_info=sim_info,
            target_sim_info=target_sim_info
        )
        if _dialog is None:
            self.log.error('_dialog was None for some reason.')
            return

        if on_chosen is None:
            raise ValueError('on_chosen was None.')

        if len(self.always_visible_responses) == 0 and len(self.responses) == 0:
            raise AssertionError('No responses have been provided. Add responses to the dialog before attempting to display it.')

        def _on_chosen(dialog: CommonUiResponseDialog) -> None:
            try:
                if dialog.cancelled:
                    self.log.debug('Dialog cancelled.')
                    on_chosen(None, CommonChoiceOutcome.CANCEL)
                    return
                choice = dialog.get_response_value()
                self.log.format_with_message('Choice made.', choice=choice)
                on_chosen(choice, CommonChoiceOutcome.CHOICE_MADE)
                self.log.debug('Finished handling _on_chosen.')
            except Exception as ex:
                self.log.error('Error occurred on choosing a value.', exception=ex)

        if include_pagination:
            self._setup_responses(
                _dialog,
                include_previous_button=include_previous_button,
                page=page
            )
        else:
            self.log.debug('Adding always visible responses.')
            for always_visible_response in self.always_visible_responses:
                _dialog.add_response(always_visible_response)
            self.log.debug('Adding responses.')
            for response in self.responses:
                _dialog.add_response(response)

        self.log.debug('Adding listener.')
        _dialog.add_listener(_on_chosen)
        return _dialog

    def _setup_responses(
        self,
        _dialog: CommonUiResponseDialog,
        include_previous_button: bool=True,
        page: int=1
    ):
        if page < 0:
            raise AssertionError('page cannot be less than zero.')

        added_previous_button = False
        number_of_responses = len(self.responses)
        self.log.format(number_of_responses=number_of_responses, per_page=self._per_page)
        if number_of_responses > self._per_page:
            number_of_pages = math.ceil(number_of_responses / self._per_page)

            if page > number_of_pages:
                raise AssertionError('page was out of range. Number of Pages: {}, Requested Page: {}'.format(str(number_of_pages), str(page)))
            # Add the responses that are always visible.
            for always_visible_response in self.always_visible_responses:
                _dialog.add_response(always_visible_response)

            # Add the responses that should show on the current page.
            start_index = (page - 1) * self._per_page
            end_index = page * self._per_page
            self.log.format(start_index=start_index, end_index=end_index)
            current_choices = self.responses[start_index:end_index]
            self.log.format(current_responses=current_choices)
            for response in current_choices:
                _dialog.add_response(response)

            if page < number_of_pages:
                self.log.format_with_message('Adding Next response.', page=page, number_of_pages=number_of_pages)
                _dialog.add_response(CommonUiDialogResponse(len(self.responses) + 1, CommonDialogNavigationButtonTag.NEXT, text=self._next_button_text))
            else:
                self.log.format_with_message('Not adding Next.', page=page, number_of_pages=number_of_pages)

            if page > 1:
                self.log.format_with_message('Adding Previous response.', page=page, number_of_pages=number_of_pages)
                added_previous_button = True
                _dialog.add_response(CommonUiDialogResponse(len(self.responses) + 2, CommonDialogNavigationButtonTag.PREVIOUS, text=self._previous_button_text))
            else:
                self.log.format_with_message('Not adding Previous response.', page=page)
        else:
            self.log.debug('Adding always visible responses.')
            for always_visible_response in self.always_visible_responses:
                _dialog.add_response(always_visible_response)
            self.log.debug('Adding responses.')
            for response in self.responses:
                _dialog.add_response(response)

        if not added_previous_button and include_previous_button:
            self.log.format_with_message('Adding Previous response.', page=page)
            _dialog.add_response(CommonUiDialogResponse(len(self.responses) + 2, CommonDialogNavigationButtonTag.PREVIOUS, text=self._previous_button_text))

    def _create_dialog(
        self,
        dialog_options: UiDialogOption=0,
        sim_info: SimInfo=None,
        target_sim_info: SimInfo=None
    ) -> Union[CommonUiResponseDialog, None]:
        try:
            self.log.debug('Creating dialog.')
            return CommonUiResponseDialog.TunableFactory().default(
                sim_info or CommonSimUtils.get_active_sim_info(),
                tuple(),
                dialog_options=dialog_options,
                text=lambda *_, **__: self.description,
                title=lambda *_, **__: self.title,
                target_sim_id=CommonSimUtils.get_sim_id(target_sim_info) if target_sim_info is not None else None,
                resolver=DoubleSimResolver(sim_info, target_sim_info) if sim_info is not None and target_sim_info is not None else None
            )
        except Exception as ex:
            self.log.error('_create_dialog', exception=ex)
        return None


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.show_choose_response_dialog',
    'Show an example of CommonChooseResponseDialog.'
)
def _common_testing_show_choose_response_dialog(output: CommonConsoleCommandOutput):
    output('Showing test choose response dialog.')

    def _on_chosen(choice: str, outcome: CommonChoiceOutcome):
        output('Chose {} with result: {}.'.format(pformat(choice), pformat(outcome)))

    responses: Tuple[CommonUiDialogResponse] = (
        CommonUiDialogResponse(
            1,
            'Value 1',
            text=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_ONE)
        ),
        CommonUiDialogResponse(
            2,
            'Value 2',
            text=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_TWO)
        ),
        CommonUiDialogResponse(
            3,
            'Value 3',
            text=CommonLocalizationUtils.create_localized_string('Test Button 3')
        )
    )
    title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
    description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)

    active_sim_info = CommonSimUtils.get_active_sim_info()
    dialog = CommonChooseResponseDialog(
        ModInfo.get_identity(),
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        responses,
        title_tokens=title_tokens,
        description_tokens=description_tokens,
        per_page=2
    )
    dialog.show(
        sim_info=active_sim_info,
        on_chosen=_on_chosen,
        include_previous_button=False
    )
    output('Done showing.')
