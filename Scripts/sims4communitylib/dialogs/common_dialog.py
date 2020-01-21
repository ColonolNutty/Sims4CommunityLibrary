"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Union, Iterator
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from ui.ui_dialog import UiDialogBase


class CommonDialog(HasLog):
    """Create a dialog

    """
    def __init__(
        self,
        title_identifier: Union[int, LocalizedString],
        description_identifier: Union[int, LocalizedString],
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=(),
        mod_identity: CommonModIdentity=None
    ):
        """Create a dialog

        :param title_identifier: A decimal identifier of the title text.
        :param description_identifier: A decimal identifier of the description text.
        :param title_tokens: Tokens to format into the title.
        :param description_tokens: Tokens to format into the description.
        """
        super().__init__()
        self.title = CommonLocalizationUtils.create_localized_string(title_identifier, tokens=tuple(title_tokens))
        self.description = CommonLocalizationUtils.create_localized_string(description_identifier, tokens=tuple(description_tokens))
        self._mod_identity = mod_identity

    @property
    def mod_identity(self) -> CommonModIdentity:
        """The Identity of the mod that owns this class.

        """
        return self._mod_identity or ModInfo.get_identity()

    def show(self, *_, **__):
        """Show the dialog

        """
        raise NotImplementedError('\'{}\' not implemented.'.format(self.__class__.show.__name__))

    def _create_dialog(self, *_, **__) -> Union[UiDialogBase, None]:
        raise NotImplementedError('\'{}\' not implemented.'.format(self.__class__._create_dialog.__name__))
