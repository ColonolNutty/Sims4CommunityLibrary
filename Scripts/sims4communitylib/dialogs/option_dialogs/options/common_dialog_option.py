"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable, Union, Tuple

from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from ui.ui_dialog_picker import BasePickerRow
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext, \
    DialogOptionValueType


class CommonDialogOption:
    """CommonDialogOption(value, context, on_chosen=CommonFunctionUtils.noop)

    An option the player can choose within a dialog.

    :param value: The value of the option.
    :type value: DialogOptionValueType
    :param context: A context to customize the dialog option.
    :type context: CommonDialogOptionContext
    :param on_chosen: A callback invoked when the dialog option is chosen.
    :type on_chosen: Callable[[DialogOptionValueType], Any], optional
    """
    def __init__(
        self,
        value: DialogOptionValueType,
        context: CommonDialogOptionContext,
        on_chosen: Callable[[DialogOptionValueType], Any]=CommonFunctionUtils.noop
    ):
        if context is None:
            raise AttributeError('Missing required argument \'context\'')

        self._value = value
        self._option_context = context
        self._on_chosen = on_chosen

    @property
    def title(self) -> LocalizedString:
        """The title of the option.

        :return: The title of the option.
        :rtype: LocalizedString
        """
        return self.context.title

    @property
    def description(self) -> LocalizedString:
        """The description of the option.

        :return: The description of the option.
        :rtype: LocalizedString
        """
        return self.context.description

    @property
    def tooltip(self) -> Union[CommonLocalizationUtils.LocalizedTooltip, None]:
        """The tooltip displayed to the player on hover.

        :return: The tooltip displayed when hovering the option or None if no tooltip specified.
        :rtype: Union[CommonLocalizationUtils.LocalizedTooltip, None]
        """
        return self.context.tooltip

    @property
    def icon(self) -> Any:
        """The icon of the option.

        :return: The icon of the option.
        :rtype: Any
        """
        return self.context.icon

    @property
    def tag_list(self) -> Tuple[str]:
        """A collection of tags used to filter the option.

        :return: A collection of tags used to filter the option.
        :rtype: Tuple[str]
        """
        return self.context.tag_list

    @property
    def hashed_tag_list(self) -> Tuple[int]:
        """Same as tag_list, but the values are hashed.

        :return: Same as tag_list, but the values are hashed.
        :rtype: Tuple[str]
        """
        return self.context.hashed_tag_list

    @property
    def context(self) -> CommonDialogOptionContext:
        """The context of the option.

        :return: The context of the option.
        :rtype: CommonDialogOptionContext
        """
        return self._option_context

    @property
    def value(self) -> DialogOptionValueType:
        """The value of the option.

        :return: The value of the option.
        :rtype: DialogOptionValueType
        """
        return self._value

    @property
    def on_chosen(self) -> Callable[[DialogOptionValueType], Any]:
        """The action to perform upon choosing this option.

        :return: The action to perform upon choosing this option.
        :rtype: Callable[[DialogOptionValueType], Any]
        """
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

    def as_row(self, option_id: int) -> BasePickerRow:
        """as_row(option_id)

        Convert the option into a picker row.

        :param option_id: The index of the option.
        :type option_id: int
        :return: The option as a Picker Row
        :rtype: BasePickerRow
        """
        raise NotImplementedError('\'{}\' not implemented.'.format(self.__class__.as_row.__name__))
