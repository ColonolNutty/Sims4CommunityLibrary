"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Union

from sims4.common import Pack
from sims4communitylib.enums.common_game_pack import CommonGamePack
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_log_registry import CommonLogRegistry


class CommonGamePackUtils:
    """ Utilities for checking various information about Game Packs and their availability. """

    @staticmethod
    def has_game_pack_available(game_pack: Union[CommonGamePack, Pack]) -> bool:
        """has_game_pack_available(game_pack)

        Whether or not the specified Game Pack is available.

        :param game_pack: The Game Pack to check for.
        :type game_pack: Union[CommonGamePack, Pack]
        :return: True, if the specified Game Pack is available. False, if not.
        :rtype: bool
        """
        from sims4.common import is_available_pack
        game_pack = CommonGamePack.convert_to_vanilla(game_pack)
        return is_available_pack(game_pack)

    @staticmethod
    def has_game_packs_available(game_packs: Tuple[Union[CommonGamePack, Pack]]) -> bool:
        """has_game_packs_available(game_packs)

        Whether or not the specified Game Pack is available.

        :param game_packs: The Game Packs to check for.
        :type game_packs: Tuple[Union[CommonGamePack, Pack]]
        :return: True, if all of the specified Game Packs are available. False, if any of them are not available.
        :rtype: bool
        """
        from sims4.common import are_packs_available
        game_packs = [CommonGamePack.convert_to_vanilla(game_pack) for game_pack in game_packs if CommonGamePack.convert_to_vanilla(game_pack) is not None]
        return are_packs_available(game_packs)

    @staticmethod
    def get_available_game_packs() -> Tuple[Union[CommonGamePack, Pack]]:
        """get_available_game_packs()

        Retrieve a collection of all available Game Packs.

        :return: A collection of all Game Packs currently available and installed.
        :rtype: Tuple[Union[CommonGamePack, Pack]]
        """
        from sims4.common import get_available_packs
        return tuple(get_available_packs())

    @staticmethod
    def get_game_pack_name(game_pack: Union[CommonGamePack, Pack]) -> str:
        """get_game_pack_name(game_pack)

        Retrieve the name of a Game Pack.

        :param game_pack: The Game Pack to retrieve the name of.
        :type game_pack: Union[CommonGamePack, Pack]
        :return: The name of the Game Pack or <Unknown Pack> if not available.
        :rtype: str
        """
        from sims4.common import get_pack_name
        return get_pack_name(game_pack)


log = CommonLogRegistry().register_log(ModInfo.get_identity(), 's4cl_game_pack_utils')
log.enable()


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.print_available_packs', 'Print the game packs available in the game.')
def _common_print_available_game_packs(output: CommonConsoleCommandOutput):
    output('Printing the available game packs.')
    for game_pack in CommonGamePack.get_all():
        is_available = CommonGamePackUtils.has_game_pack_available(game_pack)
        pack_value = CommonGamePack.convert_to_vanilla(game_pack)
        if is_available:
            output(f'{game_pack.name} ({pack_value.name}): Available')
            log.debug(f'{game_pack.name} ({pack_value.name}): Available')
        else:
            output(f'{game_pack.name} ({pack_value.name}): Not Available')
            log.debug(f'{game_pack.name} ({pack_value.name}): Not Available')


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.print_pack_values', 'Print Pack values.')
def _common_print_pack_values(output: CommonConsoleCommandOutput):
    output('Doing')
    for pack in Pack:
        pack_name = str(pack).replace('Pack.', '')
        pack_hex_value = str(hex(int(pack)))
        output(f'{pack_name} = {pack_hex_value}')
        log.debug(f'{pack_name} = {pack_hex_value}')
    output('Done')
