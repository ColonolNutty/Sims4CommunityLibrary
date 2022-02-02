"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Any, Callable, Union

from pprint import pformat
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.dialogs.utils.common_dialog_utils import CommonDialogUtils
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog_picker import UiObjectPicker, ObjectPickerRow


class CommonChooseItemResult(CommonInt):
    """Different outcomes upon the player choosing or not choosing items in the dialog.

    """
    DIALOG_CANCELLED: 'CommonChooseItemResult' = 0
    ITEM_CHOSEN: 'CommonChooseItemResult' = 1
    ITEM_CHOSEN_WITH_ERROR: 'CommonChooseItemResult' = 2

    @staticmethod
    def is_error(result: 'CommonChooseItemResult') -> bool:
        """is_error(result)

        Determine if a result is an error or cancel.

        :param result: The result to check
        :type result: CommonChooseItemResult
        :return: True, if the result is an error or cancelled. False, if not.
        :rtype: bool
        """
        return result == CommonChooseItemResult.DIALOG_CANCELLED or result == CommonChooseItemResult.ITEM_CHOSEN_WITH_ERROR


class CommonChooseItemDialog:
    """CommonChooseItemDialog(\
        title_identifier,\
        description_identifier,\
        list_items,\
        title_tokens=(),\
        description_tokens=()\
    )

    Create a dialog that prompts the player to choose an item.

    .. warning:: Obsolete: Please use :class:`.CommonChooseObjectDialog` instead.
        Use to create a dialog that prompts the player to choose a single item from a list of items.

    .. note:: To see an example dialog, run the command :class:`s4clib_testing.show_choose_item_dialog` in the in-game console.

    .. highlight:: python
    .. code-block:: python

        def _common_testing_show_choose_item_dialog():

            def _item_chosen(chosen_item: str, result: CommonChooseItemResult):
                pass

            # LocalizedStrings within other LocalizedStrings
            title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
            description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
            from sims4communitylib.utils.common_icon_utils import CommonIconUtils
            options = [ObjectPickerRow(option_id=1, name=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING),
                                       row_description=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_ONE),
                                       row_tooltip=None,
                                       icon=CommonIconUtils.load_checked_square_icon(),
                                       tag='Value 1'),
                       ObjectPickerRow(option_id=2, name=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING),
                                       row_description=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_TWO),
                                       row_tooltip=None,
                                       icon=CommonIconUtils.load_arrow_navigate_into_icon(),
                                       tag='Value 2')]
            dialog = CommonChooseItemDialog(CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                                            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                                            tuple(options),
                                            title_tokens=title_tokens,
                                            description_tokens=description_tokens)
            dialog.show(on_item_chosen=_item_chosen)

    :param title_identifier: A decimal identifier of the title text.
    :type title_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param description_identifier: A decimal identifier of the description text.
    :type description_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param list_items: The items to display in the dialog.
    :type list_items: Tuple[ObjectPickerRow]
    :param title_tokens: Tokens to format into the title.
    :type title_tokens: Tuple[Any], optional
    :param description_tokens: Tokens to format into the description.
    :type description_tokens: Tuple[Any], optional
    """
    def __init__(
        self,
        title_identifier: Union[int, str, LocalizedString, CommonStringId],
        description_identifier: Union[int, str, LocalizedString, CommonStringId],
        list_items: Tuple[ObjectPickerRow],
        title_tokens: Tuple[Any]=(),
        description_tokens: Tuple[Any]=()
    ):
        self.title = CommonLocalizationUtils.create_localized_string(title_identifier, tokens=title_tokens)
        self.description = CommonLocalizationUtils.create_localized_string(description_identifier, tokens=description_tokens)
        self.list_items = list_items

    def add_item(self, item: ObjectPickerRow):
        """add_item(item)

        Add a new item to choose from.

        :param item: The item to add.
        :type item: ObjectPickerRow
        """
        self.list_items += (item,)

    def show(
        self,
        on_item_chosen: Callable[[Any, CommonChooseItemResult], Any]=CommonFunctionUtils.noop,
        picker_type: UiObjectPicker.UiObjectPickerObjectPickerType=UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT
    ):
        """show(\
            on_item_chosen=CommonFunctionUtils.noop,\
            picker_type=UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT\
        )

        Show the dialog and invoke the callbacks upon the player selecting an item.

        :param on_item_chosen: Invoked upon the player choosing an item from the list.
        :type on_item_chosen: Callable[[Any, CommonChooseItemResult], Any], optional
        :param picker_type: Determines how the items appear in the dialog.
        :type picker_type: UiObjectPicker.UiObjectPickerObjectPickerType, optional
        """
        _dialog = self._create_dialog(picker_type=picker_type)
        if _dialog is None:
            return

        def _on_item_chosen(dialog: UiObjectPicker):
            if not dialog.accepted:
                return on_item_chosen(None, CommonChooseItemResult.DIALOG_CANCELLED)
            chosen_item = CommonDialogUtils.get_chosen_item(dialog)
            return on_item_chosen(chosen_item, CommonChooseItemResult.ITEM_CHOSEN)

        for list_item in self.list_items:
            _dialog.add_row(list_item)

        _dialog.add_listener(_on_item_chosen)
        _dialog.show_dialog()

    def _create_dialog(self, picker_type: UiObjectPicker.UiObjectPickerObjectPickerType=UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT) -> Union[UiObjectPicker, None]:
        return UiObjectPicker.TunableFactory().default(CommonSimUtils.get_active_sim_info(),
                                                       text=lambda *_, **__: self.description,
                                                       title=lambda *_, **__: self.title,
                                                       min_selectable=1,
                                                       max_selectable=1,
                                                       picker_type=picker_type)


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.show_choose_item_dialog',
    'Show an example of CommonChooseItemDialog.',
    show_with_help_command=False
)
def _common_testing_show_choose_item_dialog(output: CommonConsoleCommandOutput):
    output('Showing test choose item dialog.')

    def _item_chosen(chosen_item: str, result: CommonChooseItemResult):
        output('Item chosen {} with result: {}.'.format(pformat(chosen_item), pformat(result)))

    # LocalizedStrings within other LocalizedStrings
    title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
    description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
    from sims4communitylib.utils.common_icon_utils import CommonIconUtils
    options = [ObjectPickerRow(option_id=1, name=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING),
                               row_description=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_ONE),
                               row_tooltip=None,
                               icon=CommonIconUtils.load_checked_square_icon(),
                               tag='Value 1'),
               ObjectPickerRow(option_id=2, name=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING),
                               row_description=CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_BUTTON_TWO),
                               row_tooltip=None,
                               icon=CommonIconUtils.load_arrow_navigate_into_icon(),
                               tag='Value 2')]
    dialog = CommonChooseItemDialog(CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                                    CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                                    tuple(options),
                                    title_tokens=title_tokens,
                                    description_tokens=description_tokens)
    dialog.show(on_item_chosen=_item_chosen)
    output('Done showing.')
