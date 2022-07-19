"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, Dict

from sims4communitylib.persistence.data_stores.common_data_store import CommonDataStore


class CommonSettingsDataStore(CommonDataStore):
    """ Manages main settings for CM. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_identifier(cls) -> str:
        raise NotImplementedError()

    @property
    def _version(self) -> int:
        """This version indicates the current version of the default data. Changing this value will cause all settings to be wiped and replaced with the default data."""
        raise NotImplementedError()

    @property
    def _default_data(self) -> Dict[str, Any]:
        """ The data used as a default for the settings. """
        return {
            self.__class__._VERSION: self._version,
            **self._build_default_data()
        }.copy()

    def _build_default_data(self) -> Dict[str, Any]:
        raise NotImplementedError()
