"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat

from typing import Any, Union, Callable, Iterator, Dict, Tuple, List

from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_multi_pane_choose_dialog import CommonMultiPaneChooseDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_option_dialog import CommonChooseOptionDialog
from sims4communitylib.dialogs.option_dialogs.common_option_dialog import CommonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option import CommonDialogOption
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext, \
    DialogOptionValueType
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_object_option import CommonDialogObjectOption
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from ui.ui_dialog import UiDialogBase


class CommonMultiPaneChooseOptionDialog(CommonOptionDialog):
    """CommonMultiPaneChooseOptionDialog(\
        mod_identity,\
        title_identifier,\
        description_identifier,\
        title_tokens=(),\
        description_tokens=(),\
        on_close=CommonFunctionUtils.noop\
    )

    A container for multiple choose option dialogs.

    .. note:: To see an example dialog, run the command :class:`s4clib_testing.show_multi_pane_choose_option_dialog` in the in-game console.

    .. warning:: This dialog does not currently work with `CommonChooseSimOptionDialog` or `CommonChooseSimsOptionDialog`.

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        def _on_option_chosen_in_dialog_one(option_identifier: str, choice: str):
            pass

        def _on_option_chosen_in_dialog_two(option_identifier: str, choice: str):
            pass

        def _on_submit(chosen_options: Dict[int, Any]):
            pass

        # LocalizedStrings within other LocalizedStrings
        title_tokens = (
            CommonLocalizationUtils.create_localized_string(
                CommonStringId.TESTING_SOME_TEXT_FOR_TESTING,
                text_color=CommonLocalizedStringColor.GREEN
            ),
        )
        description_tokens = (
            CommonLocalizationUtils.create_localized_string(
                CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME,
                tokens=(CommonSimUtils.get_active_sim_info(),),
                text_color=CommonLocalizedStringColor.BLUE
            ),
        )

        sub_dialog_one = CommonChooseObjectOptionDialog(
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            title_tokens=title_tokens,
            description_tokens=description_tokens,
            per_page=2
        )

        sub_dialog_one.add_option(
            CommonDialogObjectOption(
                'Option 1',
                'Value 1',
                CommonDialogOptionContext(
                    CommonStringId.TESTING_SOME_TEXT_FOR_TESTING,
                    CommonStringId.TESTING_TEST_BUTTON_ONE,
                    icon=CommonIconUtils.load_checked_square_icon()
                ),
                on_chosen=_on_option_chosen_in_dialog_one
            )
        )

        sub_dialog_one.add_option(
            CommonDialogObjectOption(
                'Option 2',
                'Value 2',
                CommonDialogOptionContext(
                    CommonStringId.TESTING_SOME_TEXT_FOR_TESTING,
                    CommonStringId.TESTING_TEST_BUTTON_TWO,
                    icon=CommonIconUtils.load_arrow_navigate_into_icon()
                ),
                on_chosen=_on_option_chosen_in_dialog_one
            )
        )

        sub_dialog_one.add_option(
            CommonDialogObjectOption(
                'Option 3',
                'Value 3',
                CommonDialogOptionContext(
                    CommonLocalizationUtils.create_localized_string('Value 3'),
                    CommonStringId.TESTING_TEST_BUTTON_TWO,
                    icon=CommonIconUtils.load_arrow_navigate_into_icon()
                ),
                on_chosen=_on_option_chosen_in_dialog_one
            )
        )

        sub_dialog_two = CommonChooseObjectOptionDialog(
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            title_tokens=title_tokens,
            description_tokens=description_tokens,
            per_page=2
        )

        sub_dialog_two.add_option(
            CommonDialogObjectOption(
                'Option 4',
                'Value 4',
                CommonDialogOptionContext(
                    CommonStringId.TESTING_SOME_TEXT_FOR_TESTING,
                    CommonStringId.TESTING_TEST_BUTTON_ONE,
                    icon=CommonIconUtils.load_checked_square_icon()
                ),
                on_chosen=_on_option_chosen_in_dialog_two
            )
        )

        sub_dialog_two.add_option(
            CommonDialogObjectOption(
                'Option 5',
                'Value 5',
                CommonDialogOptionContext(
                    CommonStringId.TESTING_SOME_TEXT_FOR_TESTING,
                    CommonStringId.TESTING_TEST_BUTTON_TWO,
                    icon=CommonIconUtils.load_arrow_navigate_into_icon()
                ),
                on_chosen=_on_option_chosen_in_dialog_two
            )
        )

        sub_dialog_two.add_option(
            CommonDialogObjectOption(
                'Option 6',
                'Value 6',
                CommonDialogOptionContext(
                    CommonLocalizationUtils.create_localized_string('Value 3'),
                    CommonStringId.TESTING_TEST_BUTTON_TWO,
                    icon=CommonIconUtils.load_arrow_navigate_into_icon()
                ),
                on_chosen=_on_option_chosen_in_dialog_two
            )
        )

        option_dialog = CommonMultiPaneChooseOptionDialog(
            ModInfo.get_identity(),
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            title_tokens=title_tokens,
            description_tokens=description_tokens
        )

        option_dialog.add_sub_dialog(sub_dialog_one)
        option_dialog.add_sub_dialog(sub_dialog_two)

        option_dialog.show(
            on_submit=_on_submit,
            sim_info=CommonSimUtils.get_active_sim_info()
        )


    :param mod_identity: The identity of the mod creating the dialog. See :class:`.CommonModIdentity` for more information.
    :type mod_identity: CommonModIdentity
    :param title_identifier: A decimal identifier of the title text.
    :type title_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param description_identifier: A decimal identifier of the description text.
    :type description_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param title_tokens: An iterator of Tokens to format into the title. Default is an empty collection.
    :type title_tokens: Iterator[Any], optional
    :param description_tokens: An iterator of Tokens to format into the description. Default is an empty collection.
    :type description_tokens: Iterator[Any], optional
    :param on_close: A callback invoked upon the dialog closing. Default is CommonFunctionUtils.noop.
    :type on_close: Callable[[], None], optional
    """
    def __init__(
        self,
        mod_identity: CommonModIdentity,
        title_identifier: Union[int, str, LocalizedString, CommonStringId],
        description_identifier: Union[int, str, LocalizedString, CommonStringId],
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=(),
        on_close: Callable[[], None]=CommonFunctionUtils.noop
    ):
        super().__init__(
            CommonMultiPaneChooseDialog(
                mod_identity,
                title_identifier,
                description_identifier,
                title_tokens=title_tokens,
                description_tokens=description_tokens
            ),
            on_close=on_close
        )

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cl_multi_pane_choose_option_dialog'

    @property
    def _internal_dialog(self) -> CommonMultiPaneChooseDialog:
        result: CommonMultiPaneChooseDialog = super()._internal_dialog
        return result

    def add_sub_dialog(self, sub_dialog: CommonChooseOptionDialog, *dialog_arguments: Any, **dialog_keyword_arguments: Any):
        """add_sub_dialog(sub_dialog, *dialog_arguments, **dialog_keyword_arguments)

        Add a sub dialog.

        :param sub_dialog: An instance of a choose option dialog.
        :type sub_dialog: CommonChooseOptionDialog
        :param dialog_arguments: Arguments to pass to the sub dialog when building it.
        :type dialog_arguments: Any, optional
        :param dialog_keyword_arguments: Keyword arguments to pass to the sub dialog when building it.
        :type dialog_keyword_arguments: Any, optional
        """
        self._internal_dialog.add_sub_dialog(sub_dialog._internal_dialog, *dialog_arguments, **dialog_keyword_arguments)

    def show(
        self,
        on_submit: Callable[[Dict[int, Tuple[Any]]], Any]=CommonFunctionUtils.noop,
        sim_info: SimInfo=None
    ):
        """show(\
            on_submit=CommonFunctionUtils.noop,\
            sim_info=None\
        )

        Show the dialog and invoke the callbacks upon the player submitting their selections.

        :param on_submit: A callback invoked upon the player submitting the dialog and the choices within it.\
            Each choice is mapped as follows: The key is the index of the dialog a value belongs to, starting at 0. The value is the choice made within that dialog. Default is CommonFunctionUtils.noop.
        :type on_submit: Callable[[Dict[int, Tuple[Any]]], Any], optional
        :param sim_info: The SimInfo of the Sim that will appear in the dialog image. The default Sim is the active Sim. Default is None.
        :type sim_info: SimInfo, optional
        """
        try:
            return self._internal_dialog.show(on_submit=self._on_submit(on_submit=on_submit), sim_info=sim_info)
        except Exception as ex:
            self.log.error('multi_pane_choose_option.show', exception=ex)

    def build_dialog(
        self,
        on_submit: Callable[[Dict[int, Tuple[Any]]], bool]=CommonFunctionUtils.noop,
        sim_info: SimInfo=None
    ) -> Union[UiDialogBase, None]:
        """build_dialog(\
            on_submit=CommonFunctionUtils.noop,\
            sim_info=None\
        )

        Build the dialog and invoke the callbacks upon the player submitting their selections.

        :param on_submit: A callback invoked upon the player submitting the dialog and the choices within it.\
            Default is CommonFunctionUtils.noop. Each choice is mapped as follows The key is the dialog index starting at 0. The value is the choice made within that sub dialog. Default is CommonFunctionUtils.noop.
        :type on_submit: Callable[[Dict[int, Tuple[Any]]], Any], optional
        :param sim_info: The SimInfo of the Sim that will appear in the dialog image. The default Sim is the active Sim. Default is None.
        :type sim_info: SimInfo, optional
        """
        try:
            return self._internal_dialog.build_dialog(on_submit=self._on_submit(on_submit=on_submit), sim_info=sim_info)
        except Exception as ex:
            self.log.error('multi_pane_choose_option.build_dialog', exception=ex)
        return None

    def _on_submit(
        self,
        on_submit: Callable[[Dict[int, Tuple[Any]]], Any]=CommonFunctionUtils.noop
    ) -> Callable[[Dict[int, Tuple[CommonDialogOption]], CommonChoiceOutcome], bool]:
        def _on_submit(chosen_options: Dict[int, Tuple[CommonDialogOption]], outcome: CommonChoiceOutcome) -> bool:
            try:
                if chosen_options is None or not chosen_options or CommonChoiceOutcome.is_error_or_cancel(outcome):
                    self.log.debug('No options chosen.')
                    self.close()
                    return False

                self.log.debug('Chose options: {} with outcome: {}'.format(pformat(chosen_options), pformat(outcome)))
                chosen_values: Dict[int, DialogOptionValueType] = dict()
                for chosen_option_index in chosen_options:
                    self.log.debug('Chosen option index: {}'.format(chosen_option_index))
                    chosen_option_options = chosen_options[chosen_option_index]
                    chosen_option_values: List[Any] = list()
                    for chosen_option_option in chosen_option_options:
                        chosen_option_values.append(chosen_option_option.value)
                        self.log.debug('Chose value for option: {}'.format(chosen_option_option.value))
                        chosen_option_option.choose()
                    chosen_values[chosen_option_index] = tuple(chosen_option_values)

                self.log.debug('Submitting choices: {}'.format(pformat(chosen_values)))
                return on_submit(chosen_values)
            except Exception as ex:
                self.log.error('Error occurred on submitting a value.', exception=ex)
            return False
        return _on_submit


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.show_multi_pane_choose_option_dialog',
    'Show an example of CommonMultiPaneChooseOptionDialog.'
)
def _common_testing_show_multi_pane_choose_option_dialog(output: CommonConsoleCommandOutput):
    output('Showing test multi pane choose option dialog.')

    def _on_option_chosen_in_dialog_one(option_identifier: str, choice: str):
        output('Chose option in dialog one {} with value: {}.'.format(pformat(option_identifier), pformat(choice)))

    def _on_option_chosen_in_dialog_two(option_identifier: str, choice: str):
        output('Chose option in dialog two {} with value: {}.'.format(pformat(option_identifier), pformat(choice)))

    def _on_submit(chosen_options: Dict[int, Any]):
        output('Chosen options from all dialogs {}.'.format(pformat(chosen_options)))

    # LocalizedStrings within other LocalizedStrings
    title_tokens = (
        CommonLocalizationUtils.create_localized_string(
            CommonStringId.TESTING_SOME_TEXT_FOR_TESTING,
            text_color=CommonLocalizedStringColor.GREEN
        ),
    )
    description_tokens = (
        CommonLocalizationUtils.create_localized_string(
            CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME,
            tokens=(CommonSimUtils.get_active_sim_info(),),
            text_color=CommonLocalizedStringColor.BLUE
        ),
    )

    sub_dialog_one = CommonChooseObjectOptionDialog(
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        title_tokens=title_tokens,
        description_tokens=description_tokens,
        per_page=2
    )

    sub_dialog_one.add_option(
        CommonDialogObjectOption(
            'Option 1',
            'Value 1',
            CommonDialogOptionContext(
                CommonStringId.TESTING_SOME_TEXT_FOR_TESTING,
                CommonStringId.TESTING_TEST_BUTTON_ONE,
                icon=CommonIconUtils.load_checked_square_icon()
            ),
            on_chosen=_on_option_chosen_in_dialog_one
        )
    )

    sub_dialog_one.add_option(
        CommonDialogObjectOption(
            'Option 2',
            'Value 2',
            CommonDialogOptionContext(
                CommonStringId.TESTING_SOME_TEXT_FOR_TESTING,
                CommonStringId.TESTING_TEST_BUTTON_TWO,
                icon=CommonIconUtils.load_arrow_navigate_into_icon()
            ),
            on_chosen=_on_option_chosen_in_dialog_one
        )
    )

    sub_dialog_one.add_option(
        CommonDialogObjectOption(
            'Option 3',
            'Value 3',
            CommonDialogOptionContext(
                CommonLocalizationUtils.create_localized_string('Value 3'),
                CommonStringId.TESTING_TEST_BUTTON_TWO,
                icon=CommonIconUtils.load_arrow_navigate_into_icon()
            ),
            on_chosen=_on_option_chosen_in_dialog_one
        )
    )

    sub_dialog_two = CommonChooseObjectOptionDialog(
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        title_tokens=title_tokens,
        description_tokens=description_tokens,
        per_page=2
    )

    sub_dialog_two.add_option(
        CommonDialogObjectOption(
            'Option 4',
            'Value 4',
            CommonDialogOptionContext(
                CommonStringId.TESTING_SOME_TEXT_FOR_TESTING,
                CommonStringId.TESTING_TEST_BUTTON_ONE,
                icon=CommonIconUtils.load_checked_square_icon()
            ),
            on_chosen=_on_option_chosen_in_dialog_two
        )
    )

    sub_dialog_two.add_option(
        CommonDialogObjectOption(
            'Option 5',
            'Value 5',
            CommonDialogOptionContext(
                CommonStringId.TESTING_SOME_TEXT_FOR_TESTING,
                CommonStringId.TESTING_TEST_BUTTON_TWO,
                icon=CommonIconUtils.load_arrow_navigate_into_icon()
            ),
            on_chosen=_on_option_chosen_in_dialog_two
        )
    )

    sub_dialog_two.add_option(
        CommonDialogObjectOption(
            'Option 6',
            'Value 6',
            CommonDialogOptionContext(
                CommonLocalizationUtils.create_localized_string('Value 3'),
                CommonStringId.TESTING_TEST_BUTTON_TWO,
                icon=CommonIconUtils.load_arrow_navigate_into_icon()
            ),
            on_chosen=_on_option_chosen_in_dialog_two
        )
    )

    option_dialog = CommonMultiPaneChooseOptionDialog(
        ModInfo.get_identity(),
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        title_tokens=title_tokens,
        description_tokens=description_tokens
    )

    option_dialog.add_sub_dialog(sub_dialog_one)
    option_dialog.add_sub_dialog(sub_dialog_two)

    option_dialog.show(
        on_submit=_on_submit,
        sim_info=CommonSimUtils.get_active_sim_info()
    )
    output('Done showing.')
