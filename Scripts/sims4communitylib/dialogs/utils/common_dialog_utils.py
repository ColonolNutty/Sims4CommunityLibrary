"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Union, Tuple

from ui.ui_dialog_generic import UiDialogTextInput
from ui.ui_dialog_multi_picker import UiMultiPicker
from ui.ui_dialog_picker import UiDialogObjectPicker, UiCasItemPicker


class CommonDialogUtils:
    """Utilities for use with dialogs.

    """
    TEXT_INPUT_NAME = 'text_input'

    @staticmethod
    def get_chosen_item(dialog: Union[UiDialogObjectPicker, UiMultiPicker, UiCasItemPicker]) -> Any:
        """get_chosen_item(dialog)

        Retrieves the item chosen by the player from a dialog.

        :param dialog: The dialog to get the chosen item of.
        :type dialog: Union[UiDialogObjectPicker, UiMultiPicker]
        :return: The value of the chosen item.
        :rtype: Any
        """
        if isinstance(dialog, UiCasItemPicker) and hasattr(dialog, 'get_result_definitions_and_counts'):
            (ids, _) = dialog.get_result_definitions_and_counts()
            return ids[-1] or ids[0]
        return dialog.get_result_tags()[-1] or dialog.get_result_tags()[0]

    @staticmethod
    def get_chosen_items(dialog: Union[UiDialogObjectPicker, UiMultiPicker, UiCasItemPicker]) -> Tuple[Any]:
        """get_chosen_items(dialog)

        Retrieves the items chosen by the player from a dialog.

        :param dialog: The dialog to get the chosen items of.
        :type dialog: Union[UiDialogObjectPicker, UiMultiPicker]
        :return: A collection of chosen items.
        :rtype: Tuple[Any]
        """
        if isinstance(dialog, UiCasItemPicker) and hasattr(dialog, 'get_result_definitions_and_counts'):
            (ids, _) = dialog.get_result_definitions_and_counts()
            return ids
        return dialog.get_result_tags()

    @staticmethod
    def get_input_value(dialog: UiDialogTextInput) -> Union[str, None]:
        """get_input_value(dialog)

        Retrieve the value entered by the player from an input dialog.

        :param dialog: The dialog to get the chosen items of.
        :type dialog: UiDialogTextInput
        :return: The value of the entered input.
        :rtype: Union[str, None]
        """
        return str(dialog.text_input_responses.get(CommonDialogUtils.TEXT_INPUT_NAME))
