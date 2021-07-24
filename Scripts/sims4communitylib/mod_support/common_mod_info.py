"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.common_service import CommonService


class CommonModInfo(CommonService):
    """Provide information about your mod.

    For information on what each of the properties represents, see :class:`.CommonModIdentity`

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        from sims4communitylib.mod_support.common_mod_info import CommonModInfo

        # This is how the sims4communitylib.modinfo.ModInfo implementation works.
        class ModInfo(CommonModInfo):
            _FILE_PATH: str = str(__file__)

            @property
            def _name(self) -> str:
                return 'Sims4CommunityLib'

            @property
            def _author(self) -> str:
                return 'ColonolNutty'

            @property
            def _base_namespace(self) -> str:
                return 'sims4communitylib'

            @property
            def _file_path(self) -> str:
                return ModInfo._FILE_PATH

            @property
            def _version(self) -> str:
                return '3.5.6'

    """
    @classmethod
    def get_identity(cls) -> CommonModIdentity:
        """The identity of a mod

        .. note:: It contains information about a mod such as Mod Name, Mod Author,\
            the script base namespace, and the file path to your mod.

        :return: The identity of a mod.
        :rtype: CommonModIdentity
        """
        identity_property_name = '_MOD_IDENTITY'
        if getattr(cls, identity_property_name, None) is None:
            mod_info: CommonModInfo = cls.get()
            setattr(cls, identity_property_name, CommonModIdentity(mod_info._name, mod_info._author, mod_info._base_namespace, mod_info._file_path, mod_info._version))
        return getattr(cls, identity_property_name)

    @property
    def _name(self) -> str:
        raise NotImplementedError('Missing \'{}._name\'.'.format(self.__class__.__name__))

    @property
    def _author(self) -> str:
        raise NotImplementedError('Missing \'{}._author\'.'.format(self.__class__.__name__))

    @property
    def _base_namespace(self) -> str:
        raise NotImplementedError('Missing \'{}._base_namespace\'.'.format(self.__class__.__name__))

    @property
    def _file_path(self) -> str:
        raise NotImplementedError('Missing \'{}._file_path\'.'.format(self.__class__.__name__))

    @property
    def _version(self) -> str:
        return '1.0'
