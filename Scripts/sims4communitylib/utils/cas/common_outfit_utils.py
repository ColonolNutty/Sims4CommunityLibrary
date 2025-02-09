"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os

from animation.arb import Arb
from buffs.appearance_modifier.appearance_modifier import AppearanceModifier
from buffs.appearance_modifier.appearance_modifier_type import AppearanceModifierType
from buffs.appearance_modifier.appearance_tracker import ModifierInfo
from cas.cas import OutfitData
from sims.outfits.outfit_enums import OutfitCategory, BodyType, OutfitFilterFlag, BodyTypeFlag
from sims.sim_info import SimInfo
from sims.sim_info_base_wrapper import SimInfoBaseWrapper
from sims4.utils import classproperty
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.buffs_enum import CommonBuffId
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.enums.tags_enum import CommonGameTag
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.utils.sims.common_buff_utils import CommonBuffUtils
from singletons import DEFAULT
from typing import Tuple, Union, Dict, Callable, Iterator, Set

ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'

if ON_RTD:
    # noinspection PyMissingOrEmptyDocstring
    class OutfitCategory:

        @classproperty
        def value_to_name(self) -> Dict['OutfitCategory', str]:
            pass

        @classproperty
        def name_to_value(self) -> Dict[str, 'OutfitCategory']:
            pass

    # noinspection PyMissingOrEmptyDocstring
    class BodyType:
        NONE = 0

        @classproperty
        def value_to_name(self) -> Dict['BodyType', str]:
            pass

        @classproperty
        def name_to_value(self) -> Dict[str, 'BodyType']:
            pass

    # noinspection PyMissingOrEmptyDocstring
    class SimInfo:
        pass

if not ON_RTD:
    from sims.outfits.outfit_enums import OutfitCategory, BodyType
    from sims.sim_info import SimInfo


class CommonOutfitUtils(HasClassLog):
    """Utilities for handling Sim outfits.

    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_outfit_utils'

    @classmethod
    def has_permission_to_change_to_nude(cls, sim_info: SimInfo) -> CommonTestResult:
        """has_permission_to_change_to_nude(sim_info)

        Determine if a Sim has permission to change to their Nude (Bathing) outfit.

        .. note:: In the vanilla game, only Adult and Elder Sims have permission to change to Nude.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of the test. True, if the test passes. False, if the test fails.
        :rtype: CommonTestResult
        """
        if not CommonAgeUtils.is_teen_adult_or_elder(sim_info):
            return CommonTestResult(False, reason=f'{sim_info} does not have permission to change to Nude. They are neither a Teen, Adult, Young Adult, nor Elder Sim.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_PERMISSION_TO_CHANGE_INTO_NUDE_SIM_IS_NOT_A_TEEN_ADULT_ELDER, tooltip_tokens=(sim_info,))
        return CommonTestResult(True, reason=f'{sim_info} has permission to change to their Nude outfit.', tooltip_text=CommonStringId.S4CL_SIM_HAS_PERMISSION_TO_CHANGE_INTO_NUDE, tooltip_tokens=(sim_info,))

    @classmethod
    def is_every_day_category(cls, outfit_category: OutfitCategory) -> bool:
        """is_every_day_category(outfit_category)

        Determine if an OutfitCategory is EVERYDAY

        :param outfit_category: The OutfitCategory to check.
        :type outfit_category: OutfitCategory
        :return: True, if the OutfitCategory is OutfitCategory.EVERYDAY. False, if it is not.
        :rtype: bool
        """
        return int(outfit_category) == int(OutfitCategory.EVERYDAY)

    @classmethod
    def is_formal_category(cls, outfit_category: OutfitCategory) -> bool:
        """is_formal_category(outfit_category)

        Determine if an OutfitCategory is FORMAL

        :param outfit_category: The OutfitCategory to check.
        :type outfit_category: OutfitCategory
        :return: True, if the OutfitCategory is OutfitCategory.FORMAL. False, if it is not.
        :rtype: bool
        """
        return int(outfit_category) == int(OutfitCategory.FORMAL)

    @classmethod
    def is_athletic_category(cls, outfit_category: OutfitCategory) -> bool:
        """is_athletic_category(outfit_category)

        Determine if an OutfitCategory is ATHLETIC

        :param outfit_category: The OutfitCategory to check.
        :type outfit_category: OutfitCategory
        :return: True, if the OutfitCategory is OutfitCategory.ATHLETIC. False, if it is not.
        :rtype: bool
        """
        return int(outfit_category) == int(OutfitCategory.ATHLETIC)

    @classmethod
    def is_sleep_category(cls, outfit_category: OutfitCategory) -> bool:
        """is_sleep_category(outfit_category)

        Determine if an OutfitCategory is SLEEP

        :param outfit_category: The OutfitCategory to check.
        :type outfit_category: OutfitCategory
        :return: True, if the OutfitCategory is OutfitCategory.SLEEP. False, if it is not.
        :rtype: bool
        """
        return int(outfit_category) == int(OutfitCategory.SLEEP)

    @classmethod
    def is_party_category(cls, outfit_category: OutfitCategory) -> bool:
        """is_party_category(outfit_category)

        Determine if an OutfitCategory is PARTY

        :param outfit_category: The OutfitCategory to check.
        :type outfit_category: OutfitCategory
        :return: True, if the OutfitCategory is OutfitCategory.PARTY. False, if it is not.
        :rtype: bool
        """
        return int(outfit_category) == int(OutfitCategory.PARTY)

    @classmethod
    def is_bathing_category(cls, outfit_category: OutfitCategory) -> bool:
        """is_bathing_category(outfit_category)

        Determine if an OutfitCategory is BATHING

        :param outfit_category: The OutfitCategory to check.
        :type outfit_category: OutfitCategory
        :return: True, if the OutfitCategory is OutfitCategory.BATHING. False, if it is not.
        :rtype: bool
        """
        return int(outfit_category) == int(OutfitCategory.BATHING)

    @classmethod
    def is_career_category(cls, outfit_category: OutfitCategory) -> bool:
        """is_career_category(outfit_category)

        Determine if an OutfitCategory is CAREER

        :param outfit_category: The OutfitCategory to check.
        :type outfit_category: OutfitCategory
        :return: True, if the OutfitCategory is OutfitCategory.CAREER. False, if it is not.
        :rtype: bool
        """
        return int(outfit_category) == int(OutfitCategory.CAREER)

    @classmethod
    def is_situation_category(cls, outfit_category: OutfitCategory) -> bool:
        """is_situation_category(outfit_category)

        Determine if an OutfitCategory is SITUATION

        :param outfit_category: The OutfitCategory to check.
        :type outfit_category: OutfitCategory
        :return: True, if the OutfitCategory is OutfitCategory.SITUATION. False, if it is not.
        :rtype: bool
        """
        return int(outfit_category) == int(OutfitCategory.SITUATION)

    @classmethod
    def is_special_category(cls, outfit_category: OutfitCategory) -> bool:
        """is_special_category(outfit_category)

        Determine if an OutfitCategory is SPECIAL

        :param outfit_category: The OutfitCategory to check.
        :type outfit_category: OutfitCategory
        :return: True, if the OutfitCategory is OutfitCategory.SPECIAL. False, if it is not.
        :rtype: bool
        """
        return int(outfit_category) == int(OutfitCategory.SPECIAL)

    @classmethod
    def is_swimwear_category(cls, outfit_category: OutfitCategory) -> bool:
        """is_swimwear_category(outfit_category)

        Determine if an OutfitCategory is SWIMWEAR

        :param outfit_category: The OutfitCategory to check.
        :type outfit_category: OutfitCategory
        :return: True, if the OutfitCategory is OutfitCategory.SWIMWEAR. False, if it is not.
        :rtype: bool
        """
        return int(outfit_category) == int(OutfitCategory.SWIMWEAR)

    @classmethod
    def is_hot_weather_category(cls, outfit_category: OutfitCategory) -> bool:
        """is_hot_weather_category(outfit_category)

        Determine if an OutfitCategory is HOTWEATHER

        :param outfit_category: The OutfitCategory to check.
        :type outfit_category: OutfitCategory
        :return: True, if the OutfitCategory is OutfitCategory.HOTWEATHER. False, if it is not.
        :rtype: bool
        """
        # noinspection PyBroadException
        try:
            return int(outfit_category) == int(OutfitCategory.HOTWEATHER)
        except:
            return False

    @classmethod
    def is_cold_weather_category(cls, outfit_category: OutfitCategory) -> bool:
        """is_cold_weather_category(outfit_category)

        Determine if an OutfitCategory is COLDWEATHER

        :param outfit_category: The OutfitCategory to check.
        :type outfit_category: OutfitCategory
        :return: True, if the OutfitCategory is OutfitCategory.COLDWEATHER. False, if it is not.
        :rtype: bool
        """
        # noinspection PyBroadException
        try:
            return int(outfit_category) == int(OutfitCategory.COLDWEATHER)
        except:
            return False

    @classmethod
    def is_batuu_category(cls, outfit_category: OutfitCategory) -> bool:
        """is_batuu_category(outfit_category)

        Determine if an OutfitCategory is BATUU

        :param outfit_category: The OutfitCategory to check.
        :type outfit_category: OutfitCategory
        :return: True, if the OutfitCategory is OutfitCategory.BATUU. False, if it is not.
        :rtype: bool
        """
        # noinspection PyBroadException
        try:
            return int(outfit_category) == int(OutfitCategory.BATUU)
        except:
            return False

    @classmethod
    def get_all_outfit_categories(cls) -> Tuple[OutfitCategory]:
        """get_all_outfit_categories()

        Retrieve a collection of all OutfitCategory types.

        :return: A collection of all OutfitCategories.
        :rtype: Tuple[OutfitCategory]
        """
        return tuple(OutfitCategory.values)

    @classmethod
    def is_wearing_everyday_outfit(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """is_wearing_everyday_outfit(sim_info)

        Determine if a Sim is wearing an Everyday outfit.

        :param sim_info: The Sim to check.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :return: True, if the sim is wearing an everyday outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.is_every_day_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @classmethod
    def is_wearing_formal_outfit(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """is_wearing_formal_outfit(sim_info)

        Determine if a Sim is wearing a Formal outfit.

        :param sim_info: The Sim to check.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :return: True, if the sim is wearing a formal outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.is_formal_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @classmethod
    def is_wearing_athletic_outfit(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """is_wearing_athletic_outfit(sim_info)

        Determine if a Sim is wearing an Athletic outfit.

        :param sim_info: The Sim to check.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :return: True, if the sim is wearing an athletic outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.is_athletic_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @classmethod
    def is_wearing_sleep_outfit(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """is_wearing_sleep_outfit(sim_info)

        Determine if a Sim is wearing a Sleep outfit.

        :param sim_info: The Sim to check.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :return: True, if the sim is wearing a sleep outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.is_sleep_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @classmethod
    def is_wearing_party_outfit(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """is_wearing_party_outfit(sim_info)

        Determine if a Sim is wearing a Party outfit.

        :param sim_info: The Sim to check.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :return: True, if the sim is wearing a party outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.is_party_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @classmethod
    def is_wearing_bathing_outfit(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """is_wearing_bathing_outfit(sim_info)

        Determine if a Sim is wearing a Bathing outfit.

        :param sim_info: The Sim to check.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :return: True, if the sim is wearing their bathing/nude outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.is_bathing_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @classmethod
    def is_wearing_career_outfit(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """is_wearing_career_outfit(sim_info)

        Determine if a Sim is wearing a Career outfit.

        :param sim_info: The Sim to check.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :return: True, if the sim is wearing a career outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.is_career_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @classmethod
    def is_wearing_situation_outfit(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """is_wearing_situation_outfit(sim_info)

        Determine if a Sim is wearing a Situation outfit.

        :param sim_info: The Sim to check.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :return: True, if the sim is wearing a situation outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.is_situation_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @classmethod
    def is_wearing_special_outfit(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """is_wearing_special_outfit(sim_info)

        Determine if a Sim is wearing a Special outfit.

        :param sim_info: The Sim to check.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :return: True, if the sim is wearing a special outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.is_special_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @classmethod
    def is_wearing_swimwear_outfit(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """is_wearing_swimwear_outfit(sim_info)

        Determine if a Sim is wearing a Swimwear outfit.

        :param sim_info: The Sim to check.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :return: True, if the sim is wearing a swimwear outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.is_swimwear_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @classmethod
    def is_wearing_hot_weather_outfit(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """is_wearing_hot_weather_outfit(sim_info)

        Determine if a Sim is wearing a Hot Weather outfit.

        :param sim_info: The Sim to check.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :return: True, if the sim is wearing a hot weather outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.is_hot_weather_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @classmethod
    def is_wearing_cold_weather_outfit(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """is_wearing_cold_weather_outfit(sim_info)

        Determine if a Sim is wearing a Cold Weather outfit.

        :param sim_info: The Sim to check.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :return: True, if the sim is wearing a cold weather outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.is_cold_weather_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @classmethod
    def is_wearing_batuu_outfit(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """is_wearing_batuu_outfit(sim_info)

        Determine if a Sim is wearing a Batuu outfit.

        :param sim_info: The Sim to check.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :return: True, if the sim is wearing a batuu outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.is_batuu_category(CommonOutfitUtils.get_current_outfit_category(sim_info))

    @classmethod
    def is_wearing_towel(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> CommonTestResult:
        """is_wearing_towel(sim_info)

        Determine if a Sim is currently wearing a towel.

        :param sim_info: The Sim to check.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :return: The result of testing. True, if the sim is wearing a towel. False, if not.
        :rtype: CommonTestResult
        """
        return CommonBuffUtils.has_buff(sim_info, CommonBuffId.IS_WEARING_TOWEL)

    @classmethod
    def get_outfit_category_by_name(cls, name: str, default_category: Union[OutfitCategory, None] = OutfitCategory.CURRENT_OUTFIT) -> OutfitCategory:
        """get_outfit_category_by_name(name, default_value=OutfitCategory.CURRENT_OUTFIT)

        Retrieve an OutfitCategory by name.

        :param name: The name of an outfit category.
        :type name: str
        :param default_category: The default outfit category to use if the outfit category is not found using the specified name. Default is OutfitCategory.CURRENT_OUTFIT.
        :type default_category: Union[OutfitCategory, None], optional
        :return: The OutfitCategory with the specified name or OutfitCategory.CURRENT_OUTFIT if no outfit category was found using the specified name.
        :rtype: OutfitCategory
        """
        upper_case_name = str(name).upper().strip()
        return CommonResourceUtils.get_enum_by_name(upper_case_name, OutfitCategory, default_value=default_category)

    @classmethod
    def convert_value_to_outfit_category(cls, value: Union[OutfitCategory, int]) -> Union[OutfitCategory, int]:
        """convert_value_to_outfit_category(value)

        Retrieve an OutfitCategory by value.

        :param value: The value of an outfit category.
        :type value: Union[OutfitCategory, int]
        :return: The OutfitCategory with the specified value or the specified value if no OutfitCategory was found.
        :rtype: Union[OutfitCategory, int]
        """
        if isinstance(value, OutfitCategory):
            return value
        if value in OutfitCategory.value_to_name:
            return CommonResourceUtils.get_enum_by_name(OutfitCategory.value_to_name[value], OutfitCategory, default_value=value)
        return value

    @classmethod
    def get_current_outfit_category(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> OutfitCategory:
        """get_current_outfit_category(sim_info)

        Retrieve the current OutfitCategory and Index of a Sim.

        :param sim_info: The Sim to get the outfit category of.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :return: The OutfitCategory of the current outfit a Sim is wearing.
        :rtype: OutfitCategory
        """
        return CommonOutfitUtils.get_current_outfit(sim_info)[0]

    @classmethod
    def get_current_outfit_index(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> int:
        """get_current_outfit_index(sim_info)

        Retrieve the current OutfitCategory and Index of a Sim.

        .. note:: If a Sim has two Athletic outfits and they are wearing the second outfit, the index would be `1`.

        :param sim_info: The Sim to get the outfit index of.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :return: The index of their current outfit relative to the outfits a Sim has in the current OutfitCategory.
        :rtype: int
        """
        return CommonOutfitUtils.get_current_outfit(sim_info)[1]

    @classmethod
    def get_current_outfit(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> Tuple[OutfitCategory, int]:
        """get_current_outfit(sim_info)

        Retrieve the current OutfitCategory and Index of the current sim.

        .. note:: If a Sim has two Athletic outfits and they are wearing the second outfit, the index would be `1`.

        :param sim_info: The Sim to get the current outfit of.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :return: The OutfitCategory and index of the current outfit a Sim is wearing.
        :rtype: Tuple[OutfitCategory, int]
        """
        if sim_info is None:
            return OutfitCategory.EVERYDAY, 0
        current_outfit = sim_info.get_current_outfit()
        # noinspection PyBroadException
        try:
            current_outfit_category = cls.convert_value_to_outfit_category(current_outfit[0])
        except:
            current_outfit_category = current_outfit[0]
        if current_outfit_category is None:
            current_outfit_category = current_outfit[0]
        return current_outfit_category, current_outfit[1]

    @classmethod
    def get_appearance_modifiers_gen(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper], appearance_modifier_type: AppearanceModifierType, include_appearance_modifier_callback: Callable[[ModifierInfo], bool] = None) -> Iterator[AppearanceModifier]:
        """get_appearance_modifiers_gen(sim_info, appearance_modifier_type, include_appearance_modifier_callback=None)

        Retrieve the appearance modifiers of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :param appearance_modifier_type: The type of appearance modifiers to retrieve.
        :type appearance_modifier_type: AppearanceModifierType
        :param include_appearance_modifier_callback: If an appearance modifier matches this callback, then it will be returned. Default is None.
        :type include_appearance_modifier_callback: Callable[[ModifierInfo], bool], optional
        :return: A collection of appearance modifiers.
        :rtype: Iterator[AppearanceModifier]
        """
        if sim_info is None:
            return tuple()
        if not hasattr(sim_info, 'appearance_tracker') or sim_info.appearance_tracker is None:
            return tuple()
        if appearance_modifier_type is None:
            return
        active_appearance_modifier_info_library: Dict[AppearanceModifierType, Tuple[ModifierInfo]] = sim_info.appearance_tracker._active_appearance_modifier_infos
        if active_appearance_modifier_info_library is None:
            return tuple()
        if appearance_modifier_type not in active_appearance_modifier_info_library:
            return tuple()
        modifier_info_list = active_appearance_modifier_info_library[appearance_modifier_type]
        if not modifier_info_list:
            return tuple()
        for modifier_info in modifier_info_list:
            if modifier_info is None:
                continue
            if include_appearance_modifier_callback is not None and not include_appearance_modifier_callback(modifier_info):
                continue
            yield modifier_info.modifier

    @classmethod
    def get_outfit_data(cls, sim_info: Union[Union[SimInfo, SimInfoBaseWrapper], SimInfoBaseWrapper], outfit_category_and_index: Union[Tuple[OutfitCategory, int], None] = None) -> Union[OutfitData, None]:
        """get_outfit_data(sim_info, outfit_category_and_index=None)

        Retrieve OutfitData for the specified OutfitCategory and Index of a Sim.

        :param sim_info: The Sim to retrieve outfit data of.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :param outfit_category_and_index: The OutfitCategory and Index of the outfit to retrieve data from. Default is the current outfit.
        :type outfit_category_and_index: Union[Tuple[OutfitCategory, int], None], optional
        :return: Outfit Data for the specified outfit or None if the Sim does not have the specified outfit.
        :rtype: Union[OutfitData, None]
        """
        if outfit_category_and_index is None:
            outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)
        if not cls.has_outfit(sim_info, outfit_category_and_index):
            return None
        return sim_info.get_outfit(outfit_category_and_index[0], outfit_category_and_index[1])

    @classmethod
    def has_cas_part_attached(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper], cas_part_id: int, outfit_category_and_index: Tuple[OutfitCategory, int] = None) -> bool:
        """has_any_cas_parts_attached(sim_info, cas_part_id, outfit_category_and_index=None)

        Determine if any of the specified CAS Parts are attached to the Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :param cas_part_id: A CAS Part identifier.
        :type cas_part_id: int
        :param outfit_category_and_index: The OutfitCategory and Index of the outfit to check. Default is the current outfit.
        :type outfit_category_and_index: Union[Tuple[OutfitCategory, int], None], optional
        :return: True, if the Sim has the specified CAS Parts attached to the specified outfit. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.has_any_cas_parts_attached(sim_info, (cas_part_id, ), outfit_category_and_index=outfit_category_and_index)

    @classmethod
    def has_any_cas_parts_attached(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper], cas_part_ids: Tuple[int], outfit_category_and_index: Tuple[OutfitCategory, int] = None) -> bool:
        """has_any_cas_parts_attached(sim_info, cas_part_ids, outfit_category_and_index=None)

        Determine if any of the specified CAS Parts are attached to the Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :param cas_part_ids: A collection of CAS Part identifiers.
        :type cas_part_ids: Tuple[int]
        :param outfit_category_and_index: The OutfitCategory and Index of the outfit to check. Default is the current outfit.
        :type outfit_category_and_index: Union[Tuple[OutfitCategory, int], None], optional
        :return: True, if the Sim has any of the specified CAS Parts attached to the specified outfit. False, if not.
        :rtype: bool
        """
        body_parts = CommonOutfitUtils.get_outfit_parts(sim_info, outfit_category_and_index=outfit_category_and_index)
        if not body_parts:
            return False
        outfit_part_ids = body_parts.values()
        for cas_part_id in cas_part_ids:
            if cas_part_id in outfit_part_ids:
                return True
        return False

    @classmethod
    def get_outfit_parts(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper], outfit_category_and_index: Union[Tuple[OutfitCategory, int], None] = None) -> Dict[Union[BodyType, int], int]:
        """get_outfit_parts(sim_info, outfit_category_and_index=None)

        Retrieve Outfit Parts for the specified OutfitCategory and Index of a Sim.

        :param sim_info: The Sim to retrieve outfit parts of.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :param outfit_category_and_index: The OutfitCategory and Index of the outfit to retrieve data from. Default is the current outfit.
        :type outfit_category_and_index: Union[Tuple[OutfitCategory, int], None], optional
        :return: A dictionary of body types and cas parts in those body types for the outfit of a Sim. If an outfit does not exist, an empty dict will be returned.
        :rtype: Dict[Union[BodyType, int], int]
        """
        if outfit_category_and_index is None:
            outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)
        if not cls.has_outfit(sim_info, outfit_category_and_index):
            return dict()
        outfit_data = sim_info.get_outfit(outfit_category_and_index[0], outfit_category_and_index[1])
        if outfit_data is None:
            return dict()
        return dict(zip(list(outfit_data.body_types), list(outfit_data.part_ids)))

    @classmethod
    def refresh_outfit(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper], outfit_category_and_index: Union[Tuple[OutfitCategory, int], None] = None):
        """refresh_outfit(sim_info, outfit_category_and_index=None)

        Refresh the outfit of a Sim.

        :param sim_info: The info of a Sim.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :param outfit_category_and_index: The OutfitCategory and index to refresh. Default is the Sims current outfit.
        :type outfit_category_and_index: Tuple[OutfitCategory, int], optional
        """
        if outfit_category_and_index is None:
            outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)
        if not cls.has_outfit(sim_info, outfit_category_and_index):
            return
        cls.trigger_outfit_generated(sim_info, outfit_category_and_index)
        cls.set_outfit_dirty(sim_info, outfit_category_and_index[0])
        cls.set_current_outfit(sim_info, outfit_category_and_index)

    @classmethod
    def trigger_outfit_generated(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper], outfit_category_and_index: Tuple[OutfitCategory, int]):
        """trigger_outfit_generated(sim_info, outfit_category_and_index)

        Trigger the outfit generated callbacks for a Sim with an OutfitCategory and Index.

        :param sim_info: The info of a Sim.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :param outfit_category_and_index: The OutfitCategory and index to send.
        :type outfit_category_and_index: Tuple[OutfitCategory, int]
        """
        sim_info.on_outfit_generated(*outfit_category_and_index)

    @classmethod
    def set_current_outfit(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper], outfit_category_and_index: Tuple[OutfitCategory, int]):
        """set_current_outfit(sim_info, outfit_category_and_index)

        Set the current outfit of a Sim to the specified OutfitCategory and Index.

        :param sim_info: The Sim to change the outfit of.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :param outfit_category_and_index: The OutfitCategory and index to change to.
        :type outfit_category_and_index: Tuple[OutfitCategory, int]
        """
        arb = Arb()
        sim_info.try_set_current_outfit(outfit_category_and_index, arb=arb)

    @classmethod
    def set_outfit_dirty(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper], outfit_category: OutfitCategory):
        """set_outfit_dirty(sim_info, outfit_category)

        Flag the specified OutfitCategory of a Sim as dirty.
        This will tell the game that it needs to be updated.

        :param sim_info: The Sim to flag the OutfitCategory for.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :param outfit_category: The OutfitCategory being flagged.
        :type outfit_category: OutfitCategory
        """
        sim_info.set_outfit_dirty(outfit_category)

    @classmethod
    def set_outfit_clean(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper], outfit_category: OutfitCategory):
        """set_outfit_clean(sim_info, outfit_category)

        Flag the specified OutfitCategory of a Sim as clean.

        :param sim_info: The Sim to flag the OutfitCategory for.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :param outfit_category: The OutfitCategory being flagged.
        :type outfit_category: OutfitCategory
        """
        sim_info.clear_outfit_dirty(outfit_category)

    @classmethod
    def generate_outfit(
        cls,
        sim_info: Union[SimInfo, SimInfoBaseWrapper],
        outfit_category_and_index: Tuple[OutfitCategory, int],
        tag_list: Tuple[CommonGameTag] = (),
        outfit_filter_flag: OutfitFilterFlag = DEFAULT,
        body_type_flags: BodyTypeFlag = DEFAULT,
        ignore_if_exists: bool = False,
        **kwargs
    ) -> bool:
        """generate_outfit(\
            sim_info,\
            outfit_category_and_index,\
            tag_list=(),\
            outfit_filter_flag=DEFAULT,\
            body_type_flags=DEFAULT,\
            ignore_if_exists=False,\
            **kwargs\
        )

        Generate an outfit for a Sim for the specified OutfitCategory and Index.

        .. note:: If an outfit exists in the specified OutfitCategory and Index, already, it will be overridden.

        :param sim_info: The Sim to generate an outfit for.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :param outfit_category_and_index: The OutfitCategory and Index of the outfit to generate.
        :type outfit_category_and_index: Tuple[OutfitCategory, int]
        :param tag_list: A collection of tags to match CAS Parts to. Default is any tag.
        :type tag_list: Tuple[CommonGameTag], optional
        :param outfit_filter_flag: Flags to filter CAS Parts with. Default is no flags.
        :type outfit_filter_flag: OutfitFilterFlag, optional
        :param body_type_flags: Flags to filter CAS Parts with. Default is no flags.
        :type body_type_flags: BodyTypeFlag, optional
        :param ignore_if_exists: If set to True, the outfit will not be generated if an outfit already exists at the specified Outfit Category and Index.
        :return: True, if an outfit was generated successfully. False, if not.
        :rtype: bool
        """

        if ignore_if_exists and CommonOutfitUtils.has_outfit(sim_info, outfit_category_and_index):
            cls.get_log().format_with_message('Outfit already existed, no need to generate it!', sim=sim_info, outfit_category_and_index=outfit_category_and_index)
            return False

        outfit_category = outfit_category_and_index[0]
        outfit_index = outfit_category_and_index[1]
        return sim_info.generate_outfit(outfit_category, outfit_index=outfit_index, tag_list=tag_list, filter_flag=outfit_filter_flag, body_type_flags=body_type_flags, **kwargs)

    @classmethod
    def copy_outfit(cls, mod_identity: CommonModIdentity, sim_info: SimInfo, from_outfit_category_and_index: Tuple[OutfitCategory, int], to_outfit_category_and_index: Tuple[OutfitCategory, int], change_sim_to_outfit_after_apply: bool = False) -> bool:
        """copy_outfit(mod_identity, sim_info, from_outfit_category_and_index, to_outfit_category_and_index, change_sim_to_outfit_after_apply=False)

        Copy one Outfit of a Sim to another Outfit of the same Sim.

        :param mod_identity: The identity of the mod copying the outfit.
        :type mod_identity: CommonModIdentity
        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param from_outfit_category_and_index: The Outfit Category and Index to copy CAS Parts from.
        :type from_outfit_category_and_index: Tuple[OutfitCategory, int]
        :param to_outfit_category_and_index: The Outfit Category and Index to copy CAS Parts to.
        :type to_outfit_category_and_index: Tuple[OutfitCategory, int]
        :param change_sim_to_outfit_after_apply: Set to True to change the Sim to the outfit after the changes are applied. Default is False.
        :type change_sim_to_outfit_after_apply: bool, optional
        :return: True, if CAS Parts were copied successfully. False, if not.
        :rtype: bool
        """
        from sims4communitylib.services.sim.cas.common_sim_outfit_io import CommonSimOutfitIO
        outfit_io = CommonSimOutfitIO(sim_info, outfit_category_and_index=from_outfit_category_and_index, mod_identity=mod_identity)
        return outfit_io.apply(change_sim_to_outfit_after_apply=change_sim_to_outfit_after_apply, apply_to_all_outfits_in_same_category=False, apply_to_outfit_category_and_index=to_outfit_category_and_index)

    @classmethod
    def regenerate_outfit(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper], outfit_category_and_index: Tuple[OutfitCategory, int]) -> None:
        """regenerate_outfit(sim_info, outfit_category_and_index)

        Delete and regenerate an outfit of a Sim.

        .. note:: If the Sim does not have the specified outfit to regenerate, it will be generated instead.

        :param sim_info: An instance of a Sim.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :param outfit_category_and_index: The OutfitCategory and index to regenerate for the Sim.
        :type outfit_category_and_index: Tuple[OutfitCategory, int]
        """
        current_outfit = CommonOutfitUtils.get_current_outfit(sim_info)
        outfit_flags = OutfitFilterFlag.USE_EXISTING_IF_APPROPRIATE & OutfitFilterFlag.USE_VALID_FOR_LIVE_RANDOM
        tags = tuple()
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        if CommonSimGenderOptionUtils.prefers_menswear(sim_info):
            tags = (CommonGameTag.GENDER_APPROPRIATE_MALE,)
        elif CommonSimGenderOptionUtils.prefers_womenswear(sim_info):
            tags = (CommonGameTag.GENDER_APPROPRIATE_FEMALE,)
        outfit = outfit_category_and_index
        cls.get_log().format_with_message('Generating outfit', outfit=outfit)
        generate_result = CommonOutfitUtils.generate_outfit(sim_info, outfit, outfit_filter_flag=outfit_flags, tag_list=tags)
        cls.get_log().format_with_message('Finished generating outfit', outfit=outfit, generate_result=generate_result, outfit_flags=outfit_flags, tags=tags)
        sim_info.appearance_tracker.evaluate_appearance_modifiers()
        CommonOutfitUtils.resend_outfits(sim_info)
        CommonOutfitUtils.set_current_outfit(sim_info, current_outfit)

    @classmethod
    def regenerate_all_outfits(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> None:
        """regenerate_all_outfits(sim_info)

        Delete and regenerate all outfits for a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        """
        current_outfit = CommonOutfitUtils.get_current_outfit(sim_info)
        outfit_flags = OutfitFilterFlag.USE_EXISTING_IF_APPROPRIATE & OutfitFilterFlag.USE_VALID_FOR_LIVE_RANDOM
        tags = tuple()
        from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
        if CommonSimGenderOptionUtils.prefers_menswear(sim_info):
            tags = (CommonGameTag.GENDER_APPROPRIATE_MALE,)
        elif CommonSimGenderOptionUtils.prefers_womenswear(sim_info):
            tags = (CommonGameTag.GENDER_APPROPRIATE_FEMALE,)
        for outfit_category in CommonOutfitUtils.get_all_outfit_categories():
            for outfit_index in range(cls.get_maximum_number_of_outfits_for_category(outfit_category)):
                outfit = (outfit_category, outfit_index)
                if not CommonOutfitUtils.has_outfit(sim_info, outfit):
                    cls.get_log().format_with_message('Sim did not have outfit.', sim=sim_info, outfit=outfit)
                    continue
                cls.get_log().format_with_message('Generating outfit', outfit=outfit)
                generate_result = CommonOutfitUtils.generate_outfit(sim_info, outfit, outfit_filter_flag=outfit_flags, tag_list=tags)
                cls.get_log().format_with_message('Finished generating outfit', outfit=outfit, generate_result=generate_result, outfit_flags=outfit_flags, tags=tags)
        sim_info.appearance_tracker.evaluate_appearance_modifiers()
        CommonOutfitUtils.resend_outfits(sim_info)
        CommonOutfitUtils.set_current_outfit(sim_info, current_outfit)

    @classmethod
    def resend_outfits(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """resend_outfits(sim_info)

        Resend outfit data to a Sim to refresh their outfits.

        :param sim_info: The Sim to resend the outfit for.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :return: True, if outfits were resent successfully. False, if not.
        :rtype: bool
        """
        sim_info.resend_outfits()
        return True

    @classmethod
    def get_maximum_number_of_outfits_for_category(cls, outfit_category: OutfitCategory) -> int:
        """get_maximum_number_of_outfits_for_category(outfit_category)

        Retrieve the maximum number of outfits allowed for an outfit category.

        :param outfit_category: The outfit category to check.
        :type outfit_category: OutfitCategory
        :return: The maximum number of Outfits a Sim may have within the specified outfit category.
        :rtype: int
        """
        if outfit_category is None:
            return 0
        from sims.outfits.outfit_utils import get_maximum_outfits_for_category
        return get_maximum_outfits_for_category(outfit_category)

    @classmethod
    def get_previous_outfit(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper], default_outfit_category_and_index: Tuple[OutfitCategory, int] = (OutfitCategory.EVERYDAY, 0)) -> Tuple[OutfitCategory, int]:
        """get_previous_outfit(sim_info, default_outfit_category_and_index=(OutfitCategory.EVERYDAY, 0))

        Retrieve the previous outfit a Sim was wearing before their current outfit.

        :param sim_info: The Sim to get the previous outfit of.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :param default_outfit_category_and_index: A default OutfitCategory and index if no previous outfit was found.
        :type default_outfit_category_and_index: Tuple[OutfitCategory, int], optional
        :return: The OutfitCategory and Index of the outfit a Sim was wearing before their current outfit or the default if none was found.
        :rtype: Tuple[OutfitCategory, int]
        """
        return sim_info.get_previous_outfit() or default_outfit_category_and_index

    @classmethod
    def remove_previous_outfit(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper]):
        """remove_previous_outfit(sim_info)

        Remove the outfit a Sim was wearing before their current outfit, from the cache.

        :param sim_info: The Sim to remove the outfit from.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        """
        sim_info.set_previous_outfit(None, force=True)

    @classmethod
    def get_all_outfit_category_and_indexes(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper], include_outfit_categories: Tuple[OutfitCategory] = ()) -> Tuple[Tuple[OutfitCategory, int]]:
        """get_all_outfit_category_and_indexes(sim_info, include_outfit_categories=())

        Retrieve a collection of outfit category and index for each outfit available to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :param include_outfit_categories: A collection of outfit categories to include. If empty, all outfit categories will be included. Default is empty.
        :type include_outfit_categories: Tuple[OutfitCategory], optional
        :return: A collection of outfit category and index for each outfit available to a Sim.
        :rtype: Tuple[Tuple[OutfitCategory, int]]
        """
        outfits = sim_info.get_outfits()
        outfit_list = list()
        for (outfit_category, _outfit_list) in outfits.get_all_outfits():
            outfit_category: OutfitCategory = outfit_category
            if include_outfit_categories and outfit_category not in include_outfit_categories:
                continue
            for (outfit_index, _) in enumerate(_outfit_list):
                outfit_index: int = outfit_index
                outfit_list.append((outfit_category, outfit_index))
        return tuple(outfit_list)

    @classmethod
    def has_outfit(cls, sim_info: Union[Union[SimInfo, SimInfoBaseWrapper], SimInfoBaseWrapper], outfit_category_and_index: Tuple[OutfitCategory, int]) -> bool:
        """has_outfit(sim_info, outfit_category_and_index)

        Determine if a Sim has an existing outfit in the specified OutfitCategory and Index.

        :param sim_info: The Sim to check.
        :type sim_info: Union[Union[SimInfo, SimInfoBaseWrapper], SimInfoBaseWrapper]
        :param outfit_category_and_index: The OutfitCategory and index to locate.
        :type outfit_category_and_index: Tuple[OutfitCategory, int], optional
        :return: True, if the Sim has the specified OutfitCategory and Index. False, if not.
        :rtype: bool
        """
        return sim_info.has_outfit(outfit_category_and_index)

    @classmethod
    def update_outfits(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper]) -> bool:
        """update_outfits(sim_info)

        Update all outfits of a Sim.

        :param sim_info: The Sim to update outfits for.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :return: True, if the outfits were updated successfully. False, if not.
        :rtype: bool
        """
        sim_info.on_outfit_changed(sim_info, CommonOutfitUtils.get_current_outfit(sim_info), CommonOutfitUtils.get_current_outfit(sim_info))
        CommonOutfitUtils.resend_outfits(sim_info)
        sim_info.appearance_tracker.evaluate_appearance_modifiers()
        return True

    @classmethod
    def has_tag_on_outfit(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper], tag: Union[int, CommonGameTag], outfit_category_and_index: Union[Tuple[OutfitCategory, int], None] = None) -> bool:
        """has_tag_on_outfit(sim_info, tag, outfit_category_and_index=None)

        Determine if the Outfit of a Sim has the specified tag.

        :param sim_info: An instance of a Sim.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :param tag: A tag to locate.
        :type tag: Union[int, CommonGameTag]
        :param outfit_category_and_index: The OutfitCategory and Index of the outfit to retrieve data from. Default is the current outfit.
        :type outfit_category_and_index: Union[Tuple[OutfitCategory, int], None], optional
        :return: True, if the Outfit of the Sim has the specified tag. False, if not.
        :rtype: bool
        """
        return CommonOutfitUtils.has_any_tags_on_outfit(sim_info, (tag, ), outfit_category_and_index=outfit_category_and_index)

    @classmethod
    def has_any_tags_on_outfit(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper], tags: Iterator[Union[int, CommonGameTag]], outfit_category_and_index: Union[Tuple[OutfitCategory, int], None] = None) -> bool:
        """has_any_tags_on_outfit(sim_info, tags, outfit_category_and_index=None)

        Determine if the Outfit of a Sim has any of the specified tags.

        :param sim_info: An instance of a Sim.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :param tags: A collection of tags to locate.
        :type tags: Iterator[Union[int, CommonGameTag]]
        :param outfit_category_and_index: The OutfitCategory and Index of the outfit to retrieve data from. Default is the current outfit.
        :type outfit_category_and_index: Union[Tuple[OutfitCategory, int], None], optional
        :return: True, if the Outfit of the Sim has any of the specified tags. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        if not tags:
            return False
        outfit_tags = CommonOutfitUtils.get_all_outfit_tags(sim_info, outfit_category_and_index=outfit_category_and_index)
        for tag in tags:
            if tag in outfit_tags:
                return True
        return False

    @classmethod
    def has_all_tags_on_outfit(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper], tags: Iterator[Union[int, CommonGameTag]], outfit_category_and_index: Union[Tuple[OutfitCategory, int], None] = None) -> bool:
        """has_all_tags_on_outfit(sim_info, tags, outfit_category_and_index=None)

        Determine if the Outfit of a Sim has all of the specified tags.

        :param sim_info: An instance of a Sim.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :param tags: A collection of tags to locate.
        :type tags: Iterator[Union[int, CommonGameTag]]
        :param outfit_category_and_index: The OutfitCategory and Index of the outfit to retrieve data from. Default is the current outfit.
        :type outfit_category_and_index: Union[Tuple[OutfitCategory, int], None], optional
        :return: True, if the Outfit of the Sim has all of the specified tags. False, if not.
        :rtype: bool
        """
        if sim_info is None:
            return False
        if not tags:
            return False
        outfit_tags = CommonOutfitUtils.get_all_outfit_tags(sim_info, outfit_category_and_index=outfit_category_and_index)
        for tag in tags:
            if tag not in outfit_tags:
                return False
        return True

    @classmethod
    def get_all_outfit_tags(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper], outfit_category_and_index: Union[Tuple[OutfitCategory, int], None] = None) -> Tuple[CommonGameTag]:
        """get_all_outfit_tags(sim_info, outfit_category_and_index=None)

        Retrieve a collection of game tags that apply to the outfit of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :param outfit_category_and_index: The OutfitCategory and Index of the outfit to retrieve data from. Default is the current outfit.
        :type outfit_category_and_index: Union[Tuple[OutfitCategory, int], None], optional
        :return: A collection of Game Tags that apply to the outfit of a Sim.
        :rtype: Tuple[CommonGameTag]
        """
        if sim_info is None:
            return tuple()
        combined_game_tags = list()
        for game_tags in CommonOutfitUtils.get_outfit_tags_by_cas_part_id(sim_info, outfit_category_and_index=outfit_category_and_index).values():
            for game_tag in game_tags:
                if game_tag not in combined_game_tags:
                    combined_game_tags.append(game_tag)
        return tuple(combined_game_tags)

    @classmethod
    def get_outfit_tags_by_cas_part_id(cls, sim_info: Union[SimInfo, SimInfoBaseWrapper], outfit_category_and_index: Union[Tuple[OutfitCategory, int], None] = None) -> Dict[int, Set[CommonGameTag]]:
        """get_outfit_tags_by_cas_part_id(sim_info, outfit_category_and_index=None)

        Retrieve the game tags of the outfit of a Sim grouped by CAS Part Id.

        :param sim_info: An instance of a Sim.
        :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
        :param outfit_category_and_index: The OutfitCategory and Index of the outfit to retrieve data from. Default is the current outfit.
        :type outfit_category_and_index: Union[Tuple[OutfitCategory, int], None], optional
        :return: A library of Game Tags grouped by CAS Part Id.
        :rtype: Dict[int, Tuple[CommonGameTag]]
        """
        if sim_info is None:
            return dict()
        from cas.cas import get_tags_from_outfit
        outfit_category_and_index = outfit_category_and_index or CommonOutfitUtils.get_current_outfit(sim_info)
        # noinspection PyBroadException
        try:
            return get_tags_from_outfit(sim_info._base, outfit_category_and_index[0], outfit_category_and_index[1])
        except:
            return dict()

    @classmethod
    def _print_outfit(cls, sim_info: SimInfo, outfit_category: OutfitCategory, outfit_index: int, output: CommonConsoleCommandOutput):
        from sims4communitylib.services.sim.cas.common_sim_outfit_io import CommonSimOutfitIO
        if not isinstance(outfit_category, OutfitCategory):
            # noinspection PyBroadException
            try:
                outfit_category = CommonResourceUtils.get_enum_by_int_value(int(outfit_category), OutfitCategory, default_value=outfit_category)
            except:
                output(f'ERROR: Failed to parse {outfit_category} as OutfitCategory.')
                return

        # noinspection PyBroadException
        if hasattr(outfit_category, 'name'):
            outfit_category_name = outfit_category.name
        else:
            outfit_category_name = outfit_category

        output(f'Outfit Info for outfit ({outfit_category_name}, {outfit_index}) of Sim {sim_info}')
        outfit_commands_log.debug(f'Outfit Info for outfit ({outfit_category_name}, {outfit_index}) of Sim {sim_info}')
        outfit_io = CommonSimOutfitIO(sim_info, outfit_category_and_index=(outfit_category, outfit_index))
        output(f'------Outfit: ({outfit_category_name}, {outfit_index})------')
        outfit_commands_log.debug(f'------Outfit: ({outfit_category_name}, {outfit_index})------')
        for (body_type, cas_part_id) in zip(outfit_io.body_types, outfit_io.cas_part_ids):
            body_type_value = int(body_type)
            if not isinstance(body_type, BodyType):
                # noinspection PyBroadException
                try:
                    body_type = CommonResourceUtils.get_enum_by_int_value(int(body_type), BodyType, default_value=body_type)
                except:
                    output(f'    {str(body_type)} ({body_type_value}): {cas_part_id}')
                    outfit_commands_log.debug(f'{str(body_type)} ({body_type_value}): {cas_part_id}')
                    continue
            if hasattr(body_type, 'name'):
                body_type_name = body_type.name
            else:
                body_type_name = str(body_type)
            output(f'    {body_type_name} ({body_type_value}): {cas_part_id}')
            outfit_commands_log.debug(f'{body_type_name} ({body_type_value}): {cas_part_id}')
        output('----------------------------')
        output('-')
        outfit_commands_log.debug('----------------------------')
        outfit_commands_log.debug('-')

    @classmethod
    def _parse_outfit_category_and_index_from_str(cls, output: CommonConsoleCommandOutput, outfit_category: str, outfit_index: int, sim_info: SimInfo = None, check_for_missing_outfit: bool = True, outfit_category_required: bool = False) -> Union[Tuple[OutfitCategory, int], None]:
        outfit_category_value_names = ', '.join(OutfitCategory.name_to_value.keys())
        if outfit_category is None:
            if outfit_category_required:
                output(f'ERROR: Outfit Category not specified. Valid OutfitCategory: ({outfit_category_value_names})')
            return None
        if outfit_index <= 0:
            output('ERROR: Outfit Index must be a value above Zero.')
            return None
        if not outfit_category.isnumeric():
            outfit_category_value = CommonResourceUtils.get_enum_by_name(outfit_category.upper(), OutfitCategory, default_value=None)
            if outfit_category_value is None:
                output(f'ERROR: No Outfit Category existed with name {outfit_category}. Valid OutfitCategory: ({outfit_category_value_names})')
                return
        else:
            try:
                outfit_category_value = int(outfit_category)
            except ValueError:
                output(f'ERROR: The specified outfit category is neither a number nor the name of an OutfitCategory {outfit_category}. Valid OutfitCategory: ({outfit_category_value_names})')
                return
            outfit_category_value = CommonResourceUtils.get_enum_by_int_value(outfit_category_value, OutfitCategory, default_value=None)
            if outfit_category_value is None:
                output(f'ERROR: No Outfit Category existed with value {outfit_category}. Valid OutfitCategory: ({outfit_category_value_names})')
                return

        outfit_category_and_index = (outfit_category_value, outfit_index)
        if check_for_missing_outfit and sim_info is not None:
            if not CommonOutfitUtils.has_outfit(sim_info, outfit_category_and_index):
                output(f'ERROR: The Sim {sim_info} did not have the specified outfit {outfit_category_and_index[0].name} at index {outfit_category_and_index[1]}')
                return
        return outfit_category_and_index


outfit_commands_log = CommonLogRegistry().register_log(ModInfo.get_identity(), 's4cl_outfit_commands')
outfit_commands_log.enable()


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.print_all_outfit_categories',
    'Print a list of all outfit categories that are available to Sims.'
)
def _s4clib_testing_print_all_outfit_categories(output: CommonConsoleCommandOutput):
    output('Printing all outfit categories.')
    outfit_categories_name_str = ', '.join([outfit_category.name if hasattr(outfit_category, 'name') else str(outfit_category) for outfit_category in CommonOutfitUtils.get_all_outfit_categories()])
    output(f'Outfit categories: {outfit_categories_name_str}')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.print_outfit_tags',
    'Print a list of all Game Tags applied to the outfit of a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('outfit_category', 'Value or Name', 'The Value or Name of the Outfit Category to check.', is_optional=True, default_value='Current Outfit'),
        CommonConsoleCommandArgument('outfit_index', 'Positive Number', 'The index of the outfit to check. This value does nothing if an Outfit Category is not specified.', is_optional=True, default_value=1),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Sim to check.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib_testing.printoutfittags',
    )
)
def _s4clib_testing_print_outfit_tags(output: CommonConsoleCommandOutput, outfit_category: str = None, outfit_index: int = 1, sim_info: SimInfo = None):
    if sim_info is None:
        return
    outfit_category_and_index = CommonOutfitUtils._parse_outfit_category_and_index_from_str(output, outfit_category=outfit_category, outfit_index=outfit_index, sim_info=sim_info)
    if outfit_category_and_index is None:
        outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)

    output(f'Attempting to print all game tags of outfit ({outfit_category_and_index[0].name}, {outfit_category_and_index[1]}) for Sim {sim_info}.')
    outfit_commands_log.debug(f'Printing all game tags of outfit ({outfit_category_and_index[0].name}, {outfit_category_and_index[1]}) for Sim {sim_info}.')
    outfit_commands_log.debug(f'-------Game Tags For Outfit Category:  ({outfit_category_and_index[0].name}, {outfit_category_and_index[1]})-------')
    tag_values = CommonOutfitUtils.get_all_outfit_tags(sim_info, outfit_category_and_index=outfit_category_and_index)
    cleaned_tag_names = list()
    for tag_value in tag_values:
        if isinstance(tag_value, CommonGameTag):
            tag = tag_value
        else:
            tag = CommonResourceUtils.get_enum_by_int_value(int(tag_value), CommonGameTag, default_value=tag_value)
        cleaned_tag_names.append(tag.name if hasattr(tag, 'name') else str(tag))

    sorted_tag_names = sorted(cleaned_tag_names)
    tags_str = ', '.join(sorted_tag_names)
    output(f'Game Tags: {tags_str}')
    for sorted_tag_name in sorted_tag_names:
        outfit_commands_log.debug(str(sorted_tag_name))
    outfit_commands_log.debug(f'--------------------------------')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.print_outfit_tags_by_cas_part',
    'Print a list of the Game Tags applied to each CAS Part in the outfit of a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('outfit_category', 'Value or Name', 'The Value or Name of the Outfit Category to check.', is_optional=True, default_value='Current Outfit'),
        CommonConsoleCommandArgument('outfit_index', 'Positive Number', 'The index of the outfit to check. This value does nothing if an Outfit Category is not specified.', is_optional=True, default_value=1),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Sim to check.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib_testing.printoutfittagsbycaspart',
    )
)
def _s4clib_testing_print_outfit_tags_by_cas_part(output: CommonConsoleCommandOutput, outfit_category: str = None, outfit_index: int = 1, sim_info: SimInfo = None):
    from sims4communitylib.utils.cas.common_cas_utils import CommonCASUtils
    if sim_info is None:
        return
    outfit_category_and_index = CommonOutfitUtils._parse_outfit_category_and_index_from_str(output, outfit_category=outfit_category, outfit_index=outfit_index, sim_info=sim_info)
    if outfit_category_and_index is None:
        outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)
    output(f'Attempting to print game tags for each CAS Part in outfit ({outfit_category_and_index[0].name}, {outfit_category_and_index[1]}) for Sim {sim_info}.')
    outfit_commands_log.debug(f'Printing all game tags for each CAS Part in outfit ({outfit_category_and_index[0].name}, {outfit_category_and_index[1]}) for Sim {sim_info}.')
    outfit_commands_log.debug(f'-------Game Tags For CAS Parts of Outfit Category:  ({outfit_category_and_index[0].name}, {outfit_category_and_index[1]})-------')
    tags_by_cas_part_id = CommonOutfitUtils.get_outfit_tags_by_cas_part_id(sim_info, outfit_category_and_index=outfit_category_and_index)
    for (cas_part_id, tag_values) in tags_by_cas_part_id.items():
        output(f'CAS Part Id: {cas_part_id}')
        body_type_val = int(CommonCASUtils.get_body_type_cas_part_is_attached_to(sim_info, cas_part_id))
        body_type = CommonResourceUtils.get_enum_by_int_value(body_type_val, BodyType, default_value=None)
        if body_type is None:
            body_type = str(body_type_val)
        body_type_str = body_type.name if hasattr(body_type, 'name') else str(body_type)
        output(f'Body Type: {body_type_str}')
        cleaned_tag_names = list()
        for tag_value in tag_values:
            if isinstance(tag_value, CommonGameTag):
                tag = tag_value
            else:
                tag = CommonResourceUtils.get_enum_by_int_value(int(tag_value), CommonGameTag, default_value=None)
                if tag is None:
                    tag = str(tag_value)
            cleaned_tag_names.append(tag.name if hasattr(tag, 'name') else str(tag))
        sorted_tag_names = sorted(cleaned_tag_names)
        tags_str = ', '.join(sorted_tag_names)
        output(f'Game Tags: {tags_str}')
        outfit_commands_log.debug(
            f'---ID: {cas_part_id} (BodyType: {body_type_str})---')
        for sorted_tag_name in sorted_tag_names:
            outfit_commands_log.debug(str(sorted_tag_name))
        outfit_commands_log.debug(f'---------')

    outfit_commands_log.debug(f'--------------------------------')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.print_previous_outfit',
    'Print information about the previous outfit a Sim was wearing.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Sim to check.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.printpreviousoutfit',
    )
)
def _s4clib_print_previous_outfit(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    if sim_info is None:
        output('ERROR: Failed, no Sim was specified or the specified Sim was not found!')
        return
    previous_outfit = CommonOutfitUtils.get_previous_outfit(sim_info, default_outfit_category_and_index=tuple())
    if not previous_outfit:
        output(f'FAILED: No information about the previous outfit was found for {sim_info}')
        return
    output(f'Previous Outfit Info for {sim_info}')
    outfit_commands_log.debug(f'Previous Outfit Info for {sim_info}')
    CommonOutfitUtils._print_outfit(sim_info, previous_outfit[0], previous_outfit[1], output)


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.print_outfit',
    'Print information about an outfit a Sim has.',
    command_arguments=(
        CommonConsoleCommandArgument('outfit_category', 'Value or Name', 'The Value or Name of the Outfit Category to check.', is_optional=True, default_value='Current Outfit'),
        CommonConsoleCommandArgument('outfit_index', 'Positive Number', 'The index of the outfit to check. This value does nothing if an Outfit Category is not specified.', is_optional=True, default_value=1),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Sim to check.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.printoutfit',
    )
)
def _s4clib_print_outfit(output: CommonConsoleCommandOutput, outfit_category: str = None, outfit_index: int = 1, sim_info: SimInfo = None):
    if sim_info is None:
        output('Failed, no Sim was specified or the specified Sim was not found!')
        return
    outfit_category_and_index = CommonOutfitUtils._parse_outfit_category_and_index_from_str(output, outfit_category, outfit_index=outfit_index, sim_info=sim_info)
    if outfit_category_and_index is None:
        outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)
    CommonOutfitUtils._print_outfit(sim_info, outfit_category_and_index[0], outfit_category_and_index[1], output)


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.print_outfits',
    'Print information about all outfits of a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('show_missing_outfit_info', 'True or False', 'If True, information about the outfits a Sim does not have will be displayed.', is_optional=True, default_value=False),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Sim to print the outfits of.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.printoutfits',
    )
)
def _s4clib_print_outfits(output: CommonConsoleCommandOutput, show_missing_outfit_info: bool = False, sim_info: SimInfo = None):
    if sim_info is None:
        output('ERROR: no Sim was specified or the specified Sim was not found!')
        return
    current_outfit = CommonOutfitUtils.get_current_outfit(sim_info)
    current_outfit_category = current_outfit[0]
    if not isinstance(current_outfit_category, OutfitCategory):
        # noinspection PyBroadException
        try:
            current_outfit_category = CommonResourceUtils.get_enum_by_int_value(int(current_outfit_category), OutfitCategory, default_value=current_outfit_category)
        except:
            output(f'ERROR: Failed to parse {current_outfit_category} as Outfit Category.')
            return

    # noinspection PyBroadException
    if hasattr(current_outfit_category, 'name'):
        current_outfit_category_name = current_outfit_category.name
    else:
        current_outfit_category_name = current_outfit_category

    output(f'Outfit Info for {sim_info}, Current Outfit: ({current_outfit_category_name}, {current_outfit[1]})')
    outfit_commands_log.debug(f'Outfit Info for {sim_info}, Current Outfit: ({current_outfit_category_name}, {current_outfit[1]})')
    output('------')
    outfit_commands_log.debug('------')
    for outfit_category in CommonOutfitUtils.get_all_outfit_categories():
        # noinspection PyBroadException
        try:
            outfit_category_name = outfit_category.name
        except:
            outfit_category_name = outfit_category

        for outfit_index in range(CommonOutfitUtils.get_maximum_number_of_outfits_for_category(outfit_category)):
            if not CommonOutfitUtils.has_outfit(sim_info, (outfit_category, outfit_index)):
                if show_missing_outfit_info:
                    output(f'MISSING: Sim {sim_info} did not have outfit ({outfit_category_name}, {outfit_index})')
                    outfit_commands_log.debug(f'MISSING: Sim {sim_info} did not have outfit ({outfit_category_name}, {outfit_index})')
                continue
            CommonOutfitUtils._print_outfit(sim_info, outfit_category, outfit_index, output)


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.generate_outfit',
    'Generate an outfit for a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('outfit_category', 'Value or Name', 'The Value or Name of the Outfit Category to generate.'),
        CommonConsoleCommandArgument('outfit_index', 'Positive Number', 'The index of the outfit to generate.'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Sim to generate an outfit for.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.generateoutfit',
    )
)
def _s4clib_generate_outfit(output: CommonConsoleCommandOutput, outfit_category: str = None, outfit_index_val: int = 1, sim_info: SimInfo = None):
    outfit_category_and_index = CommonOutfitUtils._parse_outfit_category_and_index_from_str(output, outfit_category, outfit_index_val, sim_info=sim_info, check_for_missing_outfit=False, outfit_category_required=True)
    if outfit_category_and_index is None:
        return
    if sim_info is None:
        output('ERROR: No Sim was specified or the specified Sim was not found!')
        return
    outfit_category_value = outfit_category_and_index[0]
    outfit_category_name = outfit_category_value.name
    outfit_index = outfit_category_and_index[1]
    output(f'Attempting to generate outfit ({outfit_category_name}, {outfit_index}) for Sim {sim_info}')
    if CommonOutfitUtils.has_outfit(sim_info, (outfit_category_value, outfit_index)):
        output(f'FAILED: Sim {sim_info} already has an outfit ({outfit_category_name}, {outfit_index})')
        return
    generated = CommonOutfitUtils.generate_outfit(sim_info, (outfit_category_value, outfit_index))
    if generated:
        output(f'SUCCESS: Outfit ({outfit_category_name}, {outfit_index}) has been successfully generated for Sim {sim_info}.')
    else:
        output(f'FAILED: Outfit ({outfit_category_name}, {outfit_index}) failed to generate for Sim {sim_info}.')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.regenerate_outfit',
    'Regenerate an outfit of a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('outfit_category', 'Value or Name', 'The Value or Name of the Outfit Category to regenerate.', is_optional=True, default_value='Current Outfit'),
        CommonConsoleCommandArgument('outfit_index', 'Positive Number', 'The index of the outfit to regenerate. This value does nothing if an Outfit Category is not specified.', is_optional=True, default_value=1),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Sim to regenerate the outfit of.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.regenerateoutfit',
    )
)
def _common_regenerate_outfit(output: CommonConsoleCommandOutput, outfit_category: str = None, outfit_index: int = 1, sim_info: SimInfo = None):
    outfit_category_and_index = CommonOutfitUtils._parse_outfit_category_and_index_from_str(output, outfit_category, outfit_index, sim_info=sim_info)
    if outfit_category_and_index is None:
        return
    if sim_info is None:
        output('ERROR: No Sim was specified or the specified Sim was not found!')
        return
    output(f'Attempting to regenerate the current outfit of {sim_info}')
    CommonOutfitUtils.regenerate_outfit(sim_info, outfit_category_and_index)
    output(f'Done regenerating the current outfit of {sim_info}')


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.regenerate_all_outfits',
    'Regenerate all outfits of a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The Sim to regenerate the outfit of.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.regeneratealloutfits',
    )
)
def _common_regenerate_all_outfits(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    if sim_info is None:
        output('ERROR: No Sim was specified or the specified Sim was not found!')
        return
    output(f'Attempting to regenerate all outfits for {sim_info}')
    CommonOutfitUtils.regenerate_all_outfits(sim_info)
    output(f'Done regenerating all outfits for {sim_info}.')
