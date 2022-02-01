"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.mod_support.has_mod_identity import HasModIdentity
from sims4communitylib.mod_support.mod_identity import CommonModIdentity


class HasClassModIdentity(HasModIdentity):
    """An inheritable class that provides Mod Info for a class.

    .. note:: This class inherits from :class:`.HasModIdentity` and may be used as an alternative to it.

    """
    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return self.__class__.get_mod_identity()

    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        """The identity of a mod.

        .. note:: It contains information about a mod such as Mod Name, Mod Author,\
            the script base namespace, and the file path to your mod.

        :return: The identity of a mod.
        :rtype: CommonModIdentity
        """
        raise NotImplementedError(f'Missing \'{cls.get_mod_identity.__name__}\'.')
