"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat

import sims4.commands
from typing import Any, Union, Callable, Iterator, Tuple

from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.choose_objects_dialog import CommonChooseObjectsDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_options_dialog import CommonChooseOptionsDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext, \
    DialogOptionValueType
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
from ui.ui_dialog import UiDialogBase
from ui.ui_dialog_picker import UiObjectPicker


class CommonChooseObjectsOptionDialog(CommonChooseOptionsDialog):
    """CommonChooseObjectsOptionDialog(\
        mod_identity,\
        title_identifier,\
        description_identifier,\
        title_tokens=(),\
        description_tokens=(),\
        on_close=CommonFunctionUtils.noop,\
        per_page=25,\
        required_tooltip=None,\
        required_tooltip_tokens=()\
    )

    A dialog that displays a list of options and prompts to select multiple options.

    .. note:: This dialog allows selection of multiple Options.

    .. note:: To see an example dialog, run the command :class:`s4clib_testing.show_choose_objects_option_dialog` in the in-game console.

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        def _on_option_chosen(option_identifier: str, choice: str):
            pass

        def _on_submit(choices: Tuple[str]):
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
        option_dialog = CommonChooseObjectsOptionDialog(
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
            on_submit=_on_submit,
            sim_info=CommonSimUtils.get_active_sim_info()
        )


    :param mod_identity: The identity of the mod creating the dialog. See :class:`.CommonModIdentity` for more information.
    :type mod_identity: CommonModIdentity
    :param title_identifier: A decimal identifier of the title text.
    :type title_identifier: Union[int, LocalizedString]
    :param description_identifier: A decimal identifier of the description text.
    :type description_identifier: Union[int, LocalizedString]
    :param title_tokens: An iterable of Tokens to format into the title. Default is an empty collection.
    :type title_tokens: Iterator[Any], optional
    :param description_tokens: An iterable of Tokens to format into the description. Default is an empty collection.
    :type description_tokens: Iterator[Any], optional
    :param on_close: A callback invoked upon the dialog closing. Default is CommonFunctionUtils.noop.
    :type on_close: Callable[..., Any], optional
    :param per_page: The number of rows to display per page. If the number of rows (including rows added after creation) exceeds this value, pagination will be added. Default is 25.
    :type per_page: int, optional
    :param required_tooltip: If provided, this text will display when the dialog requires at least one choice and a choice has not been made. Default is None.
    :type required_tooltip: Union[int, LocalizedString], optional
    :param required_tooltip_tokens: Tokens to format into the required tooltip. Default is an empty collection.
    :type required_tooltip_tokens: Iterator[Any], optional
    """
    def __init__(
        self,
        title_identifier: Union[int, LocalizedString],
        description_identifier: Union[int, LocalizedString],
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=(),
        on_close: Callable[..., Any]=CommonFunctionUtils.noop,
        mod_identity: CommonModIdentity=None,
        per_page: int=25,
        required_tooltip: Union[int, LocalizedString]=None,
        required_tooltip_tokens: Iterator[Any]=()
    ):
        super().__init__(
            CommonChooseObjectsDialog(
                title_identifier,
                description_identifier,
                tuple(),
                title_tokens=title_tokens,
                description_tokens=description_tokens,
                per_page=per_page,
                mod_identity=mod_identity,
                required_tooltip=required_tooltip,
                required_tooltip_tokens=required_tooltip_tokens
            ),
            on_close=on_close
        )

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cl_choose_objects_option_dialog'

    @property
    def current_page(self) -> int:
        """Retrieve the current page.

        :return: A number indicating the current page.
        :rtype: int
        """
        return self._internal_dialog.current_page

    @property
    def _internal_dialog(self) -> CommonChooseObjectsDialog:
        result: CommonChooseObjectsDialog = super()._internal_dialog
        return result

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
        on_submit: Callable[[Tuple[DialogOptionValueType]], Any]=CommonFunctionUtils.noop,
        picker_type: UiObjectPicker.UiObjectPickerObjectPickerType=UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT,
        page: int=1,
        sim_info: SimInfo=None,
        categories: Iterator[CommonDialogObjectOptionCategory]=(),
        min_selectable: int=1,
        max_selectable: int=1
    ):
        """show(\
            on_submit=CommonFunctionUtils.noop,\
            picker_type=UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT,\
            page=1,\
            sim_info=None,\
            categories=(),\
            min_selectable=1,\
            max_selectable=1\
        )

        Show the dialog and invoke the callbacks upon the player submitting their selection.

        :param on_submit: When the dialog is submitted, this callback will be invoked with the chosen options.
        :type on_submit: Callable[[Tuple[DialogOptionValueType]], Any], optional
        :param picker_type: The layout of the dialog. Default is UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT.
        :type picker_type: UiObjectPicker.UiObjectPickerObjectPickerType, optional
        :param page: The page to display. Ignored if there is only one page of choices. Default is 1.
        :type page: int, optional
        :param sim_info: The SimInfo of the Sim that will appear in the dialog image. If None, it will be the active Sim. Default is None.
        :type sim_info: SimInfo, optional
        :param categories: A collection of categories do display in the dialog. Default is an empty collection.
        :type categories: Iterator[CommonDialogObjectOptionCategory], optional
        :param min_selectable: The minimum number of options that can be chosen.
        :type min_selectable: int, optional
        :param max_selectable: The maximum number of options that can be chosen.
        :type max_selectable: int, optional
        """
        return super().show(
            picker_type=picker_type,
            page=page,
            sim_info=sim_info,
            categories=categories,
            on_submit=on_submit,
            min_selectable=min_selectable,
            max_selectable=max_selectable
        )

    def build_dialog(
        self,
        on_submit: Callable[[Tuple[DialogOptionValueType]], Any]=CommonFunctionUtils.noop,
        picker_type: UiObjectPicker.UiObjectPickerObjectPickerType=UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT,
        page: int=1,
        sim_info: SimInfo=None,
        categories: Iterator[CommonDialogObjectOptionCategory]=(),
        min_selectable: int=1,
        max_selectable: int=1
    ) -> Union[UiDialogBase, None]:
        """build_dialog(\
            on_submit=CommonFunctionUtils.noop,\
            picker_type=UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT,\
            page=1,\
            sim_info=None,\
            categories=(),\
            min_selectable=1,\
            max_selectable=1\
        )

        Build the dialog and invoke the callbacks upon the player submitting their selection.

        :param on_submit: When the dialog is submitted, this callback will be invoked with the chosen options.
        :type on_submit: Callable[[Tuple[DialogOptionValueType]], Any], optional
        :param picker_type: The layout of the dialog. Default is UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT.
        :type picker_type: UiObjectPicker.UiObjectPickerObjectPickerType, optional
        :param page: The page to display. Ignored if there is only one page of choices. Default is 1.
        :type page: int, optional
        :param sim_info: The SimInfo of the Sim that will appear in the dialog image. If None, it will be the active Sim. Default is None.
        :type sim_info: SimInfo, optional
        :param categories: A collection of categories do display in the dialog. Default is an empty collection.
        :type categories: Iterator[CommonDialogObjectOptionCategory], optional
        :param min_selectable: The minimum number of options that can be chosen.
        :type min_selectable: int, optional
        :param max_selectable: The maximum number of options that can be chosen.
        :type max_selectable: int, optional
        :return: The built dialog or None if a problem occurs.
        :rtype: Union[UiDialogBase, None]
        """
        return super().build_dialog(
            picker_type=picker_type,
            page=page,
            sim_info=sim_info,
            categories=categories,
            on_submit=on_submit,
            min_selectable=min_selectable,
            max_selectable=max_selectable
        )


@sims4.commands.Command('s4clib_testing.show_choose_objects_option_dialog', command_type=sims4.commands.CommandType.Live)
def _common_testing_show_choose_objects_option_dialog(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing test choose objects option dialog.')

    def _on_option_chosen(option_identifier: str, choice: str):
        output('Chose option {} with value: {}.'.format(pformat(option_identifier), pformat(choice)))

    def _on_submit(choices: Tuple[str]):
        output('Chose options {}.'.format(pformat(choices)))

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
        option_dialog = CommonChooseObjectsOptionDialog(
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
            on_submit=_on_submit,
            sim_info=CommonSimUtils.get_active_sim_info(),
            min_selectable=1,
            max_selectable=2
        )
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to show dialog', exception=ex)
        output('Failed to show dialog, please locate your exception log file.')
    output('Done showing.')
