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
    def determine_mod_name_from_identifier(cls, identifier: Union[str, 'CommonModIdentity']) -> str:
        """determine_mod_name_from_identifier(mod_identifier)
        
        Determine the name of a Mod using a mod identifier.
        
        :param identifier: The identifier of a Mod.
        :type identifier: Union[str, 'CommonModIdentity']
        :return: The name of the Mod or 'Unknown_Mod' if the name could not be determined.
        :rtype: str
        """
        from sims4communitylib.mod_support.mod_identity import CommonModIdentity
        if identifier is None:
            return 'Unknown_Mod'
        if isinstance(identifier, CommonModIdentity):
            return identifier.name.replace(' ', '_') + (('_' + identifier.version)if identifier.version is not None else '')
        if isinstance(identifier, str):
            return identifier.replace(' ', '_')
        return str(identifier).replace(' ', '_')
