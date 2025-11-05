"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.mod_support.common_mod_info import CommonModInfo


class ModInfo(CommonModInfo):
    """Contains details related to the mod itself.

    """
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
        return '3.17'
