"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Any, Callable, Union, Iterator

from pprint import pformat
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.choose_object_dialog import CommonChooseObjectDialog
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_dialog_navigation_button_tag import CommonDialogNavigationButtonTag
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_option_category import \
    CommonDialogObjectOptionCategory
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
from ui.ui_dialog_picker import UiObjectPicker, ObjectPickerRow


class CommonChooseObjectsDialog(CommonChooseObjectDialog):
    """CommonChooseObjectsDialog(\
        title_identifier,\
        description_identifier,\
        choices,\
        title_tokens=(),\
        description_tokens=(),\
        per_page=25,\
        mod_identity=None,\
        required_tooltip=None,\
        required_tooltip_tokens=()\
    )

    Create a dialog that prompts the player to choose multiple objects.

    .. note:: To see an example dialog, run the command :class:`s4clib_testing.show_choose_objects_dialog` in the in-game console.

    .. highlight:: python
    .. code-block:: python

        def _common_testing_show_choose_objects_dialog():

            def _on_chosen(choices: Tuple[str], outcome: CommonChoiceOutcome):
                pass

            # LocalizedStrings within other LocalizedStrings
            title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
            description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
            from sims4communitylib.utils.common_icon_utils import CommonIconUtils
            options = [
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
            dialog = CommonChooseObjectsDialog(
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                tuple(options),
                title_tokens=title_tokens,
                description_tokens=description_tokens,
                per_page=2
            )
            dialog.show(on_chosen=_on_chosen, min_selectable=1, max_selectable=2)

    :param title_identifier: The title to display in the dialog.
    :type title_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param description_identifier: The description to display in the dialog.
    :type description_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param choices: The choices that can be chosen.
    :type choices: Iterator[ObjectPickerRow]
    :param title_tokens: Tokens to format into the title.
    :type title_tokens: Iterator[Any], optional
    :param description_tokens: Tokens to format into the description.
    :type description_tokens: Iterator[Any], optional
    :param per_page: The number of rows to display per page. If the number of rows (including rows added after creation) exceeds this value, pagination will be added.
    :type per_page: int
    :param mod_identity: The identity of the mod creating the dialog. See :class:`.CommonModIdentity` for more information.
    :type mod_identity: CommonModIdentity, optional
    :param required_tooltip: If provided, this text will display when the dialog requires at least one choice and a choice has not been made. Default is None.
    :type required_tooltip: Union[int, str, LocalizedString, CommonStringId], optional
    :param required_tooltip_tokens: Tokens to format into the required tooltip. Default is an empty collection.
    :type required_tooltip_tokens: Iterator[Any], optional
    """
    def __init__(
        self,
        title_identifier: Union[int, str, LocalizedString, CommonStringId],
        description_identifier: Union[int, str, LocalizedString, CommonStringId],
        choices: Iterator[ObjectPickerRow],
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=(),
        per_page: int=25,
        mod_identity: CommonModIdentity=None,
        required_tooltip: Union[int, str, LocalizedString, CommonStringId]=None,
        required_tooltip_tokens: Iterator[Any]=()
    ):
        super().__init__(
            title_identifier,
            description_identifier,
            choices,
            title_tokens=title_tokens,
            description_tokens=description_tokens,
            mod_identity=mod_identity,
            required_tooltip=required_tooltip,
            required_tooltip_tokens=required_tooltip_tokens
        )
        if per_page <= 0:
            raise AssertionError('\'per_page\' must be greater than zero.')
        self._per_page = per_page
        self._always_visible_rows = tuple()
        self._current_page = 1

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cl_choose_object_dialog'

    @property
    def current_page(self) -> int:
        """Retrieve the current page.

        :return: A number indicating the current page.
        :rtype: int
        """
        return self._current_page

    # noinspection PyMissingOrEmptyDocstring
    @property
    def rows(self) -> Tuple[ObjectPickerRow]:
        result: Tuple[ObjectPickerRow] = super().rows
        return result

    @property
    def always_visible_rows(self) -> Tuple[ObjectPickerRow]:
        """A collection of rows that will always appear in the dialog no matter which page.

        .. note:: These rows are added to the dialog before the normal rows are added to the dialog.

        :return: A collection of rows added to the dialog that will always appear.
        :rtype: Tuple[ObjectPickerRow]
        """
        return self._always_visible_rows

    # noinspection PyMissingOrEmptyDocstring
    def add_row(self, choice: ObjectPickerRow, *_, always_visible: bool=False, **__):
        """add_row(row, *_, always_on_visible=False, **__)

        Add a row to the dialog.

        :param choice: The row to add.
        :type choice: ObjectPickerRow
        :param always_visible: If set to True, the row will always appear in the dialog no matter which page. If False, the row will act as normal.
        :type always_visible: bool, optional
        """
        if not always_visible:
            super().add_row(choice, *_, **__)
            return
        try:
            self._always_visible_rows += (choice,)
        except Exception as ex:
            self.log.error('An error occurred while running \'{}\''.format(CommonChooseObjectsDialog.add_row.__name__), exception=ex)

    def show(
        self,
        on_chosen: Callable[[Tuple[Any], CommonChoiceOutcome], Any]=CommonFunctionUtils.noop,
        picker_type: UiObjectPicker.UiObjectPickerObjectPickerType=UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT,
        page: int=1,
        sim_info: SimInfo=None,
        categories: Iterator[CommonDialogObjectOptionCategory]=(),
        include_pagination: bool=True,
        min_selectable: int=1,
        max_selectable: int=1,
        sort_rows: bool=False
    ):
        """show(\
            on_chosen=CommonFunctionUtils.noop,\
            picker_type=UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT,\
            page=1,\
            sim_info=None,\
            categories=(),\
            min_selectable=1,\
            max_selectable=1,\
            sort_rows=True\
        )

        Show the dialog and invoke the callbacks upon the player choosing objects.

        :param on_chosen: A callback invoked upon the player choosing something from the list. Default is CommonFunctionUtils.noop.
        :type on_chosen: Callable[[Tuple[Any], CommonChoiceOutcome], optional
        :param picker_type: The layout of the dialog. Default is UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT.
        :type picker_type: UiObjectPicker.UiObjectPickerObjectPickerType, optional
        :param page: The page to display. Ignored if there is only one page of choices. Default is 1.
        :type page: int, optional
        :param sim_info: The Sim that will appear in the dialog image. The default Sim is the Active Sim. Default is None.
        :type sim_info: SimInfo, optional
        :param categories: A collection of categories to display in the dialog. They will appear in a drop down above the rows. Default is an empty collection.
        :type categories: Iterator[CommonDialogObjectOptionCategory], optional
        :param include_pagination: If True, pagination will be applied. If False, no pagination will be applied. Default is True.
        :type include_pagination: bool, optional
        :param min_selectable: The minimum number of items required to be selected. Default is 1.
        :type min_selectable: int, optional
        :param max_selectable: The maximum number of items allowed to be selected. Default is 1.
        :type max_selectable: int, optional
        :param sort_rows: If True, rows will be sorted by display name, with the selected rows on top. If False, rows will not be sorted. Default is False.
        :type sort_rows: bool, optional
        """
        self._current_page = page
        try:
            return self._show(
                on_chosen=on_chosen,
                picker_type=picker_type,
                page=page,
                sim_info=sim_info,
                categories=categories,
                include_pagination=include_pagination,
                min_selectable=min_selectable,
                max_selectable=max_selectable,
                sort_rows=sort_rows
            )
        except Exception as ex:
            self.log.error('An error occurred while running \'{}\''.format(CommonChooseObjectsDialog.show.__name__), exception=ex)

    def _show(
        self,
        on_chosen: Callable[[Tuple[Any], CommonChoiceOutcome], bool]=CommonFunctionUtils.noop,
        picker_type: UiObjectPicker.UiObjectPickerObjectPickerType=UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT,
        page: int=1,
        sim_info: SimInfo=None,
        categories: Iterator[CommonDialogObjectOptionCategory]=(),
        include_pagination: bool=True,
        min_selectable: int=1,
        max_selectable: int=1,
        sort_rows: bool=False
    ):
        def _on_chosen(choices: Tuple[Any], outcome: CommonChoiceOutcome) -> bool:
            try:
                self.log.debug('Choices made {}.'.format(pformat(choices)))
                if CommonDialogNavigationButtonTag.NEXT in choices:
                    self.log.debug('Next chosen.')
                    self.show(
                        on_chosen=on_chosen,
                        picker_type=picker_type,
                        page=page + 1,
                        sim_info=sim_info,
                        categories=categories,
                        min_selectable=min_selectable,
                        max_selectable=max_selectable
                    )
                    return True
                elif CommonDialogNavigationButtonTag.PREVIOUS in choices:
                    self.log.debug('Previous chosen.')
                    self.show(
                        on_chosen=on_chosen,
                        picker_type=picker_type,
                        page=page - 1,
                        sim_info=sim_info,
                        categories=categories,
                        min_selectable=min_selectable,
                        max_selectable=max_selectable
                    )
                    return True
                self.log.format_with_message('Choose Objects Choices made.', choices=pformat(choices))
                result = on_chosen(choices, outcome)
                self.log.format_with_message('Finished handling choose objects _show._on_chosen.', result=result)
                return result
            except Exception as ex:
                self.log.error('Error occurred on choosing a value.', exception=ex)
            return False

        _dialog = self.build_dialog(
            on_chosen=_on_chosen,
            picker_type=picker_type,
            page=page,
            sim_info=sim_info,
            categories=categories,
            min_selectable=min_selectable,
            max_selectable=max_selectable,
            sort_rows=sort_rows
        )
        self.log.debug('Showing dialog.')
        _dialog.show_dialog()

    # noinspection PyMissingOrEmptyDocstring
    def build_dialog(
        self,
        on_chosen: Callable[[Tuple[Any], CommonChoiceOutcome], bool]=CommonFunctionUtils.noop,
        picker_type: UiObjectPicker.UiObjectPickerObjectPickerType=UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT,
        page: int=1,
        sim_info: SimInfo=None,
        categories: Iterator[CommonDialogObjectOptionCategory]=(),
        include_pagination: bool=True,
        min_selectable: int=1,
        max_selectable: int=1,
        sort_rows: bool=False
    ) -> Union[UiObjectPicker, None]:
        self.log.format_with_message('Attempting to build dialog.', page=page, categories=categories)

        _dialog = self._create_dialog(
            picker_type=picker_type,
            categories=categories,
            sim_info=sim_info,
            min_selectable=min_selectable,
            max_selectable=max_selectable,
            sort_rows=sort_rows
        )
        if _dialog is None:
            self.log.error('_dialog was None for some reason.')
            return

        if on_chosen is None:
            raise ValueError('on_chosen was None.')

        if len(self.always_visible_rows) == 0 and len(self.rows) == 0:
            raise AssertionError('No rows have been provided. Add rows to the dialog before attempting to display it.')

        def _on_chosen(dialog: UiObjectPicker) -> bool:
            try:
                if not dialog.accepted:
                    self.log.debug('Dialog cancelled.')
                    return on_chosen(tuple(), CommonChoiceOutcome.CANCEL)
                self.log.debug('Choices not made.')
                choices = CommonDialogUtils.get_chosen_items(dialog)
                self.log.format_with_message('Choose Object Choice made.', choice=pformat(choices))
                result = on_chosen(choices, CommonChoiceOutcome.CHOICE_MADE)
                self.log.format_with_message('Finished handling choose objects _build_dialog._on_chosen.', result=result)
                return result
            except Exception as ex:
                self.log.error('Error occurred on choosing a value.', exception=ex)
            return False

        if include_pagination:
            self._setup_dialog_rows(
                _dialog,
                page=page,
                categories=categories
            )
        else:
            self.log.debug('Adding always visible rows.')
            for always_visible_rows in self.always_visible_rows:
                _dialog.add_row(always_visible_rows)
            self.log.debug('Adding rows.')
            for row in self.rows:
                _dialog.add_row(row)

        self.log.debug('Adding listener.')
        _dialog.add_listener(_on_chosen)
        return _dialog


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.show_choose_objects_dialog',
    'Show an example of CommonChooseObjectsDialog.'
)
def _common_testing_show_choose_objects_dialog(output: CommonConsoleCommandOutput):
    output('Showing test choose objects dialog.')

    def _on_chosen(choices: Tuple[str], outcome: CommonChoiceOutcome):
        output('Chose {} with result: {}.'.format(pformat(choices), pformat(outcome)))

    # LocalizedStrings within other LocalizedStrings
    title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
    description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)
    from sims4communitylib.utils.common_icon_utils import CommonIconUtils
    options = [
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
    dialog = CommonChooseObjectsDialog(
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        tuple(options),
        title_tokens=title_tokens,
        description_tokens=description_tokens,
        per_page=2
    )
    dialog.show(
        on_chosen=_on_chosen,
        min_selectable=1,
        max_selectable=2
    )
    output('Done showing.')
