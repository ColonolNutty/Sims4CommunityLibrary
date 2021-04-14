"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Union
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from ui.ui_dialog import UiDialogResponse


class CommonUiDialogResponse(UiDialogResponse):
    """ A dialog response. """
    def __init__(
        self,
        dialog_response_id: int,
        value: Any,
        sort_order: int=0,
        text: Union[int, str, LocalizedString, CommonStringId]=None,
        subtext: Union[int, str, LocalizedString, CommonStringId]=None,
        ui_request: UiDialogResponse.UiDialogUiRequest=UiDialogResponse.UiDialogUiRequest.NO_REQUEST,
        response_command: Any=None,
        disabled_text: Union[int, str, LocalizedString, CommonStringId]=None
    ):
        super().__init__(
            sort_order=sort_order,
            dialog_response_id=dialog_response_id,
            text=lambda *_, **__: CommonLocalizationUtils.create_localized_string(text) if text is not None else None,
            subtext=CommonLocalizationUtils.create_localized_string(subtext) if subtext is not None else None,
            ui_request=ui_request,
            response_command=response_command,
            disabled_text=CommonLocalizationUtils.create_localized_string(disabled_text) if disabled_text is not None else None
        )
        self.response_id = int(dialog_response_id)
        self.value = value
