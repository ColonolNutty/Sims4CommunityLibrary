"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable

from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_object_option import CommonDialogObjectOption
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.dialogs.common_input_float_dialog import CommonInputFloatDialog


class CommonDialogInputFloatOption(CommonDialogObjectOption):
    """CommonDialogInputFloatOption(\
        option_identifier,\
        initial_value,\
        context,\
        min_value=0.0,\
        max_value=2147483647.0,\
        on_chosen=CommonFunctionUtils.noop,\
        always_visible=False\
    )

    An option to open a dialog to input a float value.

    :param option_identifier: A string that identifies the option from other options.
    :type option_identifier: str
    :param initial_value: The value the option will have initially
    :type initial_value: float
    :param context: A context to customize the dialog option.
    :type context: CommonDialogOptionContext
    :param min_value: The minimum value allowed to be entered.
    :type min_value: float, optional
    :param max_value: The maximum value allowed to be entered.
    :type max_value: float, optional
    :param on_chosen: A callback invoked when the dialog option is chosen. args: (option_identifier, entered value, outcome)
    :type on_chosen: Callable[[str, float, CommonChoiceOutcome], Any], optional
    :param always_visible: If set to True, the option will always appear in the dialog no matter which page.\
    If False, the option will act as normal. Default is False.
    :type always_visible: bool, optional
    """
    def __init__(
        self,
        option_identifier: str,
        initial_value: float,
        context: CommonDialogOptionContext,
        min_value: float=0.0,
        max_value: float=2147483647.0,
        on_chosen: Callable[[str, float, CommonChoiceOutcome], Any]=CommonFunctionUtils.noop,
        always_visible: bool=False
    ):
        self._dialog = CommonInputFloatDialog(
            context.title,
            context.description,
            initial_value,
            min_value=min_value,
            max_value=max_value
        )

        def _on_submit(_: float, __: CommonChoiceOutcome):
            on_chosen(self.option_identifier, _, __)

        def _on_chosen(_, __) -> None:
            self._dialog.show(on_submit=_on_submit)

        super().__init__(
            option_identifier,
            None,
            context,
            on_chosen=_on_chosen,
            always_visible=always_visible
        )

    # noinspection PyMissingOrEmptyDocstring
    @property
    def icon(self) -> Any:
        if super().icon is not None:
            return super().icon
        return CommonIconUtils.load_arrow_right_icon()
