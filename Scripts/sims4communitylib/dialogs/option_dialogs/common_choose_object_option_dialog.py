"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Union, Callable, Iterator

from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.choose_object_dialog import CommonChooseObjectDialog
from sims4communitylib.dialogs.option_dialogs.common_choose_option_dialog import CommonChooseOptionDialog
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_object_option import CommonDialogObjectOption
from ui.ui_dialog_picker import UiObjectPicker


class CommonChooseObjectOptionDialog(CommonChooseOptionDialog):
    """ A dialog that displays a list of options. """
    def __init__(
        self,
        title_identifier: Union[int, LocalizedString],
        description_identifier: Union[int, LocalizedString],
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=(),
        on_close: Callable[..., Any]=CommonFunctionUtils.noop,
        mod_identity: ModInfo=None,
        per_page: int=25
    ):
        """
            Create a dialog to display a list of options.
        :param title_identifier: A decimal identifier of the title text.
        :param description_identifier: A decimal identifier of the description text.
        :param title_tokens: Tokens to format into the title.
        :param description_tokens: Tokens to format into the description.
        :param on_close: A callback invoked upon the dialog closing.
        :param per_page: The number of rows to display per page. If the number of rows (including rows added after creation) exceeds this value, pagination will be added.
        """
        super().__init__(
            CommonChooseObjectDialog(
                title_identifier,
                description_identifier,
                tuple(),
                title_tokens=title_tokens,
                description_tokens=description_tokens,
                per_page=per_page,
                mod_identity=mod_identity
            ),
            on_close=on_close
        )

    @property
    def log_identifier(self) -> str:
        """ An identifier for the Log of this class. """
        return 's4cl_choose_object_option_dialog'

    def add_option(self, option: CommonDialogObjectOption):
        """ Add an option to the dialog. """
        return super().add_option(option)

    def show(
        self,
        picker_type: UiObjectPicker.UiObjectPickerObjectPickerType=UiObjectPicker.UiObjectPickerObjectPickerType.OBJECT,
        page: int=1,
        sim_info: SimInfo=None
    ):
        """
            Show the dialog and invoke the callbacks upon the player making a choice.
        :param picker_type: The layout of the dialog.
        :param page: The page to display. Ignored if there is only one page of choices.
        :param sim_info: The SimInfo of the Sim that will appear in the dialog image. The default Sim is the active Sim.
        """
        return super().show(
            picker_type=picker_type,
            page=page,
            sim_info=sim_info
        )
