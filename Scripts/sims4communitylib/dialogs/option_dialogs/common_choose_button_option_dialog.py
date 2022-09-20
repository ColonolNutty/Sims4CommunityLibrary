"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat

from typing import Any, Union, Callable, Iterator

from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choose_response_dialog import CommonChooseResponseDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_response_option_dialog import \
    CommonChooseResponseOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_button_option import \
    CommonDialogButtonOption
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    CommonDialogResponseOptionContext
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.services.commands.common_console_command_parameters import \
    CommonOptionalSimInfoConsoleCommandParameter
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog import UiDialogBase, UiDialogOption


class CommonChooseButtonOptionDialog(CommonChooseResponseOptionDialog):
    """CommonChooseButtonOptionDialog(\
        mod_identity,\
        title_identifier,\
        description_identifier,\
        title_tokens=(),\
        description_tokens=(),\
        include_previous_button=True,\
        on_previous=CommonFunctionUtils.noop,\
        on_close=CommonFunctionUtils.noop\
    )

    A dialog that displays a list of options.

    .. note:: To see an example dialog, run the command :class:`s4clib_testing.show_choose_button_option_dialog` in the in-game console.

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        def _on_option_chosen(option_identifier: DialogOptionIdentifierType, choice: DialogOptionValueType):
            pass

        def _on_previous_chosen() -> None:
            pass

        def _on_close() -> None:
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
        option_dialog = CommonChooseButtonOptionDialog(
            ModInfo.get_identity(),
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            title_tokens=title_tokens,
            description_tokens=description_tokens,
            on_previous=_on_previous_chosen,
            on_close=_on_close
        )

        # We add the options, in this case we have three options.
        option_dialog.add_option(
            CommonDialogButtonOption(
                'Option 1',
                'Value 1',
                CommonDialogResponseOptionContext(
                    CommonStringId.TESTING_SOME_TEXT_FOR_TESTING,
                    subtext_identifier=CommonStringId.TESTING_TEST_BUTTON_ONE
                ),
                on_chosen=_on_option_chosen
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'Option 2',
                'Value 2',
                CommonDialogResponseOptionContext(
                    CommonStringId.TESTING_SOME_TEXT_FOR_TESTING,
                    subtext_identifier=CommonStringId.TESTING_TEST_BUTTON_TWO,
                ),
                on_chosen=_on_option_chosen
            )
        )

        option_dialog.add_option(
            CommonDialogButtonOption(
                'Option 3',
                'Value 3',
                CommonDialogResponseOptionContext(
                    CommonLocalizationUtils.create_localized_string('Value 3'),
                    subtext_identifier=CommonStringId.TESTING_TEST_BUTTON_TWO
                ),
                on_chosen=_on_option_chosen
            )
        )

        option_dialog.show(
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
    :param include_previous_button: If True, the Previous button will be appended to the end of the dialog. Default is True.
    :type include_previous_button: bool, optional
    :param on_previous: A callback invoked upon the the Previous option being chosen. Default is CommonFunctionUtils.noop.
    :type on_previous: Callable[[], None], optional
    :param on_close: A callback invoked upon the dialog closing. Default is CommonFunctionUtils.noop.
    :type on_close: Callable[[], None], optional
    """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cl_choose_button_option_dialog'

    def __init__(
        self,
        mod_identity: CommonModIdentity,
        title_identifier: Union[int, str, LocalizedString, CommonStringId],
        description_identifier: Union[int, str, LocalizedString, CommonStringId],
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=(),
        include_previous_button: bool=True,
        next_button_text: Union[int, str, LocalizedString, CommonStringId]=CommonStringId.NEXT,
        previous_button_text: Union[int, str, LocalizedString, CommonStringId]=CommonStringId.PREVIOUS,
        on_previous: Callable[[], None]=CommonFunctionUtils.noop,
        on_close: Callable[[], None]=CommonFunctionUtils.noop,
        per_page: int=10
    ):
        super().__init__(
            CommonChooseResponseDialog(
                mod_identity,
                title_identifier,
                description_identifier,
                tuple(),
                next_button_text=next_button_text,
                previous_button_text=previous_button_text,
                title_tokens=title_tokens,
                description_tokens=description_tokens,
                per_page=per_page
            ),
            include_previous_button=include_previous_button,
            on_previous=on_previous,
            on_close=on_close
        )

    def add_option(self, option: CommonDialogButtonOption):
        """add_option(option)

        Add an option to the dialog.

        :param option: The option to add.
        :type option: CommonDialogObjectOption
        """
        return super().add_option(option)

    def _add_response(self, option: CommonDialogButtonOption):
        self._internal_dialog.add_response(option.as_response(len(self._options)))

    def show(
        self,
        dialog_options: UiDialogOption=0,
        sim_info: SimInfo=None,
        target_sim_info: SimInfo=None,
        page: int=1
    ):
        """show(\
            dialog_options=0,\
            sim_info=None,\
            target_sim_info=None,\
            page=1\
        )

        Show the dialog and invoke the callbacks upon the player making a choice.

        :param dialog_options: Options to apply to the dialog, such as removing the close button. Default is no options.
        :type dialog_options: UiDialogOption, optional
        :param sim_info: The SimInfo of the Sim that will appear in the dialog image. The default Sim is the active Sim. Default is None.
        :type sim_info: SimInfo, optional
        :param target_sim_info: If provided, the dialog will appear as if it were a conversation instead of the normal view. Default is None.
        :type target_sim_info: SimInfo, optional
        :param page: The page to show the dialog on. Default is the first page.
        :type page: int, optional
        """
        return super().show(
            dialog_options=dialog_options,
            sim_info=sim_info,
            target_sim_info=target_sim_info,
            page=page
        )

    def build_dialog(
        self,
        dialog_options: UiDialogOption=0,
        sim_info: SimInfo=None,
        target_sim_info: SimInfo=None,
        page: int=1
    ) -> Union[UiDialogBase, None]:
        """build_dialog(\
            dialog_options=0,\
            sim_info=None,\
            target_sim_info=None,\
            page=1\
        )

        Build the dialog and invoke the callbacks upon the player making a choice.

        :param dialog_options: Options to apply to the dialog, such as removing the close button. Default is no options.
        :type dialog_options: UiDialogOption, optional
        :param sim_info: The SimInfo of the Sim that will appear in the dialog image. The default Sim is the active Sim. Default is None.
        :type sim_info: SimInfo, optional
        :param target_sim_info: If provided, the dialog will appear as if it were a conversation instead of the normal view. Default is None.
        :type target_sim_info: SimInfo, optional
        :param page: The page to build the dialog on. Default is the first page.
        :type page: int, optional
        :return: The built dialog or None if a problem occurs.
        :rtype: Union[UiDialogBase, None]
        """
        return super().build_dialog(
            dialog_options=dialog_options,
            sim_info=sim_info,
            page=page
        )


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.show_choose_button_option_dialog',
    'Show an example of CommonChooseButtonOptionDialog.',
    command_arguments=(
        CommonConsoleCommandArgument('target_sim_info', 'Sim Id or Name', 'The name or instance id of a Sim that will be the target of the dialog.', is_optional=True, default_value='No Sim'),
    )
)
def _common_testing_show_choose_button_option_dialog(output: CommonConsoleCommandOutput, target_sim_info: CommonOptionalSimInfoConsoleCommandParameter=None):
    output('Showing test choose button option dialog.')

    def _on_option_chosen(option_identifier: str, choice: str):
        output('Chose option {} with value: {}.'.format(pformat(option_identifier), pformat(choice)))

    def _on_previous_chosen() -> None:
        output('Chose previous option.')

    def _on_close() -> None:
        output('Closed dialog.')

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
    option_dialog = CommonChooseButtonOptionDialog(
        ModInfo.get_identity(),
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        title_tokens=title_tokens,
        description_tokens=description_tokens,
        on_previous=_on_previous_chosen,
        on_close=_on_close,
        per_page=2
    )

    option_dialog.add_option(
        CommonDialogButtonOption(
            'Option 1',
            'Value 1',
            CommonDialogResponseOptionContext(
                CommonStringId.TESTING_SOME_TEXT_FOR_TESTING,
                subtext_identifier=CommonStringId.TESTING_TEST_BUTTON_ONE
            ),
            on_chosen=_on_option_chosen
        )
    )

    option_dialog.add_option(
        CommonDialogButtonOption(
            'Option 2',
            'Value 2',
            CommonDialogResponseOptionContext(
                CommonStringId.TESTING_SOME_TEXT_FOR_TESTING,
                subtext_identifier=CommonStringId.TESTING_TEST_BUTTON_TWO,
            ),
            on_chosen=_on_option_chosen
        )
    )

    option_dialog.add_option(
        CommonDialogButtonOption(
            'Option 3',
            'Value 3',
            CommonDialogResponseOptionContext(
                CommonLocalizationUtils.create_localized_string('Value 3'),
                subtext_identifier=CommonStringId.TESTING_TEST_BUTTON_TWO
            ),
            on_chosen=_on_option_chosen
        )
    )

    option_dialog.show(
        sim_info=CommonSimUtils.get_active_sim_info(),
        target_sim_info=target_sim_info if target_sim_info is not CommonSimUtils.get_active_sim_info() else None
    )
    output('Done showing.')
