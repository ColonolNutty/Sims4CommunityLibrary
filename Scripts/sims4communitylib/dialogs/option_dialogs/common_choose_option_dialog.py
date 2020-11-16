"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable, Union
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_choose_dialog import CommonChooseDialog
from sims4communitylib.dialogs.option_dialogs.common_option_dialog import CommonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option import CommonDialogOption
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from ui.ui_dialog import UiDialogBase


class CommonChooseOptionDialog(CommonOptionDialog):
    """CommonChooseOptionDialog(\
        internal_dialog,\
        on_close=CommonFunctionUtils.noop\
    )

    A dialog that displays a list of options.

    .. warning:: Unless you know what you are doing, do not create an instance of this class directly!

    :param internal_dialog: The dialog this option dialog wraps.
    :type internal_dialog: CommonChooseDialog
    :param on_close: A callback invoked upon the dialog closing.
    :type on_close: Callable[[], None], optional
    """
    def __init__(
        self,
        internal_dialog: CommonChooseDialog,
        on_close: Callable[[], None]=CommonFunctionUtils.noop
    ):
        super().__init__(
            internal_dialog,
            on_close=on_close
        )
        self._options = []

    @property
    def option_count(self) -> int:
        """The number of options within the dialog.

        :return: The number of options within the dialog.
        :rtype: int
        """
        return len(self._options)

    @property
    def _internal_dialog(self) -> CommonChooseDialog:
        result: CommonChooseDialog = super()._internal_dialog
        return result

    def has_options(self) -> bool:
        """has_options()

        Determine if the dialog has selectable options.

        :return: True, if the dialog has any options in it. False, if not.
        :rtype: bool
        """
        try:
            return self.option_count > 0
        except Exception as ex:
            self.log.error('has_options', exception=ex)
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
            self.log.error('add_option', exception=ex)

    def _add_row(self, option: CommonDialogOption):
        self._internal_dialog.add_row(option.as_row(len(self._options)))

    def show(self, *_: Any, **__: Any):
        """show(*_, **__)

        Show the dialog.

        .. note:: Override this function to provide your own arguments.

        """
        try:
            return self._internal_dialog.show(*_, on_chosen=self._on_chosen(), **__)
        except Exception as ex:
            self.log.error('choose_option.show', exception=ex)

    def build_dialog(self, *_: Any, **__: Any) -> Union[UiDialogBase, None]:
        """build_dialog(*_, **__)

        Build the dialog.

        .. note:: Override this function to provide your own arguments.

        :return: The built dialog or None if a problem occurs.
        :rtype: Union[UiDialogBase, None]
        """
        try:
            return self._internal_dialog.build_dialog(*_, on_chosen=self._on_chosen(), **__)
        except Exception as ex:
            self.log.error('choose_option.build_dialog', exception=ex)
        return None

    def _on_chosen(self) -> Callable[[CommonDialogOption, CommonChoiceOutcome], bool]:
        def _on_chosen(chosen_option: CommonDialogOption, outcome: CommonChoiceOutcome) -> bool:
            try:
                if chosen_option is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                    self.close()
                    return False
                return chosen_option.choose()
            except Exception as ex:
                self.log.error('Error occurred on choosing a value.', exception=ex)
            return False
        return _on_chosen
