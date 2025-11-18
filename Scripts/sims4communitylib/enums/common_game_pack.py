"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Iterator, Tuple

from sims4.common import Pack
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils


class CommonGamePack(CommonInt):
    """The values of each game pack."""
    BASE_GAME: 'CommonGamePack' = 0x0

    # Free Packs
    HOLIDAY_CELEBRATION: 'CommonGamePack' = 0x5  # FP01

    # Expansions
    GET_TO_WORK: 'CommonGamePack' = 0x3  # EP01
    GET_TOGETHER: 'CommonGamePack' = 0x9  # EP02
    CITY_LIVING: 'CommonGamePack' = 0x18  # EP03
    CATS_AND_DOGS: 'CommonGamePack' = 0x19  # EP04
    SEASONS: 'CommonGamePack' = 0x1A  # EP05
    GET_FAMOUS: 'CommonGamePack' = 0x1B  # EP06
    ISLAND_LIVING: 'CommonGamePack' = 0x1C  # EP07
    DISCOVER_UNIVERSITY: 'CommonGamePack' = 0x1D  # EP08
    ECO_LIFESTYLE: 'CommonGamePack' = 0x1E  # EP09
    SNOWY_ESCAPE: 'CommonGamePack' = 0x1F  # EP10
    COTTAGE_LIVING: 'CommonGamePack' = 0x34  # EP11
    HIGH_SCHOOL_YEARS: 'CommonGamePack' = 0x35  # EP12
    GROWING_TOGETHER: 'CommonGamePack' = 0x36  # EP13
    HORSE_RANCH: 'CommonGamePack' = 0x37  # EP14
    FOR_RENT: 'CommonGamePack' = 0x38  # EP15
    LOVESTRUCK: 'CommonGamePack' = 0x39  # EP16
    LIFE_AND_DEATH: 'CommonGamePack' = 0x3A  # EP17
    BUSINESSES_AND_HOBBIES: 'CommonGamePack' = 0x3B  # EP18
    ENCHANTED_BY_NATURE: 'CommonGamePack' = 0x3C  # EP19
    ADVENTURE_AWAITS: 'CommonGamePack' = 0x3D  # EP20

    # Game Packs
    OUTDOOR_RETREAT: 'CommonGamePack' = 0x2  # GP01
    SPA_DAY: 'CommonGamePack' = 0x6  # GP02
    DINE_OUT: 'CommonGamePack' = 0xA  # GP03
    VAMPIRES: 'CommonGamePack' = 0x11  # GP04
    PARENTHOOD: 'CommonGamePack' = 0x12  # GP05
    JUNGLE_ADVENTURE: 'CommonGamePack' = 0x13  # GP06
    STRANGERVILLE: 'CommonGamePack' = 0x14  # GP07
    REALM_OF_MAGIC: 'CommonGamePack' = 0x15  # GP08
    JOURNEY_TO_BATUU: 'CommonGamePack' = 0x16  # GP09
    DREAM_HOME_DECORATOR: 'CommonGamePack' = 0x17  # GP10
    MY_WEDDING_STORIES: 'CommonGamePack' = 0x3E  # GP11
    WEREWOLVES: 'CommonGamePack' = 0x3F  # GP12

    # Stuff Packs
    LUXURY_PARTY_STUFF: 'CommonGamePack' = 0x1  # SP01
    PERFECT_PATIO_STUFF: 'CommonGamePack' = 0x4  # SP02
    COOL_KITCHEN_STUFF: 'CommonGamePack' = 0x7  # SP03
    SPOOKY_STUFF: 'CommonGamePack' = 0x8  # SP04
    MOVIE_HANGOUT_STUFF: 'CommonGamePack' = 0xB  # SP05
    ROMANTIC_GARDEN_STUFF: 'CommonGamePack' = 0xC  # SP06
    KIDS_ROOM_STUFF: 'CommonGamePack' = 0xD  # SP07
    BACKYARD_STUFF: 'CommonGamePack' = 0xE  # SP08
    VINTAGE_GLAMOUR_STUFF: 'CommonGamePack' = 0xF  # SP09
    BOWLING_NIGHT_STUFF: 'CommonGamePack' = 0x10  # SP10
    FITNESS_STUFF: 'CommonGamePack' = 0x20  # SP11
    TODDLERS_STUFF: 'CommonGamePack' = 0x21  # SP12
    LAUNDRY_DAY_STUFF: 'CommonGamePack' = 0x22  # SP13
    MY_FIRST_PET_STUFF: 'CommonGamePack' = 0x23  # SP14
    MOSCHINO_STUFF: 'CommonGamePack' = 0x24  # SP15
    TINY_LIVING_STUFF: 'CommonGamePack' = 0x25  # SP16
    NIFTY_KNITTING_STUFF: 'CommonGamePack' = 0x26  # SP17
    PARANORMAL_STUFF: 'CommonGamePack' = 0x27  # SP18
    HOME_CHEF_HUSTLE_STUFF: 'CommonGamePack' = 0x57  # SP46
    CRYSTAL_CREATIONS_STUFF: 'CommonGamePack' = 0x5A  # SP49

    # Kits
    THROWBACK_FIT_KIT: 'CommonGamePack' = 0x29  # SP20
    COUNTRY_KITCHEN_KIT: 'CommonGamePack' = 0x2A  # SP21
    BUST_THE_DUST_KIT: 'CommonGamePack' = 0x2B  # SP22
    COURTYARD_OASIS_KIT: 'CommonGamePack' = 0x2C  # SP23
    FASHION_STREET_KIT: 'CommonGamePack' = 0x2D  # SP24
    INDUSTRIAL_LOFT_KIT: 'CommonGamePack' = 0x2E  # SP25
    INCHEON_ARRIVALS_KIT: 'CommonGamePack' = 0x2F  # SP26
    MODERN_MENSWEAR_KIT: 'CommonGamePack' = 0x31  # SP28
    BLOOMING_ROOMS_KIT: 'CommonGamePack' = 0x32  # SP29
    CARNAVAL_STREETWEAR_KIT: 'CommonGamePack' = 0x33  # SP30
    DECOR_TO_THE_MAX_KIT: 'CommonGamePack' = 0x48  # SP31
    MOONLIGHT_CHIC_KIT: 'CommonGamePack' = 0x49  # SP32
    LITTLE_CAMPERS_KIT: 'CommonGamePack' = 0x4A  # SP33
    FIRST_FITS_KIT: 'CommonGamePack' = 0x4B  # SP34
    DESERT_LUXE_KIT: 'CommonGamePack' = 0x4C  # SP35
    PASTEL_POP_KIT: 'CommonGamePack' = 0x4D  # SP36
    EVERYDAY_CLUTTER_KIT: 'CommonGamePack' = 0x4E  # SP37
    SIMTIMATES_COLLECTION_KIT: 'CommonGamePack' = 0x4F  # SP38
    BATHROOM_CLUTTER_KIT: 'CommonGamePack' = 0x50  # SP39
    GREENHOUSE_HAVEN_KIT: 'CommonGamePack' = 0x51  # SP40
    BASEMENT_TREASURES_KIT: 'CommonGamePack' = 0x52  # SP41
    GRUNGE_REVIVAL_KIT: 'CommonGamePack' = 0x53  # SP42
    BOOK_NOOK_KIT: 'CommonGamePack' = 0x54  # SP43
    POOLSIDE_SPLASH_KIT: 'CommonGamePack' = 0x55  # SP44
    MODERN_LUXE_KIT: 'CommonGamePack' = 0x56  # SP45
    CASTLE_ESTATE_KIT: 'CommonGamePack' = 0x58  # SP47
    GOTH_GALORE_KIT: 'CommonGamePack' = 0x59  # SP48
    URBAN_HOMAGE_KIT: 'CommonGamePack' = 0x5B  # SP50
    PARTY_ESSENTIALS_KIT: 'CommonGamePack' = 0x5C  # SP51
    RIVIERA_RETREAT_KIT: 'CommonGamePack' = 0x5D  # SP52
    COZY_BISTRO_KIT: 'CommonGamePack' = 0x5E  # SP53
    ARTIST_STUDIO_KIT: 'CommonGamePack' = 0x5F  # SP54
    STORYBOOK_NURSERY_KIT: 'CommonGamePack' = 0x60  # SP55
    SWEET_SLUMBER_PARTY_KIT: 'CommonGamePack' = 0x61  # SP56
    COZY_KITSCH_KIT: 'CommonGamePack' = 0x62  # SP57
    COMFY_GAMER_KIT: 'CommonGamePack' = 0x63  # SP58
    SECRET_SANCTUARY_KIT: 'CommonGamePack' = 0x64  # SP59
    CASANOVA_CAVE_KIT: 'CommonGamePack' = 0x65  # SP60
    REFINED_LIVING_ROOM_KIT: 'CommonGamePack' = 0x66  # SP61
    BUSINESS_CHIC_KIT: 'CommonGamePack' = 0x67  # SP62
    SLEEK_BATHROOM_KIT: 'CommonGamePack' = 0x68  # SP63
    SWEET_ALLURE_KIT: 'CommonGamePack' = 0x69  # SP64
    RESTORATION_WORKSHOP_KIT: 'CommonGamePack' = 0x6A  # SP65
    GOLDEN_YEARS_KIT: 'CommonGamePack' = 0x6B  # SP66
    KITCHEN_CLUTTER_KIT: 'CommonGamePack' = 0x6C  # SP67
    AUTUMN_APPAREL_KIT: 'CommonGamePack' = 0x6E  # SP69
    GRANGE_MUDROOM_KIT: 'CommonGamePack' = 0x70  # SP71
    ESSENTIAL_GLAM_KIT: 'CommonGamePack' = 0x71  # SP72

    #  Unused pack ids
    # SP19: 'CommonGamePack' = 0x28  # SP19
    # SP27: 'CommonGamePack' = 0x30  # SP27
    # GP14: 'CommonGamePack' = 0x41  # GP14
    # GP15: 'CommonGamePack' = 0x42  # GP15
    # GP16: 'CommonGamePack' = 0x43  # GP16
    # GP17: 'CommonGamePack' = 0x44  # GP17
    # GP18: 'CommonGamePack' = 0x45  # GP18
    # GP19: 'CommonGamePack' = 0x46  # GP19
    # GP20: 'CommonGamePack' = 0x47  # GP20
    # SP68: 'CommonGamePack' = 0x6D  # SP68
    # SP70: 'CommonGamePack' = 0x6F  # SP70
    # SP73: 'CommonGamePack' = 0x72  # SP73
    # SP74: 'CommonGamePack' = 0x73  # SP74
    # SP75: 'CommonGamePack' = 0x74  # SP75
    # SP76: 'CommonGamePack' = 0x75  # SP76
    # SP77: 'CommonGamePack' = 0x76  # SP77
    # SP78: 'CommonGamePack' = 0x77  # SP78
    # SP79: 'CommonGamePack' = 0x78  # SP79
    # SP80: 'CommonGamePack' = 0x79  # SP80
    # SP81: 'CommonGamePack' = 0x7A  # SP81
    # SP82: 'CommonGamePack' = 0x7B  # SP82
    # SP83: 'CommonGamePack' = 0x7C  # SP83
    # SP84: 'CommonGamePack' = 0x7D  # SP84
    # SP85: 'CommonGamePack' = 0x7E  # SP85
    # SP86: 'CommonGamePack' = 0x7F  # SP86
    # SP87: 'CommonGamePack' = 0x80  # SP87
    # SP88: 'CommonGamePack' = 0x81  # SP88
    # SP89: 'CommonGamePack' = 0x82  # SP89
    # SP90: 'CommonGamePack' = 0x83  # SP90
    # SP91: 'CommonGamePack' = 0x84  # SP91
    # SP92: 'CommonGamePack' = 0x85  # SP92
    # SP93: 'CommonGamePack' = 0x86  # SP93
    # SP94: 'CommonGamePack' = 0x87  # SP94
    # SP95: 'CommonGamePack' = 0x88  # SP95
    # SP96: 'CommonGamePack' = 0x89  # SP96
    # SP97: 'CommonGamePack' = 0x8A  # SP97
    # SP98: 'CommonGamePack' = 0x8B  # SP98
    # SP99: 'CommonGamePack' = 0x8C  # SP99

    @classmethod
    def get_all(cls, exclude_values: Iterator['CommonGamePack'] = None) -> Tuple['CommonGamePack']:
        """get_all(exclude_values=None)

        Get a collection of all values.

        :param exclude_values: These values will be excluded. If set to None, BASE_GAME will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonGamePack], optional
        :return: A collection of all values.
        :rtype: Tuple[CommonGamePack]
        """
        if exclude_values is None:
            exclude_values = (CommonGamePack.BASE_GAME,)
        # noinspection PyTypeChecker
        value_list: Tuple[CommonGamePack, ...] = tuple([value for value in cls.values if value not in exclude_values])
        return value_list

    @classmethod
    def get_all_names(cls, exclude_values: Iterator['CommonGamePack'] = None) -> Tuple[str]:
        """get_all_names(exclude_values=None)

        Retrieve a collection of the names of all values.

        :param exclude_values: These values will be excluded. If set to None, BASE_GAME will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonGamePack], optional
        :return: A collection of the names of all values.
        :rtype: Tuple[str]
        """
        name_list: Tuple[str] = tuple([value.name for value in cls.get_all(exclude_values=exclude_values)])
        return name_list

    @classmethod
    def get_comma_separated_names_string(cls, exclude_values: Iterator['CommonGamePack'] = None) -> str:
        """get_comma_separated_names_string(exclude_values=None)

        Create a string containing all names of all values, separated by a comma.

        :param exclude_values: These values will be excluded. If set to None, BASE_GAME will be excluded automatically. Default is None.
        :type exclude_values: Iterator[CommonGamePack], optional
        :return: A string containing all names of all values, separated by a comma.
        :rtype: str
        """
        return ', '.join(cls.get_all_names(exclude_values=exclude_values))

    @staticmethod
    def convert_to_vanilla(value: 'CommonGamePack') -> Union[Pack, None]:
        """convert_to_vanilla(value)

        Convert a value into the vanilla Pack enum.

        :param value: An instance of CommonGamePack
        :type value: CommonGamePack
        :return: The specified value translated to Pack or None if the value could not be translated.
        :rtype: Union[Pack, None]
        """
        if value is None:
            return None
        if isinstance(value, Pack):
            return value
        return CommonResourceUtils.get_enum_by_int_value(int(value), Pack, default_value=None)

    @staticmethod
    def convert_from_vanilla(value: Union[int, Pack]) -> Union['CommonGamePack', None]:
        """convert_from_vanilla(value)

        Convert a value into a CommonGamePack enum.

        :param value: An instance of Pack
        :type value: Pack
        :return: The specified value translated to CommonGamePack or None if the value could not be translated.
        :rtype: Union[CommonGamePack, None]
        """
        if value is None:
            return None
        if isinstance(value, CommonGamePack):
            return value
        return CommonResourceUtils.get_enum_by_int_value(int(value), CommonGamePack, default_value=None)
