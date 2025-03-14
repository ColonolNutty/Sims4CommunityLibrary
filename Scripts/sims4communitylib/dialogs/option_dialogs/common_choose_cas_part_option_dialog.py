"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import random
from typing import Any, Union, Callable, Iterator, List

from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.choose_cas_part_dialog import CommonChooseCASPartDialog
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.option_dialogs.common_choose_option_dialog import CommonChooseOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_cas_part_option import \
    CommonDialogCASPartOption
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_cas_part_option_context import \
    CommonDialogCASPartOptionContext
from sims4communitylib.dtos.common_cas_part import CommonCASPart
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from ui.ui_dialog import UiDialogBase


class CommonChooseCASPartOptionDialog(CommonChooseOptionDialog):
    """CommonChooseCASPartOptionDialog(\
        mod_identity,\
        title_identifier,\
        description_identifier,\
        title_tokens=(),\
        description_tokens=(),\
        on_close=CommonFunctionUtils.noop,\
        required_tooltip=None,\
        required_tooltip_tokens=()\
    )

    A dialog that displays a list of CAS Parts for selection.

    .. note:: To see an example dialog, run the command :class:`s4clib_testing.show_choose_cas_part_option_dialog` in the in-game console.

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        def _on_chosen(_cas_part: CommonCASPart):
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

        # Create the dialog and show a number of Sims in 4 columns.
        option_dialog = CommonChooseCASPartOptionDialog(
            ModInfo.get_identity(),
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            title_tokens=title_tokens,
            description_tokens=description_tokens
        )

        cas_parts = list()

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

        for cas_part_id in cas_parts:
            should_select = random.choice((True, False))
            option_dialog.add_option(
                CommonDialogCASPartOption(
                    CommonCASPart(cas_part_id),
                    sim_info,
                    CommonDialogCASPartOptionContext(
                        tooltip_text_identifier=CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                        tooltip_tokens=(str(cas_part_id),),
                        is_selected=should_select
                    ),
                    on_chosen=_on_chosen
                )
            )

        option_dialog.show(
            sim_info=CommonSimUtils.get_active_sim_info(),
            column_count=7
        )

    :param mod_identity: The identity of the mod creating the dialog. See :class:`.CommonModIdentity` for more information.
    :type mod_identity: CommonModIdentity
    :param title_identifier: A decimal identifier of the title text.
    :type title_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param description_identifier: A decimal identifier of the description text.
    :type description_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param title_tokens: An iterator of Tokens to format into the title.
    :type title_tokens: Iterator[Any], optional
    :param description_tokens: An iterator of Tokens to format into the description.
    :type description_tokens: Iterator[Any], optional
    :param on_close: A callback invoked upon the dialog closing.
    :type on_close: Callable[[], None], optional
    :param required_tooltip: If provided, this text will display when the dialog requires at least one choice and a choice has not been made. Default is None.
    :type required_tooltip: Union[int, str, LocalizedString, CommonStringId], optional
    :param required_tooltip_tokens: Tokens to format into the required tooltip. Default is an empty collection.
    :type required_tooltip_tokens: Iterator[Any], optional
    """
    def __init__(
        self,
        mod_identity: CommonModIdentity,
        title_identifier: Union[int, str, LocalizedString, CommonStringId],
        description_identifier: Union[int, str, LocalizedString, CommonStringId],
        title_tokens: Iterator[Any] = (),
        description_tokens: Iterator[Any] = (),
        on_close: Callable[[], None] = CommonFunctionUtils.noop,
        required_tooltip: Union[int, str, LocalizedString, CommonStringId] = None,
        required_tooltip_tokens: Iterator[Any] = ()
    ):
        super().__init__(
            CommonChooseCASPartDialog(
                mod_identity,
                title_identifier,
                description_identifier,
                tuple(),
                title_tokens=title_tokens,
                description_tokens=description_tokens,
                required_tooltip=required_tooltip,
                required_tooltip_tokens=required_tooltip_tokens
            ),
            on_close=on_close
        )

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 's4cl_choose_cas_part_option_dialog'

    def add_option(self, option: CommonDialogCASPartOption):
        """add_option(option)

        Add an option to the dialog.

        :param option: The option to add.
        :type option: CommonDialogCASPartOption
        """
        return super().add_option(option)

    def show(
        self,
        sim_info: SimInfo = None,
        column_count: int = 3,
        show_dropdown_filter: bool = False,
        show_done_button: bool = True,
    ):
        """show(sim_info=None, column_count=3, show_dropdown_filter=False, show_done_button=True)

        Show the dialog.

        :param sim_info: The SimInfo of the Sim that will appear in the dialog image. The default Sim is the active Sim.
        :type sim_info: SimInfo, optional
        :param column_count: The number of columns to display CAS Parts in. Default is 3.
        :type column_count: int, optional
        :param show_dropdown_filter: If True, a dropdown filter will be displayed. If False, a dropdown filter will not be displayed. Default is False.
        :type show_dropdown_filter: bool, optional
        :param show_done_button: If True, the done button will be shown to confirm the selection. If False, a done button will not be shown and simply clicking on a CAS Part will move the dialog forward. Default is True.
        :type show_done_button: bool, optional
        """
        return super().show(
            sim_info=sim_info,
            column_count=column_count,
            show_dropdown_filter=show_dropdown_filter,
            show_done_button=show_done_button
        )

    def build_dialog(
        self,
        sim_info: SimInfo = None,
        column_count: int = 3,
        show_dropdown_filter: bool = False,
        show_done_button: bool = True
    ) -> Union[UiDialogBase, None]:
        """build_dialog(sim_info=None, column_count=3, show_dropdown_filter=False, show_done_button=True)

        Build the dialog.

        :param sim_info: The SimInfo of the Sim that will appear in the dialog image. The default Sim is the active Sim. Default is None.
        :type sim_info: SimInfo, optional
        :param column_count: The number of columns to display CAS Parts in. Default is 3.
        :type column_count: int, optional
        :param show_dropdown_filter: If True, a dropdown filter will be displayed. If False, a dropdown filter will not be displayed. Default is False.
        :type show_dropdown_filter: bool, optional
        :param show_done_button: If True, the done button will be shown to confirm the selection. If False, a done button will not be shown and simply clicking on a CAS Part will move the dialog forward. Default is True.
        :type show_done_button: bool, optional
        :return: The built dialog or None if a problem occurs.
        :rtype: Union[UiDialogBase, None]
        """
        return super().build_dialog(
            sim_info=sim_info,
            column_count=column_count,
            show_dropdown_filter=show_dropdown_filter,
            show_done_button=show_done_button
        )

    def _on_chosen(self) -> Callable[[int, CommonChoiceOutcome], bool]:
        def _on_chosen(chosen_option: int, outcome: CommonChoiceOutcome) -> bool:
            try:
                if chosen_option is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                    self.close()
                    return False
                # We have to do this, because for whatever reason the CAS Part dialog gives us the def_id instead of the tag, even though in most cases it treats them the same.
                # This is difficult because swatches are not something we are adding to the dialog. The game is deciding to add them itself.
                matching_option = None
                options: List[CommonDialogCASPartOption] = self._options
                for option in options:
                    option: CommonDialogCASPartOption = option
                    if option.value.cas_part_id == chosen_option:
                        matching_option = option
                        break
                if matching_option is None:
                    return options[0].on_chosen(CommonCASPart(chosen_option))
                return matching_option.choose()
            except Exception as ex:
                self.log.error('Error occurred on choosing a value.', exception=ex)
            return False
        return _on_chosen


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.show_choose_cas_part_option_dialog',
    'Show an example of CommonChooseCASPartOptionDialog.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Sim to use', is_optional=True, default_value='Active Sim'),
    )
)
def _common_testing_show_choose_cas_part_option_dialog(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    output('Showing test choose cas part option dialog.')

    def _on_chosen(_cas_part: CommonCASPart):
        output(f'Chose CAS Part {_cas_part}')

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
            tokens=(sim_info,),
            text_color=CommonLocalizedStringColor.BLUE
        ),
    )

    # Create the dialog and show a number of Sims in 4 columns.
    option_dialog = CommonChooseCASPartOptionDialog(
        ModInfo.get_identity(),
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        title_tokens=title_tokens,
        description_tokens=description_tokens
    )

    cas_parts = list()

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

    for cas_part_id in cas_parts:
        should_select = random.choice((True, False))
        option_dialog.add_option(
            CommonDialogCASPartOption(
                CommonCASPart(cas_part_id),
                sim_info,
                CommonDialogCASPartOptionContext(
                    tooltip_text_identifier=CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                    tooltip_tokens=(str(cas_part_id),),
                    is_selected=should_select
                ),
                on_chosen=_on_chosen
            )
        )

    option_dialog.show(
        sim_info=sim_info,
        column_count=7
    )
    output('Done showing.')
