"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

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
    """CommonDialog(\
        title_identifier,\
        description_identifier,\
        title_tokens=(),\
        description_tokens=(),\
        mod_identity=None\
    )

    An inheritable class for creating a dialog.

    .. note:: It is recommended to utilize one of the ready made dialogs, instead of creating a custom :class:`CommonDialog`

    :param title_identifier: The title to display in the dialog.
    :type title_identifier: Union[int, LocalizedString]
    :param description_identifier: The description to display in the dialog.
    :type description_identifier: Union[int, LocalizedString]
    :param title_tokens: Tokens to format into the title. Default is an empty collection.
    :type title_tokens: Iterator[Any], optional
    :param description_tokens: Tokens to format into the description. Default is an empty collection.
    :type description_tokens: Iterator[Any], optional
    :param disabled_tooltip: If provided, this text will display when the dialog is disabled. Default is None.
    :type disabled_tooltip: Union[int, LocalizedString], optional
    :param disabled_tooltip_tokens: Tokens to format into the disabled tooltip. Default is an empty collection.
    :type disabled_tooltip_tokens: Iterator[Any], optional
    :param mod_identity: The identity of the mod creating the dialog. See :class:`.CommonModIdentity` for more information. Default is None.
    :type mod_identity: CommonModIdentity, optional
    """

    def __init__(
        self,
        title_identifier: Union[int, LocalizedString],
        description_identifier: Union[int, LocalizedString],
        title_tokens: Iterator[Any]=(),
        description_tokens: Iterator[Any]=(),
        disabled_tooltip: Union[int, LocalizedString]=None,
        disabled_tooltip_tokens: Iterator[Any]=(),
        mod_identity: CommonModIdentity=None
    ):
        super().__init__()
        self.title = CommonLocalizationUtils.create_localized_string(title_identifier, tokens=tuple(title_tokens))
        self.description = CommonLocalizationUtils.create_localized_string(description_identifier, tokens=tuple(description_tokens))
        self._mod_identity = mod_identity
        if disabled_tooltip is None:
            self._disabled_tooltip = None
        else:
            self._disabled_tooltip = CommonLocalizationUtils.create_localized_string(disabled_tooltip, tokens=tuple(disabled_tooltip_tokens))

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return self._mod_identity or ModInfo.get_identity()

    @property
    def disabled_tooltip(self) -> Union[LocalizedString, None]:
        """A tooltip that will display when the dialog is disabled.

        :return: An instance of CommonModIdentity
        :rtype: CommonModIdentity
        """
        return self._disabled_tooltip

    def show(self, *_: Any, **__: Any):
        """show(*_, **__)

        Display the dialog to the player.

        .. note:: Override this method with any arguments you want to.

        """
        raise NotImplementedError('\'{}\' not implemented.'.format(self.__class__.show.__name__))

    def build_dialog(self, *_: Any, **__: Any) -> Union[UiDialogBase, None]:
        """build_dialog(*_, **__)

        Build the dialog.

        .. note:: Override this method with any arguments you want to.

        :return: The built dialog or None if a problem occurs.
        :rtype: Union[UiDialogBase, None]
        """
        return self._create_dialog(*_, **__)

    def _create_dialog(self, *_: Any, **__: Any) -> Union[UiDialogBase, None]:
        """_create_dialog(*_, **__)

        Create a dialog for use in :func:``show`.

        .. note:: Override this method with any arguments you want to.

        :return: An instance of the dialog being shown or None if a problem occurs.
        :rtype: Union[UiDialogBase, None]
        """
        raise NotImplementedError('\'{}\' not implemented.'.format(self.__class__._create_dialog.__name__))
