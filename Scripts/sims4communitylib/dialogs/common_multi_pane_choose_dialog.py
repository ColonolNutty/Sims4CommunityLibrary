"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import random
from pprint import pformat

import sims4.commands
from typing import Tuple, Any, Callable, Union, Iterator, List, Dict
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.choose_object_dialog import CommonChooseObjectDialog
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_choose_dialog import CommonChooseDialog
from sims4communitylib.dialogs.common_choose_sim_dialog import CommonChooseSimDialog
from sims4communitylib.dialogs.common_dialog import CommonDialog
from sims4communitylib.dialogs.utils.common_dialog_utils import CommonDialogUtils
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ui.ui_dialog import UiDialogBase
from ui.ui_dialog_picker import ObjectPickerRow, SimPickerRow
from protocolbuffers.Dialog_pb2 import UiDialogMessage, UiDialogMultiPicker
from ui.ui_dialog_multi_picker import UiMultiPicker

log = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'thing')
log.enable()


class CommonUiMultiPicker(UiMultiPicker):
    """A multi picker dialog. """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.disabled_tooltips: Dict[Any, LocalizedString] = dict()

    def build_msg(self, **kwargs) -> Any:
        """ Build the message for display. """
        message = super().build_msg(**kwargs)
        # noinspection PyUnresolvedReferences
        message.dialog_type = UiDialogMessage.MULTI_PICKER
        multi_picker_msg = UiDialogMultiPicker()
        for dialog in self._picker_dialogs.values():
            new_message = dialog.build_msg()
            # noinspection PyUnresolvedReferences
            multi_picker_item = multi_picker_msg.multi_picker_items.add()
            log.debug(pformat(dir(multi_picker_item)))
            multi_picker_item.picker_data = new_message.picker_data
            log.format(picker_data=pformat(dir(multi_picker_item.picker_data)))
            multi_picker_item.picker_id = new_message.dialog_id
            multi_picker_item.disabled_tooltip = self.disabled_tooltips.get(new_message.dialog_id, None) or CommonLocalizationUtils.create_localized_string('')
        message.multi_picker_data = multi_picker_msg
        return message


class CommonMultiPaneChooseDialog(CommonDialog):
    """CommonMultiPaneChooseDialog(\
        mod_identity=None,\
        title_identifier,\
        description_identifier,\
        title_tokens=(),\
        description_tokens=()\
    )

    Create a multi-pane dialog that prompts the player to choose from multiple dialogs and submit their choices.

    .. note:: To see an example dialog, run the command :class:`s4clib_testing.show_multi_pane_choose_dialog` in the in-game console.

    .. highlight:: python
    .. code-block:: python

        def _common_testing_show_multi_pane_choose_dialog():


            def _on_submit(choices_made: Tuple[Any], outcome: CommonChoiceOutcome) -> None:
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

            dialog = CommonMultiPaneChooseDialog(
                ModInfo.get_identity(),
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                title_tokens=title_tokens,
                description_tokens=description_tokens
            )

            # Add a number of sub dialogs to the multi-pane dialog.
            count = 0
            while count < 2:
                count += 1
                sub_dialog = CommonChooseObjectDialog(
                    CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                    CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                    tuple(options),
                    title_tokens=title_tokens,
                    description_tokens=description_tokens,
                    per_page=2
                )

                dialog.add_sub_dialog(sub_dialog, on_chosen=lambda *_, **__: output('Dialog {} choice: {} and outcome: {}'.format(count, pformat(_), pformat(__))))
            dialog.show(on_submit=_on_submit)

    :param title_identifier: The title to display in the dialog.
    :type title_identifier: Union[int, LocalizedString]
    :param description_identifier: The description to display in the dialog.
    :type description_identifier: Union[int, LocalizedString]
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
        title_identifier: Union[int, LocalizedString],
        description_identifier: Union[int, LocalizedString],
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
        return 's4cl_multi_pane_choose_object_dialog'

    def add_sub_dialog(self, sub_dialog: CommonChooseDialog, *dialog_arguments: Any, **dialog_keyword_arguments: Any):
        """add_sub_dialog(sub_dialog, on_chosen=CommonFunctionUtils.noop)

        Add a sub dialog to the dialog.

        :param sub_dialog: An instance of a dialog.
        :type sub_dialog: CommonChooseDialog
        :param dialog_arguments: Arguments to pass to the sub dialog when building it.
        :type dialog_arguments: Any
        :param dialog_keyword_arguments: Keyword arguments to pass to the sub dialog when building.
        :type dialog_keyword_arguments: Any
        """
        self._sub_dialogs += ((sub_dialog, dialog_arguments, dialog_keyword_arguments), )

    def show(
        self,
        on_submit: Callable[[Tuple[Any], CommonChoiceOutcome], Any]=CommonFunctionUtils.noop,
        sim_info: SimInfo=None
    ):
        """show(\
            on_submit=CommonFunctionUtils.noop,\
            sim_info=None\
        )

        Show the dialog and invoke the callbacks upon the player making a choice.

        :param on_submit: A callback invoked upon the player submitting the dialog and the choices within it. Default is CommonFunctionUtils.noop.
        :type on_submit: Callable[[Tuple[Any], CommonChoiceOutcome], Any], optional
        :param sim_info: The Sim that will appear in the dialog image. The default Sim is the Active Sim. Default is None.
        :type sim_info: SimInfo, optional
        """
        try:
            return self._show(
                on_submit=on_submit,
                sim_info=sim_info
            )
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity, 'An error occurred while running \'{}\''.format(CommonMultiPaneChooseDialog.show.__name__), exception=ex)

    def _show(
        self,
        on_submit: Callable[[Tuple[Any], CommonChoiceOutcome], Any]=CommonFunctionUtils.noop,
        sim_info: SimInfo=None
    ):
        self.log.debug('Attempting to display multi picker dialog.')
        dialog = self._build_dialog(
            on_submit=on_submit,
            sim_info=sim_info
        )
        dialog.show_dialog()

    def _build_dialog(
        self,
        on_submit: Callable[[Tuple[Any], CommonChoiceOutcome], Any]=CommonFunctionUtils.noop,
        sim_info: SimInfo=None
    ):
        self.log.format(ui_dialog_message_dir=dir(UiDialogMessage))
        dialog = self._create_dialog(sim_info=sim_info)
        if dialog is None:
            self.log.error('dialog was None for some reason.')
            return

        if on_submit is None:
            raise AssertionError('on_chosen was None.')

        if len(self._sub_dialogs) == 0:
            raise AssertionError('No sub dialogs have been added. Add sub dialogs to the dialog before attempting to display it.')

        @CommonExceptionHandler.catch_exceptions(self.mod_identity.name)
        def _on_submit(_dialog: CommonUiMultiPicker):
            if not _dialog.accepted:
                self.log.debug('Dialog cancelled.')
                return on_submit(tuple(), CommonChoiceOutcome.CANCEL)
            made_choices: bool = CommonDialogUtils.get_chosen_items(_dialog)
            if not made_choices:
                self.log.debug('No choices made. Cancelling dialog.')
                return on_submit(tuple(), CommonChoiceOutcome.CANCEL)
            self.log.debug('Choices made, combining choices.')
            chosen_items: List[Any] = list()
            for _sub_dialog_submit_id in _dialog._picker_dialogs:
                _sub_dialog_submit = _dialog._picker_dialogs[_sub_dialog_submit_id]
                for choice in CommonDialogUtils.get_chosen_items(_sub_dialog_submit):
                    chosen_items.append(choice)
            self.log.format_with_message('Choices were made.', choice=made_choices)
            result = on_submit(tuple(chosen_items), CommonChoiceOutcome.CHOICE_MADE)
            self.log.format_with_message('Finished handling choice.', result=result)
            return result

        for (sub_dialog, sub_dialog_arguments, sub_dialog_keyword_arguments) in self._sub_dialogs:
            sub_dialog: CommonChooseDialog = sub_dialog
            # noinspection PyBroadException
            try:
                if 'include_pagination' not in sub_dialog_keyword_arguments:
                    _sub_dialog: UiDialogBase = sub_dialog._build_dialog(
                        *sub_dialog_arguments,
                        include_pagination=False,
                        **sub_dialog_keyword_arguments
                    )
                else:
                    _sub_dialog: UiDialogBase = sub_dialog._build_dialog(
                        *sub_dialog_arguments,
                        **sub_dialog_keyword_arguments
                    )
            except:
                _sub_dialog: UiDialogBase = sub_dialog._build_dialog(
                    *sub_dialog_arguments,
                    **sub_dialog_keyword_arguments
                )
            if _sub_dialog is None:
                continue
            dialog.disabled_tooltips[_sub_dialog.dialog_id] = sub_dialog.disabled_tooltip
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
            CommonExceptionHandler.log_exception(self.mod_identity, '_create_dialog', exception=ex)
        return None


@sims4.commands.Command('s4clib_testing.show_multi_pane_choose_dialog', command_type=sims4.commands.CommandType.Live)
def _common_testing_show_multi_pane_choose_dialog(_connection: int=None):
    output = sims4.commands.CheatOutput(_connection)
    output('Showing test multi-pane choose dialog.')

    def _on_sim_chosen(choice: Union[SimInfo, None], outcome: CommonChoiceOutcome):
        output('Chose {} with result: {}.'.format(CommonSimNameUtils.get_full_name(choice), pformat(outcome)))

    def _on_submit(choices_made: Tuple[Any], outcome: CommonChoiceOutcome) -> None:
        output('On Submit choices_made: {} and outcome: {}'.format(pformat(choices_made), pformat(outcome)))

    try:
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
        dialog = CommonMultiPaneChooseDialog(
            ModInfo.get_identity(),
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            title_tokens=title_tokens,
            description_tokens=description_tokens
        )
        # Add a number of sub dialogs to the multi-pane dialog.
        object_count = 0
        while object_count < 2:
            object_count += 1
            sub_dialog = CommonChooseObjectDialog(
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
                tuple(options),
                title_tokens=title_tokens,
                description_tokens=description_tokens,
                per_page=2
            )

            dialog.add_sub_dialog(sub_dialog, on_chosen=lambda *_, **__: output('Dialog {} choice: {} and outcome: {}'.format(object_count, pformat(_), pformat(__))))

        current_count = 0
        count = 25
        sim_options = []
        for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
            if current_count >= count:
                break
            sim_id = CommonSimUtils.get_sim_id(sim_info)
            should_select = random.choice((True, False))
            is_enabled = random.choice((True, False))
            sim_options.append(
                SimPickerRow(
                    sim_id=sim_id,
                    select_default=should_select,
                    tag=sim_info,
                    is_enable=is_enabled
                )
            )
            current_count += 1

        sub_sim_dialog = CommonChooseSimDialog(
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            CommonStringId.TESTING_TEST_TEXT_WITH_STRING_TOKEN,
            tuple(sim_options),
            title_tokens=title_tokens,
            description_tokens=description_tokens
        )

        dialog.add_sub_dialog(sub_sim_dialog, on_chosen=_on_sim_chosen, column_count=5)
        # Show the dialog.
        dialog.show(on_submit=_on_submit)
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to show dialog', exception=ex)
        output('Failed to show dialog, please locate your exception log file.')
    output('Done showing.')
