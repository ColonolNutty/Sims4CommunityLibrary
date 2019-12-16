"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.mod_support.mod_identity import CommonModIdentity


class HasModIdentity:
    """ Base class for classes with a mod identity. """
    @property
    def mod_identity(self) -> CommonModIdentity:
        """ The Identity of the mod that owns this class. """
        raise NotImplementedError('Missing \'{}\'.'.format(self.__class__.mod_identity.__name__))
