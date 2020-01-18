"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Union, Tuple

from ui.ui_dialog_generic import UiDialogTextInput
from ui.ui_dialog_multi_picker import UiMultiPicker
from ui.ui_dialog_picker import UiDialogObjectPicker


class CommonDialogUtils:
    """ Utilities for use with dialogs. """
    @staticmethod
    def get_chosen_item(dialog: Union[UiDialogObjectPicker, UiMultiPicker]) -> Any:
        """ Retrieves the item chosen by the player from a dialog. """
        return dialog.get_result_tags()[-1] or dialog.get_result_tags()[0]

    @staticmethod
    def get_chosen_items(dialog: Union[UiDialogObjectPicker, UiMultiPicker]) -> Tuple[Any]:
        """ Retrieves the items chosen by the player from a dialog. """
        return dialog.get_result_tags()

    @staticmethod
    def get_input_value(dialog: UiDialogTextInput) -> Union[str, None]:
        """ Retrieve the value entered by the player from an input dialog. """
        return str(dialog.text_input_responses.get('text_input'))
