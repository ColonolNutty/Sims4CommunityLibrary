"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat

from typing import Tuple, Any, Callable, Union, Iterator, List, Dict
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.choose_object_dialog import CommonChooseObjectDialog
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_choose_dialog import CommonChooseDialog
from sims4communitylib.dialogs.common_dialog import CommonDialog
from sims4communitylib.dialogs.custom_dialogs.picker_dialogs.common_ui_multi_picker import CommonUiMultiPicker
from sims4communitylib.dialogs.utils.common_dialog_utils import CommonDialogUtils
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog import UiDialogBase
from ui.ui_dialog_picker import ObjectPickerRow


class CommonMultiPaneChooseDialog(CommonDialog):
    """CommonMultiPaneChooseDialog(\
        mod_identity,\
        title_identifier,\
        description_identifier,\
        title_tokens=(),\
        description_tokens=()\
    )

    Create a multi-pane dialog that prompts the player to choose from multiple dialogs and submit their choices.

    .. note:: To see an example dialog, run the command :class:`s4clib_testing.show_multi_pane_choose_dialog` in the in-game console.

    .. warning:: This dialog does not currently work with `CommonChooseSimDialog` or `CommonChooseSimsDialog`.

    .. highlight:: python
    .. code-block:: python

        def _common_testing_show_multi_pane_choose_dialog():

            def _on_submit(choices_made: Tuple[Any], outcome: CommonChoiceOutcome) -> None:
                pass

            def _on_sub_dialog_one_chosen(choice: Any, outcome: CommonChoiceOutcome) -> None:
                pass

            def _on_sub_dialog_two_chosen(choice: Any, outcome: CommonChoiceOutcome) -> None:
                pass

            # LocalizedStrings within other LocalizedStrings
            title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
            description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
            from sims4communitylib.utils.common_icon_utils import CommonIconUtils
            # Create the dialog.
            dialog = CommonMultiPaneChooseDialog(
                ModInfo.get_identity(),
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                title_tokens=title_tokens,
                description_tokens=description_tokens
            )

            sub_dialog_one_options = [
                ObjectPickerRow(
                    option_id=1,
                    name=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING),
                    row_description=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_ONE),
                    row_tooltip=None,
                    icon=CommonIconUtils.load_checked_square_icon(),
                    tag='Value 1'
                ),
                ObjectPickerRow(
                    option_id=2,
                    name=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING),
                    row_description=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_TWO),
                    row_tooltip=None,
                    icon=CommonIconUtils.load_arrow_navigate_into_icon(),
                    tag='Value 2'
                ),
                ObjectPickerRow(
                    option_id=3,
                    name=CommonLocalizationUtils.create_localized_string('Value 3'),
                    row_description=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_TWO),
                    row_tooltip=None,
                    icon=CommonIconUtils.load_arrow_navigate_into_icon(),
                    tag='Value 3'
                )
            ]

            # Add sub dialog one.
            sub_dialog_one = CommonChooseObjectDialog(
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                tuple(sub_dialog_one_options),
                title_tokens=title_tokens,
                description_tokens=description_tokens
            )
            dialog.add_sub_dialog(sub_dialog_one, on_chosen=_on_sub_dialog_one_chosen)

            # Add sub dialog two.
            sub_dialog_two_options = [
                ObjectPickerRow(
                    option_id=4,
                    name=CommonLocalizationUtils.create_localized_string('Value 4'),
                    row_description=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_ONE),
                    row_tooltip=None,
                    icon=CommonIconUtils.load_checked_square_icon(),
                    tag='Value 4'
                ),
                ObjectPickerRow(
                    option_id=5,
                    name=CommonLocalizationUtils.create_localized_string('Value 5'),
                    row_description=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_TWO),
                    row_tooltip=None,
                    icon=CommonIconUtils.load_arrow_navigate_into_icon(),
                    tag='Value 5'
                ),
                ObjectPickerRow(
                    option_id=6,
                    name=CommonLocalizationUtils.create_localized_string('Value 6'),
                    row_description=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_TWO),
                    row_tooltip=None,
                    icon=CommonIconUtils.load_arrow_navigate_into_icon(),
                    tag='Value 6'
                )
            ]

            sub_dialog_two = CommonChooseObjectDialog(
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                tuple(sub_dialog_two_options),
                title_tokens=title_tokens,
                description_tokens=description_tokens
            )

            dialog.add_sub_dialog(sub_dialog_two, on_chosen=_on_sub_dialog_two_chosen)

            # Show the dialog.
            dialog.show(on_submit=_on_submit)

    :param title_identifier: The title to display in the dialog.
    :type title_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param description_identifier: The description to display in the dialog.
    :type description_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param title_tokens: Tokens to format into the title.
    :type title_tokens: Iterator[Any], optional
    :param description_tokens: Tokens to format into the description.
    :type description_tokens: Iterator[Any], optional
    :param mod_identity: The identity of the mod creating the dialog. See :class:`.CommonModIdentity` for more information.
    :type mod_identity: CommonModIdentity, optional
    """
    def __init__(
        self,
        mod_identity: CommonModIdentity,
        title_identifier: Union[int, str, LocalizedString, CommonStringId],
        description_identifier: Union[int, str, LocalizedString, CommonStringId],
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=(),
    ):
        super().__init__(
            title_identifier,
            description_identifier,
            title_tokens=title_tokens,
            description_tokens=description_tokens,
            mod_identity=mod_identity
        )
        self._sub_dialogs: Tuple[Tuple[CommonChooseDialog, Tuple[Any], Dict[str, Any]]] = tuple()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cl_multi_pane_choose_dialog'

    def add_sub_dialog(self, sub_dialog: CommonChooseDialog, *dialog_arguments: Any, **dialog_keyword_arguments: Any):
        """add_sub_dialog(sub_dialog, *dialog_arguments, **dialog_keyword_arguments)

        Add a sub dialog to the dialog.

        :param sub_dialog: An instance of a choose dialog.
        :type sub_dialog: CommonChooseDialog
        :param dialog_arguments: Arguments to pass to the sub dialog when building it.
        :type dialog_arguments: Any
        :param dialog_keyword_arguments: Keyword arguments to pass to the sub dialog when building it.
        :type dialog_keyword_arguments: Any
        """
        self._sub_dialogs += ((sub_dialog, dialog_arguments, dialog_keyword_arguments), )

    def show(
        self,
        on_submit: Callable[[Dict[int, Tuple[Any]], CommonChoiceOutcome], Any]=CommonFunctionUtils.noop,
        sim_info: SimInfo=None
    ):
        """show(\
            on_submit=CommonFunctionUtils.noop,\
            sim_info=None\
        )

        Show the dialog and invoke the callbacks upon the player making a choice.

        :param on_submit: A callback invoked upon the player submitting the dialog and the choices within it.\
            Default is CommonFunctionUtils.noop. Each choice is mapped as follows The key is the dialog index starting at 0. The value is the choice made within that sub dialog.
        :type on_submit: Callable[[Dict[int, Tuple[Any]], CommonChoiceOutcome], Any], optional
        :param sim_info: The Sim that will appear in the dialog image. The default Sim is the Active Sim. Default is None.
        :type sim_info: SimInfo, optional
        """
        try:
            return self._show(
                on_submit=on_submit,
                sim_info=sim_info
            )
        except Exception as ex:
            self.log.error('An error occurred while running \'{}\''.format(CommonMultiPaneChooseDialog.show.__name__), exception=ex)

    def _show(
        self,
        on_submit: Callable[[Dict[int, Tuple[Any]], CommonChoiceOutcome], Any]=CommonFunctionUtils.noop,
        sim_info: SimInfo=None
    ):
        self.log.debug('Attempting to display multi choose dialog.')
        dialog = self.build_dialog(
            on_submit=on_submit,
            sim_info=sim_info
        )
        dialog.show_dialog()

    # noinspection PyMissingOrEmptyDocstring
    def build_dialog(
        self,
        on_submit: Callable[[Dict[int, Tuple[Any]], CommonChoiceOutcome], bool]=CommonFunctionUtils.noop,
        sim_info: SimInfo=None
    ):
        dialog = self._create_dialog(sim_info=sim_info)
        if dialog is None:
            self.log.error('dialog was None for some reason.')
            return

        if on_submit is None:
            raise AssertionError('on_submit was None.')

        if len(self._sub_dialogs) == 0:
            raise AssertionError('No dialogs have been added to the container. Add dialogs before attempting to display the multi pane dialog.')

        def _on_submit(_dialog: CommonUiMultiPicker) -> bool:
            try:
                if not _dialog.accepted:
                    self.log.debug('Dialog cancelled.')
                    return on_submit(dict(), CommonChoiceOutcome.CANCEL)
                self.log.debug('Choices made, combining choices.')
                index = 0
                dialog_choices: Dict[int, Tuple[Any]] = dict()
                for _sub_dialog_submit_id in _dialog._picker_dialogs:
                    _sub_dialog_submit = _dialog._picker_dialogs[_sub_dialog_submit_id]
                    sub_dialog_choices: List[Any] = list()
                    for choice in CommonDialogUtils.get_chosen_items(_sub_dialog_submit):
                        sub_dialog_choices.append(choice)
                    dialog_choices[index] = tuple(sub_dialog_choices)
                    index += 1
                if not dialog_choices:
                    self.log.debug('No choices made. Cancelling dialog.')
                    return on_submit(dict(), CommonChoiceOutcome.CANCEL)

                self.log.format_with_message('Choices were made, submitting.', choice=dialog_choices)
                result = on_submit(dialog_choices, CommonChoiceOutcome.CHOICE_MADE)
                self.log.format_with_message('Finished handling choice.', result=result)
                return result
            except Exception as ex:
                self.log.error('Error occurred on submitting a value.', exception=ex)
            return False

        for (sub_dialog, sub_dialog_arguments, sub_dialog_keyword_arguments) in self._sub_dialogs:
            sub_dialog: CommonChooseDialog = sub_dialog
            # noinspection PyBroadException
            try:
                # Delete to prevent duplicate keyword arguments.
                if 'include_pagination' in sub_dialog_keyword_arguments:
                    del sub_dialog_keyword_arguments['include_pagination']

                _sub_dialog: UiDialogBase = sub_dialog.build_dialog(
                    *sub_dialog_arguments,
                    include_pagination=False,
                    **sub_dialog_keyword_arguments
                )
            except:
                _sub_dialog: UiDialogBase = sub_dialog.build_dialog(
                    *sub_dialog_arguments,
                    **sub_dialog_keyword_arguments
                )
            if _sub_dialog is None:
                continue
            dialog.required_tooltips[_sub_dialog.dialog_id] = sub_dialog.required_tooltip
            dialog._picker_dialogs[_sub_dialog.dialog_id] = _sub_dialog

        self.log.debug('Showing dialog.')
        dialog.add_listener(_on_submit)
        return dialog

    def _create_dialog(self, sim_info: SimInfo=None) -> Union[CommonUiMultiPicker, None]:
        try:
            return CommonUiMultiPicker.TunableFactory().default(
                sim_info or CommonSimUtils.get_active_sim_info(),
                text=lambda *args, **kwargs: self.description,
                title=lambda *args, **kwargs: self.title,
                text_input=None,
                pickers=()
            )
        except Exception as ex:
            self.log.error('multi_pane_choose._create_dialog', exception=ex)
        return None


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.show_multi_pane_choose_dialog',
    'Show an example of CommonMultiPaneChooseDialog.'
)
def _common_testing_show_multi_pane_choose_dialog(output: CommonConsoleCommandOutput):
    output('Showing test multi-pane choose dialog.')

    def _on_submit(choices_made: Dict[int, Any], outcome: CommonChoiceOutcome) -> None:
        output('On Submit choices_made: {} and outcome: {}'.format(pformat(choices_made), pformat(outcome)))

    def _on_sub_dialog_one_chosen(choice: Any, outcome: CommonChoiceOutcome) -> None:
        output('Sub Dialog one choice made: {} outcome: {}'.format(pformat(choice), pformat(outcome)))

    def _on_sub_dialog_two_chosen(choice: Any, outcome: CommonChoiceOutcome) -> None:
        output('Sub Dialog two choice made: {} outcome: {}'.format(pformat(choice), pformat(outcome)))

    sim_info = CommonSimUtils.get_active_sim_info()

    # LocalizedStrings within other LocalizedStrings
    title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
    description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
    from sims4communitylib.utils.common_icon_utils import CommonIconUtils
    # Create the dialog.
    dialog = CommonMultiPaneChooseDialog(
        ModInfo.get_identity(),
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        title_tokens=title_tokens,
        description_tokens=description_tokens
    )

    sub_dialog_one_options = [
        ObjectPickerRow(
            option_id=1,
            name=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING),
            row_description=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_ONE),
            row_tooltip=None,
            icon=CommonIconUtils.load_checked_square_icon(),
            tag='Value 1'
        ),
        ObjectPickerRow(
            option_id=2,
            name=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING),
            row_description=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_TWO),
            row_tooltip=None,
            icon=CommonIconUtils.load_arrow_navigate_into_icon(),
            tag='Value 2'
        ),
        ObjectPickerRow(
            option_id=3,
            name=CommonLocalizationUtils.create_localized_string('Value 3'),
            row_description=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_TWO),
            row_tooltip=None,
            icon=CommonIconUtils.load_arrow_navigate_into_icon(),
            tag='Value 3'
        )
    ]

    # Add sub dialog one.
    sub_dialog_one = CommonChooseObjectDialog(
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        tuple(sub_dialog_one_options),
        title_tokens=title_tokens,
        description_tokens=description_tokens
    )
    dialog.add_sub_dialog(sub_dialog_one, on_chosen=_on_sub_dialog_one_chosen, sim_info=sim_info)

    # Add sub dialog two.
    sub_dialog_two_options = [
        ObjectPickerRow(
            option_id=4,
            name=CommonLocalizationUtils.create_localized_string('Value 4'),
            row_description=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_ONE),
            row_tooltip=None,
            icon=CommonIconUtils.load_checked_square_icon(),
            tag='Value 4'
        ),
        ObjectPickerRow(
            option_id=5,
            name=CommonLocalizationUtils.create_localized_string('Value 5'),
            row_description=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_TWO),
            row_tooltip=None,
            icon=CommonIconUtils.load_arrow_navigate_into_icon(),
            tag='Value 5'
        ),
        ObjectPickerRow(
            option_id=6,
            name=CommonLocalizationUtils.create_localized_string('Value 6'),
            row_description=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_TWO),
            row_tooltip=None,
            icon=CommonIconUtils.load_arrow_navigate_into_icon(),
            tag='Value 6'
        )
    ]

    sub_dialog_two = CommonChooseObjectDialog(
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        tuple(sub_dialog_two_options),
        title_tokens=title_tokens,
        description_tokens=description_tokens
    )

    dialog.add_sub_dialog(sub_dialog_two, on_chosen=_on_sub_dialog_two_chosen, include_pagination=True)

    # Show the dialog.
    dialog.show(on_submit=_on_submit)
    output('Done showing.')
