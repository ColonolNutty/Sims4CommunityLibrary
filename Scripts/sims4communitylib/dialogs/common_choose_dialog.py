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
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from ui.ui_dialog_picker import BasePickerRow


class CommonChooseDialog(CommonDialog, ABC):
    """CommonChooseDialog(\
        title_identifier,\
        description_identifier,\
        rows,\
        title_tokens=(),\
        description_tokens=(),\
        mod_identity=None\
    )

    A dialog that prompts the player to choose something.

    :param title_identifier: The title to display in the dialog.
    :type title_identifier: Union[int, LocalizedString]
    :param description_identifier: The description to display in the dialog.
    :type description_identifier: Union[int, LocalizedString]
    :param rows: The rows to display in the dialog.
    :type rows: Iterator[BasePickerRow]
    :param title_tokens: Tokens to format into the title.
    :type title_tokens: Iterator[Any], optional
    :param description_tokens: Tokens to format into the description.
    :type description_tokens: Iterator[Any], optional
    :param mod_identity: The identity of the mod creating the dialog. See :class:`.CommonModIdentity` for more information.
    :type mod_identity: CommonModIdentity, optional
    """
    def __init__(
        self,
        title_identifier: Union[int, LocalizedString],
        description_identifier: Union[int, LocalizedString],
        rows: Iterator[BasePickerRow],
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=(),
        mod_identity: CommonModIdentity=None
    ):
        super().__init__(
            title_identifier,
            description_identifier,
            title_tokens=title_tokens,
            description_tokens=description_tokens,
            mod_identity=mod_identity
        )
        self._rows = tuple(rows)

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
            CommonExceptionHandler.log_exception(self.mod_identity, 'add_row', exception=ex)
