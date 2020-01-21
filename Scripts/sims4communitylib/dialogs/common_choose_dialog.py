"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

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
    """Create a dialog to prompt the player to choose something.

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
        """Create a dialog to prompt the player to choose something.

        :param title_identifier: A decimal identifier of the title text.
        :param description_identifier: A decimal identifier of the description text.
        :param rows: The rows to display in the dialog.
        :param title_tokens: Tokens to format into the title.
        :param description_tokens: Tokens to format into the description.
        """
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

        """
        return self._rows

    def add_row(self, row: BasePickerRow):
        """Add a row to the dialog.

        """
        try:
            self._rows += (row,)
        except Exception as ex:
            CommonExceptionHandler.log_exception(self.mod_identity.name, 'add_row', exception=ex)
