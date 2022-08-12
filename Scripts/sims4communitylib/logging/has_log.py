"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import TYPE_CHECKING, Union
from sims4communitylib.mod_support.has_mod_identity import HasModIdentity
from sims4communitylib.mod_support.mod_identity import CommonModIdentity

if TYPE_CHECKING:
    from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry


class HasLog(HasModIdentity):
    """HasLog()

    An inheritable class that will add a log and mod identity to a class.

    """
    def __init__(self) -> None:
        self._log: Union['CommonLog', None] = None
        self._verbose_log: Union['CommonLog', None] = None
        self._mod_identity: Union[CommonModIdentity, None] = None

    @property
    def mod_identity(self) -> CommonModIdentity:
        """The identity of the mod that owns this property

        .. warning:: Override this property with the :class:`.CommonModIdentity` of your mod.

            This is a *MUST* override to allow for proper Exception Handling and Logging!

        :return: An instance of CommonModIdentity
        :rtype: CommonModIdentity
        :exception NotImplementedError: Thrown when the property is not implemented.
        """
        raise NotImplementedError(f'Missing \'{self.__class__.__name__}.mod_identity\'.')

    @property
    def verbose_log(self) -> 'CommonLog':
        """The verbose log for instances of the class.

        .. note:: It uses the `mod_identity` and `verbose_log_identifier` when logging.

        .. note:: This log can be used to log extra details that you don't want to appear when using the non verbose log.

        :return: An instance of CommonLog
        :rtype: CommonLog
        """
        if self._verbose_log is None:
            from sims4communitylib.utils.common_log_registry import CommonLogRegistry
            self._verbose_log = CommonLogRegistry.get().register_log(self.mod_identity, self.verbose_log_identifier)
        return self._verbose_log

    @property
    def log(self) -> 'CommonLog':
        """The log for instances of the class.

        .. note:: It uses the `mod_identity` and `log_identifier` when logging.

        :return: An instance of CommonLog
        :rtype: CommonLog
        """
        if self._log is None:
            from sims4communitylib.utils.common_log_registry import CommonLogRegistry
            self._log = CommonLogRegistry.get().register_log(self.mod_identity, self.log_identifier)
            if self._verbose_log is None:
                self._verbose_log = CommonLogRegistry.get().register_log(self.mod_identity, self.verbose_log_identifier)
        return self._log

    @property
    def log_identifier(self) -> str:
        """A string identifier for the log used by instances of the class.

        .. note:: This is the message identifier that will appear when logging messages.

        :return: The identifier of the log
        :rtype: str
        """
        return self.__class__.__name__

    @property
    def verbose_log_identifier(self) -> str:
        """A string identifier for the verbose log used by instances of the class.

        .. note:: This is the message identifier that will appear when logging messages.

        :return: The identifier of the verbose log
        :rtype: str
        """
        return f'{self.log_identifier}_verbose'
