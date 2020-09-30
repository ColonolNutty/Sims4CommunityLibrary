"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Any, Callable
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from ui.ui_dialog_generic import UiDialogTextInputOkCancel


class _CommonUiDialogTextInputOkCancel(UiDialogTextInputOkCancel):
    def __init__(
        self,
        sim_info: SimInfo,
        *args,
        title: Callable[..., LocalizedString]=None,
        text: Callable[..., LocalizedString]=None,
        **kwargs
    ):
        super().__init__(
            sim_info,
            *args,
            title=title,
            text=text,
            **kwargs
        )
        self.text_input_responses = {}

    def on_text_input(self, text_input_name: str='', text_input: str='') -> bool:
        """A callback that occurs upon text being entered.

        """
        self.text_input_responses[text_input_name] = text_input
        return False

    def build_msg(self, text_input_overrides=None, additional_tokens: Tuple[Any]=(), **kwargs):
        """Build the message.

        """
        from sims4communitylib.dialogs.utils.common_dialog_utils import CommonDialogUtils
        msg = super().build_msg(additional_tokens=(), **kwargs)
        text_input_msg = msg.text_input.add()
        text_input_msg.text_input_name = CommonDialogUtils.TEXT_INPUT_NAME
        if additional_tokens and additional_tokens[0] is not None:
            text_input_msg.initial_value = CommonLocalizationUtils.create_localized_string(str(additional_tokens[0]))
        return msg
