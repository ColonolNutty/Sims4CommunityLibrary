"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.mod_support.has_mod_identity import HasModIdentity
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry


class HasLog(HasModIdentity):
    """ Base class for classes with a log. """
    def __init__(self):
        self._log: CommonLog = None
        self._mod_identity: CommonModIdentity = None

    @property
    def mod_identity(self) -> CommonModIdentity:
        """ The Identity of the mod that owns this class. """
        raise NotImplementedError('Missing \'{}\'.'.format(self.__class__.mod_identity.__name__))

    @property
    def log(self) -> CommonLog:
        """ The Log for this class. """
        if self._log is None:
            mod_name = 'Missing Mod Name'
            if self.mod_identity is not None:
                mod_name = self.mod_identity.name
            self._log = CommonLogRegistry.get().register_log(mod_name, self.log_identifier)
        return self._log

    @property
    def log_identifier(self) -> str:
        """ An identifier for the Log of this class. """
        return self.__class__.__name__
