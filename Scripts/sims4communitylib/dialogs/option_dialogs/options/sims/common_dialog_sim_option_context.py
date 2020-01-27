"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext


class CommonDialogSimOptionContext(CommonDialogOptionContext):
    """CommonDialogSimOptionContext(is_enabled=True, is_selected=False)

    A context used by CommonDialogSimOption that contains customization of the option.

    :param is_enabled: If True, the Sim will be selectable in the dialog. If False, the Sim will be disabled in the dialog.
    :type is_enabled: bool, optional
    :param is_selected: If True, the Sim will already be selected in the dialog. If False, the Sim will not be selected in the dialog.
    :type is_selected: bool, optional
    """
    def __init__(
        self,
        is_enabled: bool=True,
        is_selected: bool=False
    ):
        super().__init__(
            0,
            0,
            is_enabled=is_enabled,
            is_selected=is_selected
        )
