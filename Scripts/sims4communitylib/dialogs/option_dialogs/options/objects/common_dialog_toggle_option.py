"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable, Union

from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_object_option import \
    CommonDialogObjectOption, DialogOptionIdentifierType


class CommonDialogToggleOption(CommonDialogObjectOption):
    """CommonDialogObjectOption(option_identifier, value, context, on_chosen=CommonFunctionUtils.noop, always_visible=False)

    An option with two states, on or off.

    :param option_identifier: A string that identifies the option from other options.
    :type option_identifier: DialogOptionIdentifierType
    :param value: The value of the option.
    :type value: bool
    :param context: A context to customize the dialog option.
    :type context: CommonDialogOptionContext
    :param on_chosen: A callback invoked when the dialog option is chosen. The values are as follows: (option_identifier, not value)
    :type on_chosen: Callable[[DialogOptionIdentifierType, bool], None], optional
    :param always_visible: If set to True, the option will always appear in the dialog no matter which page.\
    If False, the option will act as normal. Default is False.
    :type always_visible: bool, optional
    """
    def __init__(
        self,
        option_identifier: DialogOptionIdentifierType,
        value: Union[bool, CommonExecutionResult],
        context: CommonDialogOptionContext,
        on_chosen: Callable[[DialogOptionIdentifierType, bool], None]=CommonFunctionUtils.noop,
        always_visible: bool=False
    ):
        if isinstance(value, CommonExecutionResult):
            value = bool(value.result)
        super().__init__(option_identifier, value, context, on_chosen=on_chosen, always_visible=always_visible)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def icon(self) -> Any:
        if super().icon is not None:
            return super().icon
        if self.value:
            return CommonIconUtils.load_checked_square_icon()
        return CommonIconUtils.load_unchecked_square_icon()

    @property
    def value(self) -> bool:
        """The value of the option.

        :return: The value of the option.
        :rtype: bool
        """
        return self._value

    @property
    def on_chosen(self) -> Callable[[bool], Any]:
        """The action to perform upon choosing this option.

        :return: The action to perform upon choosing this option.
        :rtype: Callable[[bool], Any]
        """
        return super().on_chosen

    # noinspection PyMissingOrEmptyDocstring
    def choose(self) -> None:
        if self.on_chosen is None:
            return None
        return self.on_chosen(not bool(self.value))
