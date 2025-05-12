"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from interactions.utils.death import DeathType
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput


class _S4CLReaderForUpdate:
    # noinspection SpellCheckingInspection
    CONVERSIONS = {
        'ANGER': 'ANGER',
        'BEETLES': 'BEETLES',
        'BROKENHEART': 'BROKEN_HEART',
        'CLIMBINGROUTE': 'CLIMBING_ROUTE',
        'COWPLANT': 'COW_PLANT',
        'CROW': 'CROW',
        'DEATHFLOWERARRANGEMENT': 'DEATH_FLOWER_ARRANGEMENT',
        'DROWN': 'DROWN',
        'ELDEREXHAUSTION': 'ELDER_EXHAUSTION',
        'ELECTROCUTION': 'ELECTROCUTION',
        'EMBARRASSMENT': 'EMBARRASSMENT',
        'FIRE': 'FIRE',
        'FLIES': 'FLIES',
        'FROZEN': 'FROZEN',
        'HUNGER': 'HUNGER',
        'KILLERCHICKEN': 'KILLER_CHICKEN',
        'KILLERRABBIT': 'KILLER_RABBIT',
        'LAUGHTER': 'LAUGHTER',
        'LIGHTNING': 'LIGHTNING',
        'METEORITE': 'METEORITE',
        'MOLDSYSTEM': 'MOLD_SYSTEM',
        'MOTHERPLANT': 'MOTHER_PLANT',
        'MURPHYBED': 'MURPHY_BED',
        'OLD AGE': 'OLD_AGE',
        'OVERHEAT': 'OVERHEAT',
        'POISON': 'POISON',
        'PUFFERFISH': 'PUFFERFISH',
        'RODENTDISEASE': 'RODENT_DISEASE',
        'STEAM': 'STEAM',
        'STINKBOMB': 'STINK_BOMB',
        'SUN': 'SUN',
        'URBANMYTH': 'URBAN_MYTH',
        'VENDINGMACHINE': 'VENDING_MACHINE',
        'WITCHOVERLOAD': 'WITCH_OVERLOAD',
    }


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib_dev.log_death_types', 'Logs a list of death types for easy transfer to CommonDeathType', show_with_help_command=False)
def _common_log_ready_for_update(output: CommonConsoleCommandOutput) -> None:
    output('Logging Death Types to Messages.txt')
    from sims4communitylib_development._development._s4cl_enum_value_update_utils import _S4CLEnumValueUpdateUtils
    from sims4communitylib.enums.common_death_types import CommonDeathType
    not_found_values = _S4CLEnumValueUpdateUtils()._read_values_from_enum(DeathType, _S4CLReaderForUpdate.CONVERSIONS, CommonDeathType)
    output(f'Finished logging Death Types. {len(not_found_values)} values were not found.')
