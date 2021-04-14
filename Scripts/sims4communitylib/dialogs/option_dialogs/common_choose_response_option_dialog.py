"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable, Union
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_choose_response_dialog import CommonChooseResponseDialog
from sims4communitylib.dialogs.common_ui_response_dialog import CommonUiResponseDialog
from sims4communitylib.dialogs.option_dialogs.common_option_dialog import CommonOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.response.common_dialog_response_option import \
    CommonDialogResponseOption
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils


class CommonChooseResponseOptionDialog(CommonOptionDialog):
    """CommonChooseResponseOptionDialog(\
        internal_dialog,\
        include_previous_button=True,\
        on_previous=CommonFunctionUtils.noop\
        on_close=CommonFunctionUtils.noop\
    )

    A dialog that displays a list of options.

    .. warning:: Unless you know what you are doing, do not create an instance of this class directly!

    :param internal_dialog: The dialog this option dialog wraps.
    :type internal_dialog: CommonChooseResponseDialog
    :param include_previous_button: If True, the Previous button will be appended to the end of the dialog. Default is True.
    :type include_previous_button: bool, optional
    :param on_previous: A callback invoked upon the Previous response being chosen. Default is no operation.
    :type on_previous: Callable[[], None], optional
    :param on_close: A callback invoked upon the dialog closing.
    :type on_close: Callable[[], None], optional
    """
    def __init__(
        self,
        internal_dialog: CommonChooseResponseDialog,
        include_previous_button: bool=True,
        on_previous: Callable[[], None]=CommonFunctionUtils.noop,
        on_close: Callable[[], None]=CommonFunctionUtils.noop
    ):
        super().__init__(
            internal_dialog,
            on_close=on_close
        )
        self._include_previous_button = include_previous_button
        self._on_previous = on_previous
        self._options = []

    @property
    def option_count(self) -> int:
        """The number of options within the dialog.

        :return: The number of options within the dialog.
        :rtype: int
        """
        return len(self._options)

    @property
    def _internal_dialog(self) -> CommonChooseResponseDialog:
        result: CommonChooseResponseDialog = super()._internal_dialog
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

    def add_option(self, option: CommonDialogResponseOption):
        """add_option(option)

        Add an option to the dialog.

        :param option: The option to add.
        :type option: CommonDialogResponseOption
        """
        try:
            if self._internal_dialog is None or not hasattr(self._internal_dialog, 'add_response'):
                return
            self._options.append(option)
            self._add_response(option)
        except Exception as ex:
            self.log.error('add_option', exception=ex)

    def _add_response(self, option: CommonDialogResponseOption):
        self._internal_dialog.add_response(option.as_response(len(self._options)))

    def show(self, *_: Any, **__: Any):
        """show(*_, **__)

        Show the dialog.

        .. note:: Override this function to provide your own arguments.

        """
        try:
            return self._internal_dialog.show(*_, on_chosen=self._on_chosen(), include_previous_button=self._include_previous_button, on_previous=self._on_previous, **__)
        except Exception as ex:
            self.log.error('choose_response_option.show', exception=ex)

    def build_dialog(self, *_: Any, **__: Any) -> Union[CommonUiResponseDialog, None]:
        """build_dialog(*_, **__)

        Build the dialog.

        .. note:: Override this function to provide your own arguments.

        :return: The built dialog or None if a problem occurs.
        :rtype: Union[CommonUiResponseDialog, None]
        """
        try:
            return self._internal_dialog.build_dialog(*_, on_chosen=self._on_chosen(), include_previous_button=self._include_previous_button, on_previous=self._on_previous, **__)
        except Exception as ex:
            self.log.error('choose_response_option.build_dialog', exception=ex)
        return None

    def _on_chosen(self) -> Callable[[CommonDialogResponseOption, CommonChoiceOutcome], None]:
        def _on_chosen(chosen_option: CommonDialogResponseOption, outcome: CommonChoiceOutcome) -> None:
            try:
                if chosen_option is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                    self.close()
                    return
                chosen_option.choose()
                return
            except Exception as ex:
                self.log.error('Error occurred on choosing a value.', exception=ex)
        return _on_chosen
