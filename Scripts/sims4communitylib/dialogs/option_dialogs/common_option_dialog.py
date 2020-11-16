"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Callable, Union
from protocolbuffers.Localization_pb2 import LocalizedString
from sims4communitylib.dialogs.common_dialog import CommonDialog
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_function_utils import CommonFunctionUtils
from ui.ui_dialog import UiDialogBase


class CommonOptionDialog(HasLog):
    """CommonOptionDialog(\
        internal_dialog,\
        on_close=CommonFunctionUtils.noop\
    )

    A dialog that displays that displays options.

    .. warning:: Unless you know what you are doing, do not create an instance of this class directly!

    :param internal_dialog: The dialog this option dialog wraps.
    :type internal_dialog: CommonDialog
    :param on_close: A callback invoked upon the dialog closing. Default is CommonFunctionUtils.noop.
    :type on_close: Callable[[], None], optional
    """
    def __init__(
        self,
        internal_dialog: CommonDialog,
        on_close: Callable[[], None]=CommonFunctionUtils.noop
    ):
        super().__init__()
        self._on_close = on_close
        self.__internal_dialog = internal_dialog

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return self._internal_dialog.mod_identity

    @property
    def title(self) -> LocalizedString:
        """The title of the dialog.

        :return: The title of the dialog.
        :rtype: LocalizedString
        """
        return self._internal_dialog.title

    @property
    def description(self) -> LocalizedString:
        """The description of the dialog.

        :return: The description of the dialog.
        :rtype: LocalizedString
        """
        return self._internal_dialog.description

    @property
    def _internal_dialog(self) -> CommonDialog:
        return self.__internal_dialog

    def show(self, *_: Any, **__: Any):
        """show(*_, **__)

        Show the dialog.

        .. note:: Override this function to provide your own arguments.

        """
        raise NotImplementedError('\'{}\' not implemented.'.format(self.__class__.show.__name__))

    def build_dialog(self, *_: Any, **__: Any) -> Union[UiDialogBase, None]:
        """build_dialog(*_, **__)

        Build the dialog.

        .. note:: Override this function to provide your own arguments.

        :return: The built dialog or None if a problem occurs.
        :rtype: Union[UiDialogBase, None]
        """
        raise NotImplementedError('\'{}\' not implemented.'.format(self.__class__.build_dialog.__name__))

    def close(self) -> None:
        """close()

        Close the dialog.
        """
        return self._on_close()
