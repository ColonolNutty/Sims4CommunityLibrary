"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.persistence.data_management.common_data_manager import CommonDataManager
from sims4communitylib.persistence.persistence_services.common_persistence_service import CommonPersistenceService


class CommonSettingsDataManager(CommonDataManager):
    """ Manage a storage of settings data. """
    @classmethod
    def get_identifier(cls) -> str:
        """Retrieve the identifier of the data manager. This identifier is used in the name of the settings file."""
        if hasattr(cls, 'IDENTIFIER'):
            return cls.IDENTIFIER
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def persistence_services(self) -> Tuple[CommonPersistenceService]:
        from sims4communitylib.persistence.persistence_services.common_file_persistence_service import \
            CommonFilePersistenceService
        result: Tuple[CommonPersistenceService] = (
            CommonFilePersistenceService(per_save=False),
        )
        return result
