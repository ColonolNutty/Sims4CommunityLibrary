"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import random

from typing import Tuple, Any, Callable, Union, Iterator

from pprint import pformat

from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_choose_dialog import CommonChooseDialog
from sims4communitylib.dialogs.utils.common_dialog_utils import CommonDialogUtils
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog_picker import UiCasItemPicker, ObjectPickerRow


class CommonChooseCASPartDialog(CommonChooseDialog):
    """CommonChooseCASPartDialog(\
        mod_identity,\
        title_identifier,\
        description_identifier,\
        choices,\
        title_tokens=(),\
        description_tokens=(),\
        required_tooltip=None,\
        required_tooltip_tokens=()\
    )

    Create a dialog that prompts the player to choose an object.

    .. note:: To see an example dialog, run the command :class:`s4clib_testing.show_choose_cas_part_dialog` in the in-game console.

    .. highlight:: python
    .. code-block:: python

        def _common_testing_show_choose_cas_part_dialog():
            # LocalizedStrings within other LocalizedStrings
            def _on_chosen(choice: str, outcome: CommonChoiceOutcome):
                pass

            # LocalizedStrings within other LocalizedStrings
            title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
            description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(CommonSimUtils.get_active_sim_info(),), text_color=CommonLocalizedStringColor.BLUE),)

            sim_id = CommonSimUtils.get_sim_id(sim_info)
            cas_parts = list()

            gender = CommonGenderUtils.get_gender(sim_info)

            if CommonGenderUtils.is_male(sim_info):
                cas_parts.append(0x0000BA4F)
                cas_parts.append(0x0000630F)
                cas_parts.append(0x0001F63B)
            else:
                cas_parts.append(0x00005256)
                cas_parts.append(0x0000525A)
                cas_parts.append(0x0000B5C8)

            options = list()
            for cas_part_id in cas_parts:
                options.append(ObjectPickerRow(
                    def_id=cas_part_id,
                    tag=cas_part_id,
                    tag_list=list(),
                    use_catalog_product_thumbnails=False,
                    use_cas_catalog_product_thumbnails=True,
                    cas_catalog_gender=gender,
                    owner_sim_id=sim_id,
                    is_new=False,
                    target_sim_id=sim_id
                ))

            dialog = CommonChooseCASPartDialog(
                ModInfo.get_identity(),
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                tuple(options),
                title_tokens=title_tokens,
                description_tokens=description_tokens
            )
            dialog.show(on_chosen=_on_chosen)

    :param mod_identity: The identity of the mod creating the dialog. See :class:`.CommonModIdentity` for more information.
    :type mod_identity: CommonModIdentity
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
    :param required_tooltip: If provided, this text will display when the dialog requires at least one choice and a choice has not been made. Default is None.
    :type required_tooltip: Union[int, str, LocalizedString, CommonStringId], optional
    :param required_tooltip_tokens: Tokens to format into the required tooltip. Default is an empty collection.
    :type required_tooltip_tokens: Iterator[Any], optional
    """
    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cl_choose_cas_part_dialog'

    def __init__(
        self,
        mod_identity: CommonModIdentity,
        title_identifier: Union[int, str, LocalizedString, CommonStringId],
        description_identifier: Union[int, str, LocalizedString, CommonStringId],
        choices: Iterator[ObjectPickerRow],
        title_tokens: Iterator[Any] = (),
        description_tokens: Iterator[Any] = (),
        required_tooltip: Union[int, str, LocalizedString, CommonStringId] = None,
        required_tooltip_tokens: Iterator[Any] = ()
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

    # noinspection PyMissingOrEmptyDocstring
    @property
    def rows(self) -> Tuple[ObjectPickerRow]:
        result: Tuple[ObjectPickerRow] = super().rows
        return result

    # noinspection PyMissingOrEmptyDocstring
    def add_row(self, choice: ObjectPickerRow, *_, **__):
        """add_row(row, *_, **__)

        Add a row to the dialog.

        :param choice: The row to add.
        :type choice: ObjectPickerRow
        """
        super().add_row(choice, *_, **__)

    def show(
        self,
        on_chosen: Callable[[Any, CommonChoiceOutcome], Any] = CommonFunctionUtils.noop,
        sim_info: SimInfo = None,
        column_count: int = 3,
        show_dropdown_filter: bool = False,
        show_done_button: bool = True,
    ):
        """show(\
            on_chosen=CommonFunctionUtils.noop,\
            sim_info=None,\
            column_count=3,\
            show_dropdown_filter=False,\
            show_done_button=True\
        )

        Show the dialog and invoke the callbacks upon the player making a choice.

        :param on_chosen: A callback invoked upon the player choosing something from the list. Default is CommonFunctionUtils.noop.
        :type on_chosen: Callable[[Any, CommonChoiceOutcome], optional
        :param sim_info: The Sim that will appear in the dialog image. The default Sim is the Active Sim. Default is None.
        :type sim_info: SimInfo, optional
        :param column_count: The number of columns to show the CAS Parts in. Default is 3.
        :type column_count: int, optional
        :param show_dropdown_filter: If True, a dropdown filter will be displayed. If False, a dropdown filter will not be displayed. Default is False.
        :type show_dropdown_filter: bool, optional
        :param show_done_button: If True, the done button will be shown to confirm the selection. If False, a done button will not be shown and simply clicking on a CAS Part will move the dialog forward. Default is True.
        :type show_done_button: bool, optional
        """
        try:
            return self._show(
                on_chosen=on_chosen,
                sim_info=sim_info,
                column_count=column_count,
                show_dropdown_filter=show_dropdown_filter,
                show_done_button=show_done_button,
            )
        except Exception as ex:
            self.log.error('An error occurred while running \'{}\''.format(CommonChooseCASPartDialog.show.__name__), exception=ex)

    def _show(
        self,
        on_chosen: Callable[[Any, CommonChoiceOutcome], bool] = CommonFunctionUtils.noop,
        sim_info: SimInfo = None,
        column_count: int = 3,
        show_dropdown_filter: bool = False,
        show_done_button: bool = True,
    ):
        def _on_chosen(choice: Any, outcome: CommonChoiceOutcome) -> bool:
            try:
                self.log.format_with_message('Choose CAS Part Choice made.', choice=choice)
                result = on_chosen(choice, outcome)
                self.log.format_with_message('Finished handling choose CAS Part _show.', result=result)
                return result
            except Exception as ex:
                self.log.error('Error occurred on choosing a value.', exception=ex)
            return False

        _dialog = self.build_dialog(
            on_chosen=_on_chosen,
            sim_info=sim_info,
            column_count=column_count,
            show_dropdown_filter=show_dropdown_filter,
            show_done_button=show_done_button,
        )
        self.log.debug('Showing dialog.')
        _dialog.show_dialog()

    # noinspection PyMissingOrEmptyDocstring
    def build_dialog(
        self,
        on_chosen: Callable[[Any, CommonChoiceOutcome], bool] = CommonFunctionUtils.noop,
        sim_info: SimInfo = None,
        column_count: int = 3,
        show_dropdown_filter: bool = False,
        show_done_button: bool = True,
    ) -> Union[UiCasItemPicker, None]:
        self.log.format_with_message('Attempting to build dialog.')

        _dialog = self._create_dialog(
            sim_info=sim_info,
            column_count=column_count,
            show_dropdown_filter=show_dropdown_filter,
            show_done_button=show_done_button,
        )
        if _dialog is None:
            self.log.error('_dialog was None for some reason.')
            return

        if on_chosen is None:
            raise ValueError('on_chosen was None.')

        if len(self.rows) == 0:
            raise AssertionError('No rows have been provided. Add rows to the dialog before attempting to display it.')

        def _on_chosen(dialog: UiCasItemPicker) -> bool:
            try:
                self.log.debug('Choice made.')
                if not dialog.accepted:
                    self.log.debug('Dialog cancelled.')
                    return on_chosen(None, CommonChoiceOutcome.CANCEL)
                self.log.debug('Choice not made.')
                choice = CommonDialogUtils.get_chosen_item(dialog)
                self.log.format_with_message('Choose CAS Part Choice made.', choice=pformat(choice))
                result = on_chosen(choice, CommonChoiceOutcome.CHOICE_MADE)
                self.log.format_with_message('Finished handling choose object _on_chosen.', result=result)
                return result
            except Exception as ex:
                self.log.error('Error occurred on choosing a value.', exception=ex)
            return False

        self.log.debug('Adding rows.')
        for row in self.rows:
            _dialog.add_row(row)

        self.log.debug('Adding listener.')
        _dialog.add_listener(_on_chosen)
        return _dialog

    def _create_dialog(
        self,
        sim_info: SimInfo = None,
        min_selectable: int = 1,
        max_selectable: int = 1,
        column_count: int = 3,
        show_dropdown_filter: bool = False,
        show_done_button: bool = True,
    ) -> Union[UiCasItemPicker, None]:
        try:
            self.log.format_with_message(
                'Building dialog.',
                sim_info=sim_info,
                min_selectable=min_selectable,
                max_selectable=max_selectable,
                column_count=column_count,
                show_dropdown_filter=show_dropdown_filter,
                show_done_button=show_done_button
            )
            return UiCasItemPicker.TunableFactory().default(
                sim_info or CommonSimUtils.get_active_sim_info(),
                text=lambda *_, **__: self.description,
                title=lambda *_, **__: self.title,
                min_selectable=min_selectable,
                max_selectable=max_selectable,
                num_columns=column_count,
                use_dropdown_filter=show_dropdown_filter,
                force_done_button=show_done_button
            )
        except Exception as ex:
            self.log.error('_create_dialog', exception=ex)
        return None


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.show_choose_cas_part_dialog',
    'Show an example of CommonChooseCASPartDialog.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Sim to use', is_optional=True, default_value='Active Sim'),
    )
)
def _common_testing_show_choose_cas_part_dialog(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    output(f'Showing test choose CAS Part dialog {sim_info}.')

    def _on_chosen(choice: int, outcome: CommonChoiceOutcome):
        output(f'Chose {choice} with result: {outcome}.')

    # LocalizedStrings within other LocalizedStrings
    title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
    description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(sim_info,), text_color=CommonLocalizedStringColor.BLUE),)

    sim_id = CommonSimUtils.get_sim_id(sim_info)
    cas_parts = list()

    gender = CommonGenderUtils.get_gender(sim_info)

    cas_parts.append(0x00008882)  # yfHat_Bowler_blue

    cas_parts.append(0x0000BA4F)  # ymTop_HoodieSweats_SolidOrangeCream
    cas_parts.append(0x0000630F)  # ymBottom_ShortShorts_GreenLime
    cas_parts.append(0x0001F63B)  # ymBottom_PantsSkinnyCalf_UC_JeansBlue

    cas_parts.append(0x00005256)  # yfBottom_Shorts_GreenArmy
    cas_parts.append(0x0000525A)  # yfBottom_PantsSlacksBootcut_White
    cas_parts.append(0x0000B5C8)  # yfTop_CroppedBow_SolidLtBlue
    cas_parts.append(0x00005257)  # yfBottom_Shorts_GreenArmy
    cas_parts.append(0x0000525B)  # yfBottom_PantsSlacksBootcut_White
    cas_parts.append(0x0000B5C9)  # yfTop_CroppedBow_SolidLtBlue
    cas_parts.append(0x00005258)  # yfBottom_Shorts_GreenArmy
    cas_parts.append(0x00005259)  # yfBottom_Shorts_GreenArmy

    options = list()
    for cas_part_id in cas_parts:
        options.append(ObjectPickerRow(
            def_id=cas_part_id,
            tag=cas_part_id,
            tag_list=list(),
            use_catalog_product_thumbnails=False,
            use_cas_catalog_product_thumbnails=True,
            cas_catalog_gender=gender,
            owner_sim_id=sim_id,
            is_new=False,
            target_sim_id=sim_id,
            is_selected=random.random() > 0.5,
            row_tooltip=CommonLocalizationUtils.create_localized_tooltip(CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN, tooltip_tokens=(str(cas_part_id),)),
        ))

    dialog = CommonChooseCASPartDialog(
        ModInfo.get_identity(),
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        tuple(options),
        title_tokens=title_tokens,
        description_tokens=description_tokens
    )
    dialog.show(sim_info=sim_info, on_chosen=_on_chosen, column_count=4)
    output('Done showing.')
