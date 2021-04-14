"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable, Union

from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.dialogs.common_ui_dialog_response import CommonUiDialogResponse
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option_context import \
    DialogResponseOptionValueType, CommonDialogResponseOptionContext
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils


class CommonDialogResponseOption:
    """CommonDialogResponseOption(value, context, on_chosen=CommonFunctionUtils.noop)

    An option the player can choose within a dialog.

    :param value: The value of the option.
    :type value: DialogOptionValueType
    :param context: A context to customize the dialog option.
    :type context: CommonDialogResponseOptionContext
    :param on_chosen: A callback invoked when the dialog option is chosen.
    :type on_chosen: Callable[[DialogOptionValueType], Any], optional
    """
    def __init__(
        self,
        value: DialogResponseOptionValueType,
        context: CommonDialogResponseOptionContext,
        on_chosen: Callable[[DialogResponseOptionValueType], Any]=CommonFunctionUtils.noop
    ):
        if context is None:
            raise AttributeError('Missing required argument \'context\'')

        self._value = value
        self._option_context = context
        self._on_chosen = on_chosen

    @property
    def text(self) -> LocalizedString:
        """The text of the dialog option."""
        return self.context.text

    @property
    def subtext(self) -> Union[LocalizedString, None]:
        """The subtext that displays under the option."""
        return self.context.subtext

    @property
    def disabled_text(self) -> Union[LocalizedString, None]:
        """The text that displays on the option as a tooltip. If provided, the option will also be disabled."""
        return self.context.disabled_text

    @property
    def context(self) -> CommonDialogResponseOptionContext:
        """The context of the option."""
        return self._option_context

    @property
    def value(self) -> DialogResponseOptionValueType:
        """The value of the option."""
        return self._value

    @property
    def on_chosen(self) -> Callable[[DialogResponseOptionValueType], Any]:
        """The action to perform upon choosing this option."""
        return self._on_chosen

    def choose(self) -> Any:
        """choose()

        Choose the option.

        :return: The result of choosing the option.
        :rtype: Any
        """
        if self.on_chosen is None:
            return None
        return self.on_chosen(self.value)

    def as_response(self, option_id: int) -> CommonUiDialogResponse:
        """as_response(option_id)

        Convert the option into a response.

        :param option_id: The index of the option.
        :type option_id: int
        :return: The option as a Response
        :rtype: CommonUiDialogResponse
        """
        raise NotImplementedError('\'{}\' not implemented.'.format(self.__class__.as_response.__name__))
