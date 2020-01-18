"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable, Union

from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from ui.ui_dialog_picker import BasePickerRow
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext, \
    DialogOptionValueType


class CommonDialogOption:
    """ A option the player can choose within a dialog.  """
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
        """ The title of the option. """
        return self.context.title

    @property
    def description(self) -> LocalizedString:
        """ The description of the option. """
        return self.context.description

    @property
    def tooltip(self) -> Union[CommonLocalizationUtils.LocalizedTooltip, None]:
        """ The tooltip displayed to the player on hover. """
        return self.context.tooltip

    @property
    def icon(self) -> Any:
        """ The icon of the option. """
        return self.context.icon

    @property
    def context(self) -> CommonDialogOptionContext:
        """ The context of the option. """
        return self._option_context

    @property
    def value(self) -> DialogOptionValueType:
        """ The value of the option. """
        return self._value

    @property
    def on_chosen(self) -> Callable[[DialogOptionValueType], Any]:
        """ The action to perform upon choosing this option. """
        return self._on_chosen

    def choose(self) -> Any:
        """ Choose this option. """
        if self.on_chosen is None:
            return None
        return self.on_chosen(self.value)

    def as_row(self, option_id: int) -> BasePickerRow:
        """ Convert the option into a picker row. """
        raise NotImplementedError('\'{}\' not implemented.'.format(self.__class__.as_row.__name__))
