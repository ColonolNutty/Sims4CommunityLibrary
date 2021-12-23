"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from sims4.common import Pack


class CommonGamePackUtils:
    """ Utilities for checking various information about Game Packs and their availability. """

    @staticmethod
    def has_game_pack_available(game_pack: Pack) -> bool:
        """has_game_pack_available(game_pack)

        Whether or not the specified Game Pack is available.

        :param game_pack: The Game Pack to check for.
        :type game_pack: Pack
        :return: True, if the specified Game Pack is available. False, if not.
        :rtype: bool
        """
        from sims4.common import is_available_pack
        return is_available_pack(game_pack)

    @staticmethod
    def has_game_packs_available(game_packs: Tuple[Pack]) -> bool:
        """has_game_packs_available(game_packs)

        Whether or not the specified Game Pack is available.

        :param game_packs: The Game Packs to check for.
        :type game_packs: Tuple[Pack]
        :return: True, if all of the specified Game Packs are available. False, if any of them are not available.
        :rtype: bool
        """
        from sims4.common import are_packs_available
        return are_packs_available(game_packs)

    @staticmethod
    def get_available_game_packs() -> Tuple[Pack]:
        """get_available_game_packs()

        Retrieve a collection of all available Game Packs.

        :return: A collection of all Game Packs currently available and installed.
        :rtype: Tuple[Pack]
        """
        from sims4.common import get_available_packs
        return tuple(get_available_packs())

    @staticmethod
    def get_game_pack_name(game_pack: Pack) -> str:
        """get_game_pack_name(game_pack)

        Retrieve the name of a Game Pack.

        :param game_pack: The Game Pack to retrieve the name of.
        :type game_pack: Pack
        :return: The name of the Game Pack or <Unknown Pack> if not available.
        :rtype: str
        """
        from sims4.common import get_pack_name
        return get_pack_name(game_pack)
