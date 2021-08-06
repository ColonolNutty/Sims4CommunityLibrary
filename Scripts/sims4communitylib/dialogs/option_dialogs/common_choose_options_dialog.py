"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Tuple, Any, Callable, List

from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_choose_dialog import CommonChooseDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_option_dialog import CommonChooseOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option import CommonDialogOption
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import DialogOptionValueType
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils


# noinspection PyMissingOrEmptyDocstring
from ui.ui_dialog import UiDialogBase


class CommonChooseOptionsDialog(CommonChooseOptionDialog):
    """CommonChooseOptionsDialog(\
        internal_dialog,\
        on_close=CommonFunctionUtils.noop\
    )

    A dialog that displays a list of options and prompts to select multiple items.

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

    def show(
        self,
        *_,
        on_submit: Callable[[Tuple[DialogOptionValueType]], Any]=CommonFunctionUtils.noop,
        min_selectable: int=1,
        max_selectable: int=1,
        allow_no_selection: bool=False,
        **__
    ):
        """show(\
            *_,\
            on_submit=CommonFunctionUtils.noop,\
            min_selectable=1,\
            max_selectable=1,\
            allow_no_selection=False,\
            **__\
        )

        Show the dialog.

        .. note:: Override this function to provide your own arguments.

        :param on_submit: When the dialog is submitted, this callback will be invoked with the chosen options.
        :type on_submit: Callable[[Tuple[DialogOptionValueType]], Any], optional
        :param min_selectable: The minimum number of options that can be chosen.
        :type min_selectable: int, optional
        :param max_selectable: The maximum number of options that can be chosen.
        :type max_selectable: int, optional
        :param allow_no_selection: If True, the player may select no options. If False, the dialog will close with no options selected. Default is False.
        :type allow_no_selection: bool, optional
        """
        try:
            return self._internal_dialog.show(
                *_,
                on_chosen=self._on_submit(on_submit, allow_no_selection=allow_no_selection),
                min_selectable=min_selectable,
                max_selectable=max_selectable,
                **__
            )
        except Exception as ex:
            self.log.error('choose_options.show', exception=ex)

    def build_dialog(
        self,
        *_: Any,
        on_submit: Callable[[Tuple[DialogOptionValueType]], Any]=CommonFunctionUtils.noop,
        min_selectable: int=1,
        max_selectable: int=1,
        allow_no_selection: bool=False,
        **__: Any
    ) -> Union[UiDialogBase, None]:
        """build_dialog(\
            *_,\
            on_submit=CommonFunctionUtils.noop,\
            min_selectable=1,\
            max_selectable=1,\
            allow_no_selection=False,\
            **__\
        )

        Build the dialog.

        .. note:: Override this function to provide your own arguments.

        :param on_submit: When the dialog is submitted, this callback will be invoked with the chosen options.
        :type on_submit: Callable[[Tuple[DialogOptionValueType]], Any], optional
        :param min_selectable: The minimum number of options that can be chosen.
        :type min_selectable: int, optional
        :param max_selectable: The maximum number of options that can be chosen.
        :type max_selectable: int, optional
        :param allow_no_selection: If True, the player may select no options. If False, the dialog will close with no options selected. Default is False.
        :type allow_no_selection: bool, optional
        :return: The built dialog or None if a problem occurs.
        :rtype: Union[UiDialogBase, None]
        """
        try:

            return self._internal_dialog.build_dialog(
                *_,
                on_chosen=self._on_submit(on_submit, allow_no_selection=allow_no_selection),
                min_selectable=min_selectable,
                max_selectable=max_selectable,
                **__
            )
        except Exception as ex:
            self.log.error('choose_options.build_dialog', exception=ex)
        return None

    def _on_chosen(self) -> Callable[[Union[Tuple[CommonDialogOption], None], CommonChoiceOutcome], bool]:
        return self._on_submit()

    def _on_submit(
        self,
        on_submit: Callable[[Tuple[DialogOptionValueType]], Any]=CommonFunctionUtils.noop,
        allow_no_selection: bool=False
    ) -> Callable[[Union[Tuple[CommonDialogOption], None], CommonChoiceOutcome], bool]:
        def _on_submit(chosen_options: Union[Tuple[CommonDialogOption], None], outcome: CommonChoiceOutcome) -> bool:
            try:
                if chosen_options is None or CommonChoiceOutcome.is_error_or_cancel(outcome):
                    self.close()
                    return True
                if not allow_no_selection:
                    if len(chosen_options) == 0:
                        self.close()
                        return True
                chosen_values: List[DialogOptionValueType] = list()
                for chosen_option in chosen_options:
                    chosen_values.append(chosen_option.value)
                    chosen_option.choose()
                return on_submit(tuple(chosen_values))
            except Exception as ex:
                self.log.error('Error occurred on submitting a value.', exception=ex)
            return False
        return _on_submit
