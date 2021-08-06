"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable, TypeVar
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from ui.ui_dialog_picker import ObjectPickerRow
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option import CommonDialogOption
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext, \
    DialogOptionValueType

DialogOptionIdentifierType = TypeVar('DialogOptionIdentifierType')


class CommonDialogObjectOption(CommonDialogOption):
    """CommonDialogObjectOption(option_identifier, value, context, on_chosen=CommonFunctionUtils.noop)

    An option the player can choose within a dialog.

    :param option_identifier: A string that identifies the option from other options.
    :type option_identifier: DialogOptionIdentifierType
    :param value: The value of the option.
    :type value: DialogOptionValueType
    :param context: A context to customize the dialog option.
    :type context: CommonDialogOptionContext
    :param on_chosen: A callback invoked when the dialog option is chosen. The values are as follows: (option_identifier, value)
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
        if option_identifier is None:
            raise AttributeError('Missing required argument \'option_identifier\'')

        self._option_identifier = option_identifier
        self._always_visible = always_visible

        def _on_chosen(val: DialogOptionValueType) -> Any:
            return on_chosen(self.option_identifier, val)

        super().__init__(value, context, on_chosen=_on_chosen)

    @property
    def option_identifier(self) -> DialogOptionIdentifierType:
        """Used to identify the option.

        :return: The identity of the option.
        :rtype: str
        """
        return self._option_identifier

    @property
    def value(self) -> DialogOptionValueType:
        """The value of the option.

        :return: The value of the option.
        :rtype: DialogOptionValueType
        """
        return self._value

    @property
    def always_visible(self) -> bool:
        """Determine if the option will always be visible.

        :return: If set to True, the option will always appear in the dialog no matter which page.\
        If False, the option will act as normal.
        :rtype: bool
        """
        return self._always_visible

    def as_row(self, option_id: int) -> ObjectPickerRow:
        """as_row(option_id)

        Convert the option into a picker row.

        :param option_id: The index of the option.
        :type option_id: int
        :return: The option as a Picker Row
        :rtype: ObjectPickerRow
        """
        return ObjectPickerRow(
            option_id=option_id,
            name=self.title,
            row_description=self.description,
            row_tooltip=self.tooltip,
            icon=self.icon,
            is_enable=self.context.is_enabled,
            is_selected=self.context.is_selected,
            tag_list=self.hashed_tag_list,
            tag=self
        )
