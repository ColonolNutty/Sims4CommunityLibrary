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
    """An inheritable class that will add a log and mod identity to a class.

    """
    def __init__(self):
        self._log: CommonLog = None
        self._mod_identity: CommonModIdentity = None

    @property
    def mod_identity(self) -> CommonModIdentity:
        """The identity of the mod that owns this property

        .. warning:: Override this property with the :class:`.CommonModIdentity` of your mod.

            This is a *MUST* override to allow for proper Exception Handling and Logging!

        """
        raise NotImplementedError('Missing \'{}\'.'.format(self.__class__.mod_identity.__name__))

    @property
    def log(self) -> CommonLog:
        """The Log for this class.

        .. note:: It uses the `mod_identity` and `log_identifier` when logging.
        """
        if self._log is None:
            mod_name = 'Missing Mod Name'
            if self.mod_identity is not None:
                mod_name = self.mod_identity.name
            self._log = CommonLogRegistry.get().register_log(mod_name, self.log_identifier)
        return self._log

    @property
    def log_identifier(self) -> str:
        """The string identifier for the Log of this class.

        .. note:: This is the string that will appear when logging messages using this logger

        :return: The identifier for the log
        :rtype: str
        """
        return self.__class__.__name__
