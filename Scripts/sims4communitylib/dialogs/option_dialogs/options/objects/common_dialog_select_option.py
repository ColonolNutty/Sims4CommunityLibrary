"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable

from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import DialogOptionValueType, \
    CommonDialogOptionContext
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_object_option import \
    CommonDialogObjectOption, DialogOptionIdentifierType


class CommonDialogSelectOption(CommonDialogObjectOption):
    """CommonDialogSelectOption(option_identifier, value, context, on_chosen=CommonFunctionUtils.noop, always_visible=False)

    An option that invokes a callback, passing in its value.

    :param option_identifier: A string that identifies the option from other options.
    :type option_identifier: DialogOptionIdentifierType
    :param value: The value of the option.
    :type value: DialogOptionValueType
    :param context: A context to customize the dialog option.
    :type context: CommonDialogOptionContext
    :param on_chosen: A callback invoked when the dialog option is chosen.
    :type on_chosen: Callable[[DialogOptionIdentifierType, DialogOptionValueType], None], optional
    :param always_visible: If set to True, the option will always appear in the dialog no matter which page.\
    If False, the option will act as normal. Default is False.
    :type always_visible: bool, optional
    """
    def __init__(
        self,
        option_identifier: DialogOptionIdentifierType,
        value: DialogOptionValueType,
        context: CommonDialogOptionContext,
        on_chosen: Callable[[DialogOptionIdentifierType, DialogOptionValueType], None]=CommonFunctionUtils.noop,
        always_visible: bool=False
    ):
        super().__init__(option_identifier, value, context, on_chosen=on_chosen, always_visible=always_visible)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def icon(self) -> Any:
        if super().icon is not None:
            return super().icon
        return CommonIconUtils.load_arrow_right_icon()
