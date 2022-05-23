"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable

from objects.components.state import ObjectState
from objects.game_object import GameObject
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_select_option import \
    CommonDialogSelectOption
from sims4communitylib.dialogs.option_dialogs.common_choose_object_option_dialog import CommonChooseObjectOptionDialog
from sims4communitylib.logging._has_s4cl_log import _HasS4CLLog
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.objects.common_object_state_utils import CommonObjectStateUtils
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils


class CommonChangeObjectStateDialog(_HasS4CLLog):
    """ Open a dialog that allows changing the states of objects. """

    def __init__(self, game_object: GameObject, on_close: Callable[[], None] = None):
        super().__init__()
        self._game_object = game_object
        self._on_close = on_close

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'common_change_object_state_dialog'

    def open(self) -> None:
        """ Open Dialog. """
        def _reopen() -> None:
            self.open()

        def _on_close() -> None:
            if self._on_close is not None:
                self._on_close()

        option_dialog = CommonChooseObjectOptionDialog(
            CommonObjectUtils.get_catalog_name(self._game_object),
            0,
            on_close=_on_close,
            mod_identity=self.mod_identity,
            per_page=500
        )

        def _on_state_chosen(_: str, _chosen_state: ObjectState):
            if _chosen_state is None:
                _on_close()
                return
            self._modify_object_state_dialog(_chosen_state, on_close=_reopen)

        for (object_state, object_state_value) in CommonObjectStateUtils.get_object_state_items(self._game_object).items():
            display_name = CommonLocalizationUtils.create_localized_string(f'{object_state}: {object_state_value}')
            option_dialog.add_option(
                CommonDialogSelectOption(
                    str(object_state),
                    object_state,
                    CommonDialogOptionContext(
                        display_name,
                        0,
                        icon=CommonIconUtils.load_arrow_right_icon()
                    ),
                    on_chosen=_on_state_chosen
                )
            )

        option_dialog.show(sort_options=True)

    def _modify_object_state_dialog(self, object_state: ObjectState, on_close: Callable[[], None]):
        def _on_close() -> None:
            on_close()

        option_dialog = CommonChooseObjectOptionDialog(
            CommonObjectUtils.get_catalog_name(self._game_object),
            0,
            on_close=_on_close,
            mod_identity=self.mod_identity,
            per_page=500
        )

        def _on_state_chosen(_: str, _chosen_state: ObjectState):
            if _chosen_state is None:
                _on_close()
                return
            CommonObjectStateUtils.set_object_state(self._game_object, _chosen_state)
            _on_close()

        current_object_state_value = CommonObjectStateUtils.get_current_object_state(self._game_object, object_state)
        for object_state_value in object_state.values:
            display_name = CommonLocalizationUtils.create_localized_string(str(object_state_value))
            icon = CommonIconUtils.load_unfilled_circle_icon()
            if object_state_value == current_object_state_value:
                icon = CommonIconUtils.load_filled_circle_icon()
            option_dialog.add_option(
                CommonDialogSelectOption(
                    str(object_state_value),
                    object_state_value,
                    CommonDialogOptionContext(
                        display_name,
                        0,
                        icon=icon
                    ),
                    on_chosen=_on_state_chosen
                )
            )

        option_dialog.show(sort_options=True)
