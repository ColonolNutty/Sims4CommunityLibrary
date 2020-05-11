"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable
from sims4communitylib.dialogs.option_dialogs.common_option_dialog import CommonOptionDialog
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_object_option import CommonDialogObjectOption
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext


class CommonDialogOpenDialogOption(CommonDialogObjectOption):
    """CommonDialogOpenDialogOption(create_dialog_callback, context, always_visible=False)

    An option that branches into other options.

    :param create_dialog_callback: A callback invoked when the dialog option is chosen. It should open a dialog.
    :type create_dialog_callback: Callable[..., CommonOptionDialog]
    :param context: A context to customize the dialog option.
    :type context: CommonDialogOptionContext
    :param always_visible: If set to True, the option will always appear in the dialog no matter which page.\
    If False, the option will act as normal. Default is False.
    :type always_visible: bool, optional
    """
    def __init__(
        self,
        create_dialog_callback: Callable[..., CommonOptionDialog],
        context: CommonDialogOptionContext,
        always_visible: bool=False
    ):
        def _on_chosen(_, __) -> None:
            create_dialog_callback().show()

        super().__init__(
            'Dialog Branch',
            None,
            context,
            on_chosen=_on_chosen,
            always_visible=always_visible
        )

    # noinspection PyMissingOrEmptyDocstring
    @property
    def icon(self) -> Any:
        if super().icon is not None:
            return super().icon
        return CommonIconUtils.load_arrow_navigate_into_icon()
