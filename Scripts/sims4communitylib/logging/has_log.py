"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.mod_support.has_mod_identity import HasModIdentity
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry


class HasLog(HasModIdentity):
    """HasLog()

    An inheritable class that will add a log and mod identity to a class.

    """
    def __init__(self) -> None:
        self._log: CommonLog = None
        self._mod_identity: CommonModIdentity = None

    @property
    def mod_identity(self) -> CommonModIdentity:
        """The identity of the mod that owns this property

        .. warning:: Override this property with the :class:`.CommonModIdentity` of your mod.

            This is a *MUST* override to allow for proper Exception Handling and Logging!

        :return: An instance of CommonModIdentity
        :rtype: CommonModIdentity
        :exception NotImplementedError: Thrown when the property is not implemented.
        """
        raise NotImplementedError('Missing \'{}.mod_identity\'.'.format(self.__class__.__name__))

    @property
    def log(self) -> CommonLog:
        """The log for instances of the class.

        .. note:: It uses the `mod_identity` and `log_identifier` when logging.

        :return: An instance of CommonLog
        :rtype: CommonLog
        """
        if self._log is None:
            mod_name = CommonModIdentity._get_mod_name(self.mod_identity)
            self._log = CommonLogRegistry.get().register_log(mod_name, self.log_identifier)
        return self._log

    @property
    def log_identifier(self) -> str:
        """A string identifier for the log used by instances of the class.

        .. note:: This is the text that will appear when logging messages.

        :return: The identifier of the log
        :rtype: str
        """
        return self.__class__.__name__
