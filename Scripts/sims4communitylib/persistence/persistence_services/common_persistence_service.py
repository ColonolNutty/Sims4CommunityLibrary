"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict, Any

from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo


class CommonPersistenceService(HasLog):
    """CommonPersistenceService()

    A service used to persist data.

    """

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'common_persistence_service'

    def __init__(self) -> None:
        super().__init__()
        if self.__class__.__name__ == CommonPersistenceService.__name__:
            raise RuntimeError('{} cannot be created directly. You must inherit from it to create an instance of it.'.format(self.__class__.__name__))

    def _format_data_name(self, mod_identity: CommonModIdentity, identifier: str=None) -> str:
        if identifier is not None:
            return '{}_{}'.format(mod_identity.base_namespace, identifier.replace(' ', '_')).lower()
        else:
            return '{}_main'.format(mod_identity.base_namespace).lower()

    def load(self, mod_identity: CommonModIdentity, identifier: str=None) -> Dict[str, Any]:
        """load(mod_identity, identifier=None)

        Load persisted data for the specified Mod Identity.

        :param mod_identity: The identity of the mod that data is being loaded for.
        :type mod_identity: CommonModIdentity
        :param identifier: If set, the identifier will be used to make the data name even more unique. Don't set it if you don't need to! Default is None.
        :type identifier: str, optional
        :return: A library of data.
        :rtype: Dict[str, Any]
        """
        raise NotImplementedError()

    def save(self, mod_identity: CommonModIdentity, data: Dict[str, Any], identifier: str=None) -> bool:
        """save(mod_identity, data, identifier=None)

        Save persisted data for the specified Mod Identity.

        :param mod_identity: The identity of the mod that data is being saved for.
        :type mod_identity: CommonModIdentity
        :param data: The data being persisted.
        :type data: Dict[str, Any]
        :param identifier: If set, the identifier will be used to make the data name even more unique. Don't set it if you don't need to! Default is None.
        :type identifier: str, optional
        :return: True, if the data was persisted successfully. False, if not.
        :rtype: bool
        """
        raise NotImplementedError()

    def remove(self, mod_identity: CommonModIdentity, identifier: str=None) -> bool:
        """remove(mod_identity)

        Removed persisted data for the specified Mod Identity.

        :param mod_identity: The identity of the mod that data is being removed for.
        :type mod_identity: CommonModIdentity
        :param identifier: If set, the identifier will be used to make the data name even more unique. Don't set it if you don't need to! Default is None.
        :type identifier: str, optional
        :return: True, if the data was removed successfully. False, if not.
        :rtype: bool
        """
        raise NotImplementedError()
