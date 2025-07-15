"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4.resources import Types
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput


class _S4CLReaderForUpdate:
    # noinspection SpellCheckingInspection
    CONVERSIONS = {
        'CAREER_CAREER_DOCTORCLINIC': 'CAREER_DOCTOR_CLINIC',
        'REGION_BGDEBUG_MEGALOTSTESTWORLD': 'TEST_WORLD_MEGA_LOTS',
        'REGION_CAREER_ALIENWORLD': 'ALIEN_WORLD',
        'REGION_CAREER_POLICESTATION': 'POLICE_STATION',
        'REGION_CAREER_RETAIL': 'RETAIL',
        'REGION_CAREER_SCIENCELAB': 'SCIENCE_LAB',
        'REGION_DEBUG_EP07_TESTWORLD': 'TEST_WORLD_EP07',
        'REGION_DEBUG_MAGALOG': 'TEST_WORLD_MAGALOG',
        'REGION_DEBUG_PERFTEST': 'TEST_WORLD_PERFORMANCE',
        'REGION_DEBUG_TESTWORLD': 'TEST_WORLD',
        'REGION_DEBUG_TESTWORLD_GP02': 'TEST_WORLD_GP02',
        'REGION_DESTINATION_BATUU': 'BATUU',
        'REGION_DESTINATION_CAMPINGFOREST': 'CAMPING_FOREST',
        'REGION_DESTINATION_JUNGLE': 'JUNGLE',
        'REGION_HIDDEN_ACTINGSTUDIO': 'ACTING_STUDIO',
        'REGION_HIDDEN_FORGOTTENGROTTO': 'FORGOTTEN_GROTTO',
        'REGION_HIDDEN_MAGIC_VENUE': 'MAGIC_VENUE',
        'REGION_HIDDEN_SLYVANGLADE': 'SLYVAN_GLADE',
        'REGION_RESIDENTIAL_BAYAREA': 'BAY_AREA',
        'REGION_RESIDENTIAL_CITYLIFE': 'CITY_LIFE',
        'REGION_RESIDENTIAL_COTTAGEWORLD': 'COTTAGE_WORLD',
        'REGION_RESIDENTIAL_ECOWORLD': 'ECO_WORLD',
        'REGION_RESIDENTIAL_EP14WORLD': 'CHESTNUT_RIDGE',
        'REGION_RESIDENTIAL_EP16WORLD': 'CIUDAD_ENAMORADA',
        'REGION_RESIDENTIAL_EP17WORLD': 'RAVENWOOD',
        'REGION_RESIDENTIAL_EP18WORLD': 'NORDHAVEN',
        'REGION_RESIDENTIAL_EP19WORLD': 'INNISGREEN',
        'REGION_RESIDENTIAL_FAMEWORLD': 'FAME_WORLD',
        'REGION_RESIDENTIAL_HIGHSCHOOLWORLD': 'HIGH_SCHOOL_WORLD',
        'REGION_RESIDENTIAL_ISLANDWORLD': 'ISLAND_WORLD',
        'REGION_RESIDENTIAL_MAGIC': 'MAGIC_WORLD',
        'REGION_RESIDENTIAL_MOUNTAINWORLD': 'MOUNTAIN_WORLD',
        'REGION_RESIDENTIAL_MULTIUNITWORLD': 'TOMARANGE',
        'REGION_RESIDENTIAL_NEWCREST': 'NEW_CREST',
        'REGION_RESIDENTIAL_NORTHEUROPE': 'NORTH_EUROPE',
        'REGION_RESIDENTIAL_OASISSPRINGS': 'OASIS_SPRINGS',
        'REGION_RESIDENTIAL_PETWORLD': 'PET_WORLD',
        'REGION_RESIDENTIAL_STRANGETOWN': 'STRANGE_TOWN',
        'REGION_RESIDENTIAL_UNIVERSITYWORLD': 'UNIVERSITY_WORLD',
        'REGION_RESIDENTIAL_VAMPIREWORLD': 'VAMPIRE_WORLD',
        'REGION_RESIDENTIAL_WEDDINGWORLD': 'WEDDING_WORLD',
        'REGION_RESIDENTIAL_WILLOWCREEK': 'WILLOW_CREEK',
        'REGION_RESIDENTIAL_WOLFTOWN': 'WOLF_TOWN',
    }


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib_dev.log_regions', 'Logs a list of regions for easy transfer to CommonRegionId', show_with_help_command=False)
def _common_log_ready_for_update(output: CommonConsoleCommandOutput) -> None:
    output('Logging Region')
    from sims4communitylib_development._development._s4cl_enum_value_update_utils import _S4CLEnumValueUpdateUtils
    from sims4communitylib.enums.common_region_id import CommonRegionId
    not_found_values = _S4CLEnumValueUpdateUtils()._read_values_from_instance_types(Types.REGION, _S4CLReaderForUpdate.CONVERSIONS, CommonRegionId, skip_not_found=True)
    output(f'Finished logging Regions. {len(not_found_values)} values were not found.')
