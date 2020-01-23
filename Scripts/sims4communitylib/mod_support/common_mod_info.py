"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService


class CommonModInfo(CommonService):
    """Information about a mod.

    """
    @classmethod
    def get_identity(cls) -> CommonModIdentity:
        """Retrieve an identity for this mod.

        """
        identity_property_name = '_MOD_IDENTITY'
        if getattr(cls, identity_property_name, None) is None:
            mod_info: CommonModInfo = cls.get()
            setattr(cls, identity_property_name, CommonModIdentity(mod_info._name, mod_info._author, mod_info._base_namespace, mod_info._file_path))
        return getattr(cls, identity_property_name)

    @property
    def _name(self) -> str:
        """The name of a mod without spaces.

        """
        raise NotImplementedError('Missing \'{}\'.'.format(self.__class__._name.__name__))

    @property
    def _author(self) -> str:
        """The author of a mod.

        """
        raise NotImplementedError('Missing \'{}\'.'.format(self.__class__._author.__name__))

    @property
    def _base_namespace(self) -> str:
        """The namespace of the ts4script file of a mod.
        Example: S4CL has a base name of sims4communitylib.

        """
        raise NotImplementedError('Missing \'{}\'.'.format(self.__class__._base_namespace.__name__))

    @property
    def _file_path(self) -> str:
        """The path to the ts4script file of a mod.

        """
        raise NotImplementedError('Missing \'{}\'.'.format(self.__class__._file_path.__name__))
