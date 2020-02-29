"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

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
    """CommonChooseOptionDialog(\
        internal_dialog,\
        on_close=CommonFunctionUtils.noop\
    )

    A dialog that displays a list of options.

    .. warning:: Unless you know what you are doing, do not create an instance of this class directly!

    :param internal_dialog: The dialog this option dialog wraps.
    :type internal_dialog: CommonChooseDialog
    :param on_close: A callback invoked upon the dialog closing.
    :type on_close: Callable[..., Any], optional
    """
    def __init__(
        self,
        internal_dialog: CommonChooseDialog,
        on_close: Callable[..., Any]=CommonFunctionUtils.noop
    ):
        super().__init__()
        self._on_close = on_close
        self._options = []
        self.__internal_dialog = internal_dialog

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return self._internal_dialog.mod_identity

    @property
    def option_count(self) -> int:
        """The number of options within the dialog.

        :return: The number of options within the dialog.
        :rtype: int
        """
        return len(self._options)

    @property
    def title(self) -> LocalizedString:
        """The title of the dialog.

        :return: The title of the dialog.
        :rtype: LocalizedString
        """
        return self._internal_dialog.title

    @property
    def description(self) -> LocalizedString:
        """The description of the dialog.

        :return: The description of the dialog.
        :rtype: LocalizedString
        """
        return self._internal_dialog.description

    @property
    def _internal_dialog(self) -> CommonChooseDialog:
        return self.__internal_dialog

    def has_options(self) -> bool:
        """has_options()

        Determine if the dialog has selectable options.

        :return: True, if the dialog has any options in it. False, if not.
        :rtype: bool
        """
        try:
            return self.option_count > 0
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity.name, 'has_options', exception=ex)
        return False

    def add_option(self, option: CommonDialogOption):
        """add_option(option)

        Add an option to the dialog.

        :param option: The option to add.
        :type option: CommonDialogOption
        """
        try:
            if self._internal_dialog is None or not hasattr(self._internal_dialog, 'add_row'):
                return
            self._options.append(option)
            self._add_row(option)
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity.name, 'add_option', exception=ex)

    def _add_row(self, option: CommonDialogOption):
        self._internal_dialog.add_row(option.as_row(len(self._options)))

    def show(self, *_: Any, **__: Any):
        """show(*_, **__)

        Show the dialog.

        .. note:: Override this function to provide your own arguments.

        """
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
        """close()

        Close the dialog.

        :return: True, if the dialog closed successfully. False, if not.
        :rtype: bool
        """
        return self._on_close()
