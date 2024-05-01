"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Tuple, Union, Iterator

from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.dialogs.option_dialogs.common_choose_objects_option_dialog import CommonChooseObjectsOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_action_option import \
    CommonDialogActionOption
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import \
    CommonDialogSelectOption
from sims4communitylib.enums.common_sim_demographic_types import CommonSimDemographicType
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.logging._has_s4cl_log import _HasS4CLLog
from sims4communitylib.utils.common_collection_utils import CommonCollectionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor


class CommonChooseSimDemographicTypesDialog(_HasS4CLLog):
    """CommonChooseSimDemographicTypesDialog(\
        on_close,\
        available_values=None,\
        exclude_values=None\
    )

    Open a dialog that prompts the player to choose from Sim Demographic Types.

    :param on_close: A callback invoked upon the dialog closing.
    :type on_close: Callable[[], None]
    :param available_values: The available values shown in the dialog. Default is all Values.
    :type available_values: Iterator[CommonSimDemographicType], optional
    :param exclude_values: The demographics to not display in the dialog. Default is all Values will be available.
    :type exclude_values: Iterator[CommonSimDemographicType], optional
    """
    def __init__(
        self,
        on_close: Callable[[], None],
        available_values: Iterator[CommonSimDemographicType] = None,
        exclude_values: Iterator[CommonSimDemographicType] = None
    ):
        super().__init__()
        self._on_close = on_close
        self._exclude_values = tuple(exclude_values) if exclude_values else None
        self._available_values = tuple(available_values or CommonSimDemographicType.get_all(exclude_values=self._exclude_values))

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'common_choose_sim_demographic_types_dialog'

    def open(
        self,
        title: Union[int, CommonStringId, LocalizedString],
        description: Union[int, CommonStringId, LocalizedString],
        current_selections: Tuple[CommonSimDemographicType],
        on_submit: Callable[[Tuple[CommonSimDemographicType]], None],
        include_all_choice: bool = True,
        include_none_choice: bool = True,
        reopen_on_submit: bool = True
    ) -> None:
        """open(\
            title,\
            description,\
            current_selections,\
            on_submit,\
            include_all_choice=True,\
            include_none_choice=True,\
            reopen_on_submit=True\
        )

        Open the dialog.

        :param title: The title to show at the top of the dialog.
        :type title: Union[int, CommonStringId, LocalizedString]
        :param description: The description to show at the top of the dialog.
        :type description: Union[int, CommonStringId, LocalizedString]
        :param current_selections: The currently selected options in the dialog.
        :type current_selections: Tuple[CommonSimDemographicType]
        :param on_submit: A callback invoked upon submitting the dialog.
        :type on_submit: Callable[[Tuple[CommonSimDemographicType]], None]
        :param include_all_choice: If True, the "All Sims" choice will be shown to players. If False, the "All Sims" choice will not be shown. Default is True.
        :type include_all_choice: bool, optional
        :param include_none_choice: If True, the "No Sims" choice will be shown to players. If False, the "No Sims" choice will not be shown. Default is True.
        :type include_none_choice: bool, optional
        :param reopen_on_submit: If True, the dialog will reopen on submit. If False, the dialog will not reopen on submit. Default is True.
        :type reopen_on_submit: bool, optional
        """
        def _on_close() -> None:
            if self._on_close is not None:
                self._on_close()

        def _reopen(_current_selections: Tuple[CommonSimDemographicType] = None) -> None:
            if _current_selections is None:
                _current_selections = current_selections
            self.open(
                title,
                description,
                _current_selections,
                on_submit,
                include_all_choice=include_all_choice,
                include_none_choice=include_none_choice,
                reopen_on_submit=reopen_on_submit
            )

        self.log.format_with_message('Choosing Sim demographic types.', current_selections=current_selections)

        if not current_selections:
            current_val_localized_string = CommonStringId.S4CL_NO_SIMS
        else:
            current_val_localized_string = None
            for current_value in current_selections:
                _display_name = CommonSimDemographicType.to_display_name(current_value)
                if current_val_localized_string is None:
                    current_val_localized_string = _display_name
                    continue
                current_val_localized_string = CommonLocalizationUtils.create_localized_string(CommonStringId.STRING_COMMA_SPACE_STRING, tokens=(
                    current_val_localized_string,
                    _display_name
                ))

        option_dialog = CommonChooseObjectsOptionDialog(
            title,
            description,
            title_tokens=(
                CommonLocalizationUtils.colorize(current_val_localized_string, text_color=CommonLocalizedStringColor.GREEN),
            ),
            on_close=_on_close,
            mod_identity=self.mod_identity,
            per_page=500
        )

        def _on_submit(_types: Tuple[CommonSimDemographicType]):
            if _types is None:
                _on_close()
                return
            if CommonStringId.S4CL_ALL_SIMS.name in _types:
                on_submit(self._available_values)
                if reopen_on_submit:
                    _reopen(_current_selections=self._available_values)
                return
            if CommonStringId.S4CL_NO_SIMS.name in _types:
                on_submit(tuple())
                if reopen_on_submit:
                    _reopen(_current_selections=tuple())
                return
            on_submit(_types)
            if reopen_on_submit:
                _reopen(_current_selections=_types)

        if include_all_choice:
            option_dialog.add_option(
                CommonDialogSelectOption(
                    'ChooseAllSims',
                    CommonStringId.S4CL_ALL_SIMS.name,
                    CommonDialogOptionContext(
                        CommonStringId.S4CL_ALL_SIMS,
                        CommonStringId.S4CL_ALL_OPTIONS_WILL_BE_INCLUDED,
                        icon=CommonIconUtils.load_arrow_right_icon()
                    )
                )
            )

        if include_none_choice:
            option_dialog.add_option(
                CommonDialogSelectOption(
                    'ChooseNoSims',
                    CommonStringId.S4CL_NO_SIMS.name,
                    CommonDialogOptionContext(
                        CommonStringId.S4CL_NO_SIMS,
                        CommonStringId.S4CL_NO_OPTIONS_WILL_BE_INCLUDED,
                        icon=CommonIconUtils.load_arrow_right_icon()
                    )
                )
            )

        for setting_type in self._available_values:
            display_name = CommonLocalizationUtils.create_localized_string(CommonSimDemographicType.to_display_name(setting_type))
            icon = CommonIconUtils.load_unchecked_square_icon()
            is_selected = setting_type in current_selections
            if is_selected:
                icon = CommonIconUtils.load_checked_square_icon()
            option_dialog.add_option(
                CommonDialogSelectOption(
                    setting_type.name,
                    setting_type,
                    CommonDialogOptionContext(
                        display_name,
                        CommonSimDemographicType.to_display_description(setting_type),
                        icon=icon,
                        is_selected=is_selected
                    )
                )
            )

        if not option_dialog.has_options():
            _on_close()
            return

        option_dialog.show(
            min_selectable=0,
            max_selectable=option_dialog.option_count,
            allow_no_selection=True,
            on_submit=_on_submit
        )

    def create_dialog_option(
        self,
        option_id: str,
        title: Union[int, CommonStringId, LocalizedString],
        description: Union[int, CommonStringId, LocalizedString],
        current_values: Tuple[CommonSimDemographicType],
        on_chosen: Callable[[str, Tuple[CommonSimDemographicType]], None]
    ):
        """Create a dialog option."""
        def _open_choose_sim_demographics_dialog() -> None:
            self.open(title, description, current_values, lambda val: on_chosen(option_id, val))

        if not current_values:
            current_val_localized_string = CommonStringId.S4CL_NO_SIMS
        else:
            if CommonCollectionUtils.lists_are_equal(sorted(current_values), sorted(self._available_values)):
                current_val_localized_string = CommonStringId.S4CL_ALL_SIMS
            else:
                current_val_localized_string = None
                for current_value in current_values:
                    display_name = CommonSimDemographicType.to_display_name(current_value)
                    if current_val_localized_string is None:
                        current_val_localized_string = display_name
                        continue
                    current_val_localized_string = CommonLocalizationUtils.create_localized_string(CommonStringId.STRING_COMMA_SPACE_STRING, tokens=(
                        current_val_localized_string,
                        display_name
                    ))

        return CommonDialogActionOption(
            CommonDialogOptionContext(
                title,
                description,
                title_tokens=(
                    CommonLocalizationUtils.colorize(CommonLocalizationUtils.create_localized_string(current_val_localized_string), text_color=CommonLocalizedStringColor.GREEN),
                )
            ),
            on_chosen=_open_choose_sim_demographics_dialog
        )
