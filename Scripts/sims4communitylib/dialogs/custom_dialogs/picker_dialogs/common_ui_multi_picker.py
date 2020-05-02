"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Dict
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from protocolbuffers.Dialog_pb2 import UiDialogMessage, UiDialogMultiPicker
from ui.ui_dialog_multi_picker import UiMultiPicker


class CommonUiMultiPicker(UiMultiPicker):
    """CommonUiMultiPicker(\
        *args,\
        **kwargs\
    )

    A custom multi picker dialog that enables programmatic creation.

    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.required_tooltips: Dict[Any, LocalizedString] = dict()

    def build_msg(self, **kwargs) -> Any:
        """build_msg(**kwargs)

        Build the message for display.

        :return: Unknown.
        :rtype: Any
        """
        message = super().build_msg(**kwargs)
        # noinspection PyUnresolvedReferences
        message.dialog_type = UiDialogMessage.MULTI_PICKER
        multi_picker_msg = UiDialogMultiPicker()
        for dialog in self._picker_dialogs.values():
            new_message = dialog.build_msg()
            # noinspection PyUnresolvedReferences
            multi_picker_item = multi_picker_msg.multi_picker_items.add()
            multi_picker_item.picker_data = new_message.picker_data
            multi_picker_item.picker_id = new_message.dialog_id
            multi_picker_item.disabled_tooltip = self.required_tooltips.get(new_message.dialog_id, None) or CommonLocalizationUtils.create_localized_string('')
        message.multi_picker_data = multi_picker_msg
        return message
