"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.mod_support.mod_identity import CommonModIdentity


class HasModIdentity:
    """An inheritable class that provides Mod Info for a class.

    """
    @property
    def mod_identity(self) -> CommonModIdentity:
        """The identity of a mod.

        .. note:: It contains information about a mod such as Mod Name, Mod Author,\
            the script base namespace, and the file path to your mod.

        :return: The identity of a mod.
        :rtype: CommonModIdentity
        :exception NotImplementedError: Thrown when the property is not implemented.
        """
        raise NotImplementedError('Missing \'{}.mod_identity\'.'.format(self.__class__.__name__))
