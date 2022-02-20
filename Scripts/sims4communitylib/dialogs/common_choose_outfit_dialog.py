"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Any, Callable, Union, Iterator, List

from pprint import pformat

from protocolbuffers.Localization_pb2 import LocalizedString
from sims.outfits.outfit_enums import OutfitCategory, HIDDEN_OUTFIT_CATEGORIES
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_choose_dialog import CommonChooseDialog
from sims4communitylib.dialogs.utils.common_dialog_utils import CommonDialogUtils
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog_picker import OutfitPickerRow, UiOutfitPicker


class CommonChooseOutfitDialog(CommonChooseDialog):
    """CommonChooseOutfitDialog(\
        mod_identity,\
        title_identifier,\
        description_identifier,\
        title_tokens=(),\
        description_tokens=(),\
        required_tooltip=None,\
        required_tooltip_tokens=()\
    )

    Create a dialog that allows the player to choose an outfit from a Sims currently available outfits.

    .. note:: To see an example dialog, run the command :class:`s4clib_testing.show_choose_outfit_dialog` in the in-game console.

    .. highlight:: python
    .. code-block:: python

        def _common_testing_show_choose_outfit_dialog():
            def _on_chosen(choice: Tuple[OutfitCategory, int], outcome: CommonChoiceOutcome):
                output('Chose {} with result: {}.'.format(pformat(choice), pformat(outcome)))

            try:
                sim_info = CommonSimUtils.get_active_sim_info()
                # LocalizedStrings within other LocalizedStrings
                title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
                description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(sim_info,), text_color=CommonLocalizedStringColor.BLUE),)
                from sims4communitylib.utils.common_icon_utils import CommonIconUtils
                dialog = CommonChooseOutfitDialog(
                    ModInfo.get_identity(),
                    CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                    CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                    title_tokens=title_tokens,
                    description_tokens=description_tokens
                )
                outfit_list = (OutfitCategory.EVERYDAY, 0)
                dialog.show(sim_info, outfit_list=outfit_list, on_chosen=_on_chosen)
            except Exception as ex:
                CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to show dialog', exception=ex)
                output('Failed to show dialog, please locate your exception log file.')
            output('Done showing.')

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
    :param required_tooltip: If provided, this text will display when the dialog requires at least one choice and a choice has not been made. Default is None.
    :type required_tooltip: Union[int, str, LocalizedString, CommonStringId], optional
    :param required_tooltip_tokens: Tokens to format into the required tooltip. Default is an empty collection.
    :type required_tooltip_tokens: Iterator[Any], optional
    """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'common_choose_outfit_dialog'

    def __init__(
        self,
        mod_identity: CommonModIdentity,
        title_identifier: Union[int, str, LocalizedString, CommonStringId],
        description_identifier: Union[int, str, LocalizedString, CommonStringId],
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=(),
        required_tooltip: Union[int, str, LocalizedString, CommonStringId]=None,
        required_tooltip_tokens: Iterator[Any]=()
    ):
        super().__init__(
            title_identifier,
            description_identifier,
            tuple(),
            title_tokens=title_tokens,
            description_tokens=description_tokens,
            mod_identity=mod_identity,
            required_tooltip=required_tooltip,
            required_tooltip_tokens=required_tooltip_tokens
        )

    # noinspection PyMissingOrEmptyDocstring
    @property
    def rows(self) -> Tuple[OutfitPickerRow]:
        result: Tuple[OutfitPickerRow] = super().rows
        return result

    # noinspection PyMissingOrEmptyDocstring
    def add_row(self, choice: OutfitPickerRow, *_, **__):
        """add_row(row, *_, **__)

        Add a row to the dialog.

        :param choice: The row to add.
        :type choice: OutfitPickerRow
        """
        super().add_row(choice, *_, **__)

    def show(
        self,
        sim_info: SimInfo,
        outfit_list: Iterator[Tuple[OutfitCategory, int]]=(),
        thumbnail_type: UiOutfitPicker._OutftiPickerThumbnailType=UiOutfitPicker._OutftiPickerThumbnailType.SIM_INFO,
        on_chosen: Callable[[Union[Tuple[OutfitCategory, int], None], CommonChoiceOutcome], None]=CommonFunctionUtils.noop,
        exclude_outfit_categories: Tuple[OutfitCategory]=(OutfitCategory.CURRENT_OUTFIT, OutfitCategory.BATHING, *HIDDEN_OUTFIT_CATEGORIES),
        show_filter: bool=True,
        allow_choose_current_outfit: bool=False
    ):
        """show(\
            sim_info,
            outfit_list=(),\
            thumbnail_type=UiOutfitPicker._OutftiPickerThumbnailType.SIM_INFO,\
            on_chosen=CommonFunctionUtils.noop,\
            exclude_outfit_categories=(OutfitCategory.CURRENT_OUTFIT, OutfitCategory.BATHING, OutfitCategory.SPECIAL, OutfitCategory.CAREER, OutfitCategory.SITUATION, OutfitCategory.BATUU),\
            show_filter=True,\
            allow_choose_current_outfit=False\
        )

        Show the dialog and invoke the callbacks upon the player making a choice.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param outfit_list: A collection of outfits. Default is all Outfits.
        :type outfit_list: Iterator[Tuple[OutfitCategory, int]], optional
        :param thumbnail_type: Determines how the thumbnails of the outfits should be displayed. Default is UiOutfitPicker._OutftiPickerThumbnailType.SIM_INFO
        :type thumbnail_type: UiObjectPicker._OutftiPickerThumbnailType, optional
        :param on_chosen: A callback invoked upon the player choosing something from the list. Default is CommonFunctionUtils.noop.
        :type on_chosen: Callable[[Union[Tuple[OutfitCategory, int], None], CommonChoiceOutcome], None], optional
        :param exclude_outfit_categories: A collection of Outfit Categories to exclude from display. Default is CURRENT_OUTFIT, BATHING, SPECIAL, CAREER, SITUATION, BATUU
        :type exclude_outfit_categories: Tuple[OutfitCategory], optional
        :param show_filter: Whether or not to show the Outfit Category filters in the dialogue. Default is True.
        :type show_filter: bool, optional
        :param allow_choose_current_outfit: If True, then the Outfit that is currently being worn will be allowed to be chosen. If False, the current outfit cannot be chosen. Default is False.
        :type allow_choose_current_outfit: bool, optional
        """
        try:
            outfit_list = self._setup_outfit_list(outfit_list, exclude_outfit_categories)
            return self._show(
                sim_info,
                outfit_list=outfit_list,
                thumbnail_type=thumbnail_type,
                on_chosen=on_chosen,
                show_filter=show_filter,
                allow_choose_current_outfit=allow_choose_current_outfit,
            )
        except Exception as ex:
            self.log.error('An error occurred while running \'{}\''.format(self.show.__name__), exception=ex)

    def _setup_outfit_list(
        self,
        outfit_list: Iterator[Tuple[OutfitCategory, int]],
        exclude_outfit_categories: Tuple[OutfitCategory]
    ) -> Tuple[Tuple[OutfitCategory, int]]:
        if outfit_list:
            return tuple(outfit_list)
        outfit_list: List[Tuple[OutfitCategory, int]] = list()
        for outfit_category in OutfitCategory.values:
            if outfit_category in exclude_outfit_categories:
                continue
            outfit_index = 0
            while outfit_index < CommonOutfitUtils.get_maximum_number_of_outfits_for_category(outfit_category):
                outfit_list.append((outfit_category, outfit_index))
                outfit_index += 1
        return tuple(outfit_list)

    def _show(
        self,
        sim_info: SimInfo,
        outfit_list: Iterator[Tuple[OutfitCategory, int]]=(),
        thumbnail_type: UiOutfitPicker._OutftiPickerThumbnailType=UiOutfitPicker._OutftiPickerThumbnailType.SIM_INFO,
        on_chosen: Callable[[Union[Tuple[OutfitCategory, int], None], CommonChoiceOutcome], None]=CommonFunctionUtils.noop,
        show_filter: bool=True,
        allow_choose_current_outfit: bool=False
    ):
        def _on_chosen(choice: Tuple[OutfitCategory, int], outcome: CommonChoiceOutcome) -> None:
            try:
                self.log.format_with_message('Choose Outfit Choice made.', choice=choice)
                on_chosen(choice, outcome)
                self.log.debug('Finished handling choose object _show.')
                return
            except Exception as ex:
                self.log.error('Error occurred on choosing a value.', exception=ex)

        _dialog = self.build_dialog(
            sim_info,
            outfit_list=outfit_list,
            thumbnail_type=thumbnail_type,
            on_chosen=_on_chosen,
            show_filter=show_filter,
            allow_choose_current_outfit=allow_choose_current_outfit
        )
        self.log.debug('Showing dialog.')
        _dialog.show_dialog()

    # noinspection PyMissingOrEmptyDocstring
    def build_dialog(
        self,
        sim_info: SimInfo,
        outfit_list: Iterator[Tuple[OutfitCategory, int]]=(),
        thumbnail_type: UiOutfitPicker._OutftiPickerThumbnailType=UiOutfitPicker._OutftiPickerThumbnailType.SIM_INFO,
        on_chosen: Callable[[Union[Tuple[OutfitCategory, int], None], CommonChoiceOutcome], None]=CommonFunctionUtils.noop,
        show_filter: bool=True,
        allow_choose_current_outfit: bool=False
    ) -> Union[UiOutfitPicker, None]:
        self.log.format_with_message(
            'Attempting to build dialog.',
            sim=sim_info,
            outfit_list=outfit_list,
            thumbnail_type=thumbnail_type
        )

        _dialog = self._create_dialog(
            sim_info,
            outfit_list=outfit_list,
            thumbnail_type=thumbnail_type,
            show_filter=show_filter
        )
        if _dialog is None:
            self.log.error('_dialog was None for some reason.')
            return

        if on_chosen is None:
            raise ValueError('on_chosen was None.')

        def _on_chosen(dialog: UiOutfitPicker) -> None:
            try:
                self.log.format_with_message('Choice made.', picked_results=dialog.picked_results)
                if not dialog.accepted:
                    self.log.debug('Dialog cancelled.')
                    on_chosen(None, CommonChoiceOutcome.CANCEL)
                    return
                self.log.format_with_message('Dialog accepted, checking if choices were made.')
                choice = CommonDialogUtils.get_chosen_item(dialog)
                self.log.format_with_message('Outfit choice made.', choice=choice)
                on_chosen(choice, CommonChoiceOutcome.CHOICE_MADE)
                self.log.debug('Finished handling outfit items _on_chosen.')
                return
            except Exception as ex:
                self.log.error('Error occurred on choosing a value.', exception=ex)

        self._setup_dialog_rows(
            sim_info,
            _dialog,
            outfit_list=outfit_list,
            allow_choose_current_outfit=allow_choose_current_outfit
        )

        self.log.debug('Adding listener.')
        _dialog.add_listener(_on_chosen)
        return _dialog

    def _setup_dialog_rows(
        self,
        sim_info: SimInfo,
        _dialog: UiOutfitPicker,
        outfit_list: Iterator[Tuple[OutfitCategory, int]]=(),
        allow_choose_current_outfit: bool=False
    ):
        self.log.debug('Adding rows.')
        sim_id = CommonSimUtils.get_sim_id(sim_info)
        added_rows = False
        current_outfit = CommonOutfitUtils.get_current_outfit(sim_info)
        for (outfit_category, outfit_index) in outfit_list:
            # noinspection PyTypeChecker
            if not CommonOutfitUtils.has_outfit(sim_info, (outfit_category, outfit_index)) and not CommonOutfitUtils.has_outfit(sim_info, (int(outfit_category), outfit_index)):
                self.log.format_with_message('Sim does not have outfit.', sim=sim_info, outfit_category_and_index=(outfit_category, outfit_index))
                continue
            added_rows = True
            _dialog.add_row(
                OutfitPickerRow(
                    sim_id,
                    outfit_category,
                    outfit_index,
                    # For some reason the Outfit Picker uses "is_enable" to determine which outfit is currently selected, instead of the expected "is_selected".
                    is_enable=(outfit_category, outfit_index) != current_outfit if not allow_choose_current_outfit else True,
                    tag=(outfit_category, outfit_index)
                )
            )

        for row in self.rows:
            _dialog.add_row(row)

        if not added_rows and len(self.rows) == 0:
            raise AssertionError('No rows have been provided. Add rows to the dialog before attempting to display it.')

    def _create_dialog(
        self,
        target_sim_info: SimInfo,
        outfit_list: Iterator[Tuple[OutfitCategory, int]],
        thumbnail_type: UiOutfitPicker._OutftiPickerThumbnailType=UiOutfitPicker._OutftiPickerThumbnailType.SIM_INFO,
        show_filter: bool=True
    ) -> Union[UiOutfitPicker, None]:
        try:
            outfit_categories: List[OutfitCategory] = list()
            for (outfit_category, outfit_index) in outfit_list:
                if outfit_category not in outfit_categories:
                    outfit_categories.append(outfit_category)

            dialog = UiOutfitPicker.TunableFactory()\
                .default(
                    target_sim_info or CommonSimUtils.get_active_sim_info(),
                    text=lambda *_, **__: self.description,
                    title=lambda *_, **__: self.title,
                    outfit_categories=set([outfit[0] for outfit in outfit_list]),
                    thumbnail_type=thumbnail_type,
                    show_filter=show_filter
                )
            dialog.outfit_category_filters = outfit_categories
            return dialog
        except Exception as ex:
            self.log.error('_create_dialog', exception=ex)
        return None


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.show_choose_outfit_dialog',
    'Show an example of CommonChooseResponseDialog.'
)
def _common_testing_show_choose_outfit_dialog(output: CommonConsoleCommandOutput):
    output('Showing test choose outfit dialog.')

    def _on_chosen(choice: Tuple[OutfitCategory, int], outcome: CommonChoiceOutcome):
        output('Chose {} with result: {}.'.format(pformat(choice), pformat(outcome)))

    sim_info = CommonSimUtils.get_active_sim_info()
    # LocalizedStrings within other LocalizedStrings
    title_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_SOME_TEXT_FOR_TESTING, text_color=CommonLocalizedStringColor.GREEN),)
    description_tokens = (CommonLocalizationUtils.create_localized_string(CommonStringId.TESTING_TEST_TEXT_WITH_SIM_FIRST_AND_LAST_NAME, tokens=(sim_info,), text_color=CommonLocalizedStringColor.BLUE),)
    dialog = CommonChooseOutfitDialog(
        ModInfo.get_identity(),
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
        title_tokens=title_tokens,
        description_tokens=description_tokens
    )
    outfit_list = ((OutfitCategory.EVERYDAY, 0),)
    dialog.show(sim_info, outfit_list=outfit_list, on_chosen=_on_chosen)
    output('Done showing.')
