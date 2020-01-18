"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable

from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_choose_dialog import CommonChooseDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option import CommonDialogOption
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils


class CommonChooseOptionDialog(HasLog):
    """ A dialog that displays a list of options. """
    def __init__(
        self,
        internal_dialog: CommonChooseDialog,
        on_close: Callable[..., Any]=CommonFunctionUtils.noop
    ):
        """
            Create a dialog to display a list of options.
        :param on_close: A callback invoked upon the dialog closing.
        """
        super().__init__()
        self._on_close = on_close
        self._options = []
        self.__internal_dialog = internal_dialog

    @property
    def mod_identity(self) -> CommonModIdentity:
        """ The Identity of the mod that owns this class. """
        return self._internal_dialog.mod_identity

    @property
    def option_count(self) -> int:
        """ Determine the number of options within this dialog. """
        return len(self._options)

    @property
    def title(self) -> LocalizedString:
        """ The title of the dialog. """
        return self._internal_dialog.title

    @property
    def description(self) -> LocalizedString:
        """ The description of the dialog. """
        return self._internal_dialog.description

    @property
    def _internal_dialog(self) -> CommonChooseDialog:
        return self.__internal_dialog

    def has_options(self) -> bool:
        """ Determine if the dialog has selectable options. """
        try:
            return self.option_count > 0
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity.name, 'has_options', exception=ex)
        return False

    def add_option(self, option: CommonDialogOption):
        """ Add an option to the dialog. """
        try:
            if self._internal_dialog is None or not hasattr(self._internal_dialog, 'add_row'):
                return
            self._options.append(option)
            self._internal_dialog.add_row(option.as_row(len(self._options)))
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity.name, 'add_option', exception=ex)

    def show(self, *_, **__):
        """ Show the dialog. """
        try:
            def _on_chosen(chosen_option: CommonDialogOption, outcome: CommonChoiceOutcome) -> bool:
                if chosen_option is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                    self.close()
                    return False
                return chosen_option.choose()
            self._internal_dialog.show(*_, on_chosen=_on_chosen, **__)
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity.name, 'show', exception=ex)

    def close(self) -> bool:
        """ Close the dialog. """
        return self._on_close()
