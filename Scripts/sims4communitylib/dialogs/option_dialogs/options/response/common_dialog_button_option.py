"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable, TypeVar

from sims4communitylib.dialogs.common_ui_dialog_response import CommonUiDialogResponse
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option import \
    CommonDialogResponseOption
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    DialogResponseOptionValueType, CommonDialogResponseOptionContext
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils

DialogResponseOptionIdentifierType = TypeVar('DialogResponseOptionIdentifierType')


class CommonDialogButtonOption(CommonDialogResponseOption):
    """CommonDialogButtonOption(option_identifier, value, context, on_chosen=CommonFunctionUtils.noop)

    An option the player can choose within a dialog.

    :param option_identifier: A string that identifies the option from other options.
    :type option_identifier: DialogOptionIdentifierType
    :param value: The value of the option.
    :type value: DialogResponseOptionValueType
    :param context: A context to customize the dialog option.
    :type context: CommonDialogOptionContext
    :param on_chosen: A callback invoked when the dialog option is chosen. The values are as follows: (option_identifier, value)
    :type on_chosen: Callable[[DialogOptionIdentifierType, DialogResponseOptionValueType], None], optional
    """
    def __init__(
        self,
        option_identifier: DialogResponseOptionIdentifierType,
        value: DialogResponseOptionValueType,
        context: CommonDialogResponseOptionContext,
        on_chosen: Callable[[DialogResponseOptionIdentifierType, DialogResponseOptionValueType], None]=CommonFunctionUtils.noop
    ):
        if option_identifier is None:
            raise AttributeError('Missing required argument \'option_identifier\'')

        self._option_identifier = option_identifier

        def _on_chosen(val: DialogResponseOptionValueType) -> Any:
            return on_chosen(self.option_identifier, val)

        super().__init__(value, context, on_chosen=_on_chosen)

    @property
    def option_identifier(self) -> DialogResponseOptionIdentifierType:
        """Used to identify the option."""
        return self._option_identifier

    @property
    def value(self) -> DialogResponseOptionValueType:
        """The value of the option."""
        return self._value

    def as_response(self, option_id: int) -> CommonUiDialogResponse:
        """as_response(option_id)

        Convert the option into a response.

        :param option_id: The index of the option.
        :type option_id: int
        :return: The option as a Response
        :rtype: CommonUiDialogResponse
        """
        return CommonUiDialogResponse(
            option_id,
            self,
            text=self.context.text,
            subtext=self.context.subtext,
            disabled_text=self.context.disabled_text
        )
