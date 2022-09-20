"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable, Union, Iterator

from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.dialogs.common_input_text_dialog import CommonInputTextDialog
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.dialogs.option_dialogs.options.objects.common_dialog_object_option import \
    CommonDialogObjectOption, DialogOptionIdentifierType
from sims4communitylib.dialogs.option_dialogs.options.common_dialog_option_context import CommonDialogOptionContext
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils


class CommonDialogInputTextOption(CommonDialogObjectOption):
    """CommonDialogInputTextOption(\
        mod_identity,\
        option_identifier,\
        initial_value,\
        context,\
        on_chosen=CommonFunctionUtils.noop,\
        always_visible=False,\
        dialog_description_identifier=None,\
        dialog_description_tokens=()\
    )

    An option to open a dialog to input a text value.

    :param mod_identity: The identity of the mod creating the dialog. See :class:`.CommonModIdentity` for more information.
    :type mod_identity: CommonModIdentity
    :param option_identifier: A string that identifies the option from other options.
    :type option_identifier: DialogOptionIdentifierType
    :param initial_value: The value the option will have initially
    :type initial_value: str
    :param context: A context to customize the dialog option.
    :type context: CommonDialogOptionContext
    :param on_chosen: A callback invoked when the dialog option is chosen. args: (option_identifier, entered value, outcome)
    :type on_chosen: Callable[[DialogOptionIdentifierType, int, CommonChoiceOutcome], None], optional
    :param always_visible: If set to True, the option will always appear in the dialog no matter which page.\
    If False, the option will act as normal. Default is False.
    :type always_visible: bool, optional
    :param dialog_description_identifier: The description that will display in the input dialog separately from the option.\
    If not provided the description from the provided context will be used instead.
    :type dialog_description_identifier: Union[int, str, LocalizedString, CommonStringId], optional
    :param dialog_description_tokens: An iterator of Tokens that will be formatted into the dialog description.
    :type dialog_description_tokens: Iterator[Any], optional
    """
    def __init__(
        self,
        mod_identity: CommonModIdentity,
        option_identifier: DialogOptionIdentifierType,
        initial_value: str,
        context: CommonDialogOptionContext,
        on_chosen: Callable[[DialogOptionIdentifierType, str, CommonChoiceOutcome], None]=CommonFunctionUtils.noop,
        always_visible: bool=False,
        dialog_description_identifier: Union[int, str, LocalizedString, CommonStringId]=None,
        dialog_description_tokens: Iterator[Any]=()
    ):
        if dialog_description_identifier is not None:
            dialog_description = CommonLocalizationUtils.create_localized_string(dialog_description_identifier, tokens=tuple(dialog_description_tokens))
        else:
            dialog_description = context.description
        self._dialog = CommonInputTextDialog(
            mod_identity,
            context.title,
            dialog_description,
            initial_value
        )

        def _on_submit(_: str, __: CommonChoiceOutcome):
            on_chosen(self.option_identifier, _, __)

        def _on_chosen(_, __) -> None:
            self._dialog.show(on_submit=_on_submit)

        super().__init__(
            option_identifier,
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
        return CommonIconUtils.load_arrow_right_icon()
