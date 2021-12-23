"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from sims4communitylib.mod_support.mod_identity import CommonModIdentity


class CommonModIdentityUtils:
    """Utilities for manipulating CommonModIdentity.

    """
    @classmethod
    def determine_mod_name_from_identifier(cls, identifier: Union[str, 'CommonModIdentity'], include_version: bool=True) -> str:
        """determine_mod_name_from_identifier(mod_identifier, include_version=True)
        
        Determine the name of a Mod using a mod identifier.
        
        :param identifier: The identifier of a Mod.
        :type identifier: Union[str, 'CommonModIdentity']
        :param include_version: If True and the identifier is a CommonModIdentity object, the version will be included in the mod name. If False, it will not be.
        :return: The name of the Mod or 'Unknown_Mod' if the name could not be determined.
        :rtype: str
        """
        from sims4communitylib.mod_support.mod_identity import CommonModIdentity
        if identifier is None:
            return 'Unknown_Mod'
        if isinstance(identifier, CommonModIdentity):
            return identifier.name.replace(' ', '_').replace(':', '_').replace('//', '_').replace('\\', '_') + (('_' + identifier.version.replace(':', '_').replace('//', '_').replace('\\', '_')) if identifier.version is not None and include_version else '')
        if isinstance(identifier, str):
            return identifier.replace(' ', '_').replace(':', '_').replace('//', '_').replace('\\', '_')
        return str(identifier).replace(' ', '_').replace(':', '_').replace('//', '_').replace('\\', '_')
