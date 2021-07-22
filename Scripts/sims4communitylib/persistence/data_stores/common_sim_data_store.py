"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Dict, Any
from sims4communitylib.persistence.data_stores.common_data_store import CommonDataStore


class CommonSimDataStore(CommonDataStore):
    """ A store of Sim Data. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_identifier(cls) -> str:
        return 'sim_data'

    @property
    def _version(self) -> int:
        return 1

    @property
    def _default_data(self) -> Dict[str, Any]:
        return dict()

    # noinspection PyMissingOrEmptyDocstring
    def get_default_value_by_key(self, key: str) -> Any:
        return dict()
