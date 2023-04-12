"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Any, Callable, Iterator
from protocolbuffers.Localization_pb2 import LocalizedString
from sims.sim_info import SimInfo
from sims4communitylib.dialogs.common_input_text_field import CommonInputTextField
from sims4communitylib.enums.common_character_restrictions import CommonCharacterRestriction
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from ui.ui_dialog_generic import UiDialogTextInputOkCancel


class _CommonUiDialogMultiTextInputOkCancel(UiDialogTextInputOkCancel):
    def __init__(
        self,
        sim_info: SimInfo,
        input_fields: Iterator[CommonInputTextField],
        *args,
        title: Callable[..., LocalizedString] = None,
        text: Callable[..., LocalizedString] = None,
        **kwargs
    ):
        super().__init__(
            sim_info,
            *args,
            title=title,
            text=text,
            **kwargs
        )
        self.input_fields = input_fields
        self.text_input_responses = {}

    def on_text_input(self, text_input_name: str = '', text_input: str = '') -> bool:
        """A callback that occurs upon text being entered.

        """
        self.text_input_responses[text_input_name] = text_input
        return False

    def build_msg(self, text_input_overrides=None, additional_tokens: Tuple[Any] = (), **kwargs):
        """Build the message.

        """
        msg = super().build_msg(additional_tokens=(), **kwargs)
        for input_field in self.input_fields:
            if input_field.initial_value is not None:
                self.text_input_responses[input_field.identifier] = str(input_field.initial_value)
            text_input_msg = msg.text_input.add()
            text_input_msg.text_input_name = input_field.identifier
            if input_field.default_text is not None:
                text_input_msg.default_text = CommonLocalizationUtils.create_localized_string(input_field.default_text)
            if input_field.initial_value is not None:
                text_input_msg.initial_value = CommonLocalizationUtils.create_localized_string(str(input_field.initial_value))
            if input_field.title is not None:
                text_input_msg.title = CommonLocalizationUtils.create_localized_string(input_field.title)
            if input_field.character_restriction is not None and input_field.character_restriction != CommonCharacterRestriction.NONE:
                character_restriction_mapping = {
                    CommonCharacterRestriction.NUMBERS_ONLY: CommonStringId.ZERO_THROUGH_NINE,
                }
                text_input_msg.restricted_characters = CommonLocalizationUtils.create_localized_string(character_restriction_mapping.get(input_field.character_restriction))
        return msg
