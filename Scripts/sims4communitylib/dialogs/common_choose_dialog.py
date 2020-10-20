"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from abc import ABC
from typing import Tuple, Any, Union, Iterator
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.dialogs.common_dialog import CommonDialog
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from ui.ui_dialog_picker import BasePickerRow


class CommonChooseDialog(CommonDialog, ABC):
    """CommonChooseDialog(\
        title_identifier,\
        description_identifier,\
        rows,\
        title_tokens=(),\
        description_tokens=(),\
        mod_identity=None,\
        required_tooltip=None,\
        required_tooltip_tokens=()\
    )

    A dialog that prompts the player to choose something.

    :param title_identifier: The title to display in the dialog.
    :type title_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param description_identifier: The description to display in the dialog.
    :type description_identifier: Union[int, str, LocalizedString, CommonStringId]
    :param rows: The rows to display in the dialog.
    :type rows: Iterator[BasePickerRow]
    :param title_tokens: Tokens to format into the title. Default is an empty collection.
    :type title_tokens: Iterator[Any], optional
    :param description_tokens: Tokens to format into the description. Default is an empty collection.
    :type description_tokens: Iterator[Any], optional
    :param mod_identity: The identity of the mod creating the dialog. See :class:`.CommonModIdentity` for more information. Default is None.
    :type mod_identity: CommonModIdentity, optional
    :param required_tooltip: If provided, this text will display when the dialog requires at least one choice and a choice has not been made. Default is None.
    :type required_tooltip: Union[int, str, LocalizedString, CommonStringId], optional
    :param required_tooltip_tokens: Tokens to format into the required tooltip. Default is an empty collection.
    :type required_tooltip_tokens: Iterator[Any], optional
    """
    def __init__(
        self,
        title_identifier: Union[int, str, LocalizedString, CommonStringId],
        description_identifier: Union[int, str, LocalizedString, CommonStringId],
        rows: Iterator[BasePickerRow],
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=(),
        mod_identity: CommonModIdentity=None,
        required_tooltip: Union[int, str, LocalizedString, CommonStringId]=None,
        required_tooltip_tokens: Iterator[Any]=()
    ):
        super().__init__(
            title_identifier,
            description_identifier,
            title_tokens=title_tokens,
            description_tokens=description_tokens,
            mod_identity=mod_identity
        )
        self._rows = tuple(rows)
        if required_tooltip is None:
            self._required_tooltip = None
        else:
            self._required_tooltip = CommonLocalizationUtils.create_localized_string(required_tooltip, tokens=tuple(required_tooltip_tokens))

    @property
    def required_tooltip(self) -> Union[LocalizedString, None]:
        """A tooltip that will display when the dialog requires at least one choice and a choice has not been made.

        :return: A localized string or None if no value provided.
        :rtype: Union[LocalizedString, None]
        """
        return self._required_tooltip

    @property
    def rows(self) -> Tuple[BasePickerRow]:
        """The rows to display in the dialog.

        :return: A collection of rows added to the dialog.
        :rtype: Tuple[BasePickerRow]
        """
        return self._rows

    def add_row(self, row: BasePickerRow, *_, **__):
        """add_row(row, *_, **__)

        Add a row to the dialog.

        :param row: The row to add.
        :type row: BasePickerRow
        """
        try:
            self._rows += (row,)
        except Exception as ex:
            self.log.error('add_row', exception=ex)
