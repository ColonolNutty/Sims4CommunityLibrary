"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat

import sims4.commands
from typing import Any, Union, Callable, Iterator

from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.choose_object_dialog import CommonChooseObjectDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_option_dialog import CommonChooseOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_option_category import \
    CommonDialogObjectOptionCategory
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_object_option import CommonDialogObjectOption
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog_picker import UiObjectPicker


class CommonChooseObjectOptionDialog(CommonChooseOptionDialog):
    """CommonChooseObjectOptionDialog(\
        title_identifier,\
        description_identifier,\
        title_tokens=(),\
        description_tokens=(),\
        on_close=CommonFunctionUtils.noop,\
        mod_identity=None,\
        per_page=25\
    )

    A dialog that displays a list of options.

    .. note:: To see an example dialog, run the command :class:`s4clib_testing.show_choose_object_option_dialog` in the in-game console.

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        def _on_option_chosen(option_identifier: str, choice: str):
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

        # Create the dialog and only showing 2 options per page.
        option_dialog = CommonChooseObjectOptionDialog(
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            title_tokens=title_tokens,
            description_tokens=description_tokens,
            per_page=2
        )

        from sims4communitylib.utils.common_icon_utils import CommonIconUtils

        # We add the options, in this case we have three options.
        option_dialog.add_option(
            CommonDialogObjectOption(
                'Option 1',
                'Value 1',
                CommonDialogOptionContext(
                    CommonStringId.TESTING_SOME_TEXT_FOR_TESTING,
                    CommonStringId.TESTING_TEST_BUTTON_ONE,
                    icon=CommonIconUtils.load_checked_square_icon()
                ),
                on_chosen=_on_option_chosen
            )
        )

        option_dialog.add_option(
            CommonDialogObjectOption(
                'Option 2',
                'Value 2',
                CommonDialogOptionContext(
                    CommonStringId.TESTING_SOME_TEXT_FOR_TESTING,
                    CommonStringId.TESTING_TEST_BUTTON_TWO,
                    icon=CommonIconUtils.load_arrow_navigate_into_icon()
                ),
                on_chosen=_on_option_chosen
            )
        )

        option_dialog.add_option(
            CommonDialogObjectOption(
                'Option 3',
                'Value 3',
                CommonDialogOptionContext(
                    CommonLocalizationUtils.create_localized_string('Value 3'),
                    CommonStringId.TESTING_TEST_BUTTON_TWO,
                    icon=CommonIconUtils.load_arrow_navigate_into_icon()
                ),
                on_chosen=_on_option_chosen
            )
        )

        option_dialog.show(
            sim_info=CommonSimUtils.get_active_sim_info()
        )


    :param title_identifier: A decimal identifier of the title text.
    :type title_identifier: Union[int, LocalizedString]
    :param description_identifier: A decimal identifier of the description text.
    :type description_identifier: Union[int, LocalizedString]
    :param title_tokens: An iterable of Tokens to format into the title.
    :type title_tokens: Iterator[Any], optional
    :param description_tokens: An iterable of Tokens to format into the description.
    :type description_tokens: Iterator[Any], optional
    :param on_close: A callback invoked upon the dialog closing.
    :type on_close: Callable[..., Any], optional
    :param mod_identity: The identity of the mod creating the dialog. See :class:`.CommonModIdentity` for more information.
    :type mod_identity: CommonModIdentity, optional
    :param per_page: The number of rows to display per page. If the number of rows (including rows added after creation) exceeds this value, pagination will be added.
    :type per_page: int, optional
    """
    def __init__(
        self,
        title_identifier: Union[int, LocalizedString],
        description_identifier: Union[int, LocalizedString],
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=(),
        on_close: Callable[..., Any]=CommonFunctionUtils.noop,
        mod_identity: CommonModIdentity=None,
        per_page: int=25
    ):
        super().__init__(
            CommonChooseObjectDialog(
                title_identifier,
                description_identifier,
                tuple(),
                title_tokens=title_tokens,
                description_tokens=description_tokens,
                per_page=per_page,
                mod_identity=mod_identity
            ),
            on_close=on_close
        )

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cl_choose_object_option_dialog'

    @property
    def current_page(self) -> int:
        """Retrieve the current page.

        :return: A number indicating the current page.
        :rtype: int
        """
        dialog: CommonChooseObjectDialog = self._internal_dialog
        return dialog.current_page

    def add_option(self, option: CommonDialogObjectOption):
        """add_option(option)

        Add an option to the dialog.

        :param option: The option to add.
        :type option: CommonDialogObjectOption
        """
        return super().add_option(option)

    def _add_row(self, option: CommonDialogObjectOption):
        self._internal_dialog.add_row(option.as_row(len(self._options)), always_visible=option.always_visible)

    def show(
        self,
        picker_type: UiObjectPicker.UiObjectPickerObjectPickerType=UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT,
        page: int=1,
        sim_info: SimInfo=None,
        categories: Iterator[CommonDialogObjectOptionCategory]=()
    ):
        """show(\
            picker_type=UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT,\
            page=1,\
            sim_info=None\
        )

        Show the dialog and invoke the callbacks upon the player making a choice.

        :param picker_type: The layout of the dialog.
        :type picker_type: UiObjectPicker.UiObjectPickerObjectPickerType, optional
        :param page: The page to display. Ignored if there is only one page of choices.
        :type page: int, optional
        :param sim_info: The SimInfo of the Sim that will appear in the dialog image. The default Sim is the active Sim.
        :type sim_info: SimInfo, optional
        :param categories: A collection of categories do display in the dialog.
        :type categories: Iterator[CommonDialogObjectOptionCategory]
        """
        return super().show(
            picker_type=picker_type,
            page=page,
            sim_info=sim_info,
            categories=categories
        )


@sims4.commands.Command('s4clib_testing.show_choose_object_option_dialog', command_type=sims4.commands.CommandType.Live)
def _common_testing_show_choose_object_option_dialog(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing test choose object option dialog.')

    def _on_option_chosen(option_identifier: str, choice: str):
        output('Chose option {} with value: {}.'.format(pformat(option_identifier), pformat(choice)))

    try:
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
        option_dialog = CommonChooseObjectOptionDialog(
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            title_tokens=title_tokens,
            description_tokens=description_tokens,
            per_page=2
        )

        from sims4communitylib.utils.common_icon_utils import CommonIconUtils

        option_dialog.add_option(
            CommonDialogObjectOption(
                'Option 1',
                'Value 1',
                CommonDialogOptionContext(
                    CommonStringId.TESTING_SOME_TEXT_FOR_TESTING,
                    CommonStringId.TESTING_TEST_BUTTON_ONE,
                    icon=CommonIconUtils.load_checked_square_icon()
                ),
                on_chosen=_on_option_chosen
            )
        )

        option_dialog.add_option(
            CommonDialogObjectOption(
                'Option 2',
                'Value 2',
                CommonDialogOptionContext(
                    CommonStringId.TESTING_SOME_TEXT_FOR_TESTING,
                    CommonStringId.TESTING_TEST_BUTTON_TWO,
                    icon=CommonIconUtils.load_arrow_navigate_into_icon()
                ),
                on_chosen=_on_option_chosen
            )
        )

        option_dialog.add_option(
            CommonDialogObjectOption(
                'Option 3',
                'Value 3',
                CommonDialogOptionContext(
                    CommonLocalizationUtils.create_localized_string('Value 3'),
                    CommonStringId.TESTING_TEST_BUTTON_TWO,
                    icon=CommonIconUtils.load_arrow_navigate_into_icon()
                ),
                on_chosen=_on_option_chosen
            )
        )

        option_dialog.show(
            sim_info=CommonSimUtils.get_active_sim_info()
        )
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to show dialog', exception=ex)
        output('Failed to show dialog, please locate your exception log file.')
    output('Done showing.')
