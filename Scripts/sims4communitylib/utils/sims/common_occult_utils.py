"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Iterator, Tuple, Union

from sims.occult.occult_enums import OccultType
from sims.sim_info import SimInfo
from sims.sim_info_base_wrapper import SimInfoBaseWrapper
from sims4communitylib.enums.common_occult_type import CommonOccultType
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.sims.common_sim_loot_action_utils import CommonSimLootActionUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
try:
    from traits.trait_type import TraitType
except ModuleNotFoundError:
    from traits.traits import TraitType


class CommonOccultUtils:
    """Utilities for manipulating the Occults of Sims.

    """
    @staticmethod
    def get_all_occult_types_for_sim_gen(sim_info: SimInfo) -> Iterator[OccultType]:
        """get_all_occult_types_for_sim_gen(sim_info)

        Retrieve a generator of OccultType for all Occults of a Sim.

        .. note:: Results include the occult type of the sim_info specified.\
            If they are Human by default, the Human occult type will be included.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :return: An iterable of OccultType for all occults of the Sim. (Results will not include Occult Types not within the OccultTypes enum, such as Skeleton, Robot, and Ghost! Use :class:`.CommonSimOccultTypeUtils` for more accurate results.)
        :rtype: Iterator[OccultType]
        """
        if sim_info is None:
            return tuple()
        yield OccultType.HUMAN
        sim_occult_types = CommonOccultUtils._get_occult_types(sim_info)
        for occult_type in OccultType.values:
            if occult_type == OccultType.HUMAN:
                continue
            if sim_occult_types & occult_type:
                yield occult_type

    @staticmethod
    def get_sim_info_for_all_occults_gen(sim_info: SimInfo, exclude_occult_types: Iterator[OccultType]) -> Iterator[SimInfo]:
        """get_sim_info_for_all_occults_gen(sim_info, exclude_occult_types)

        Retrieve a generator of SimInfo objects for all Occults of a sim.

        .. note:: Results include the occult type of the sim_info specified.\
            If they are Human by default, the Human occult Sim info will be included.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :param exclude_occult_types: A collection of OccultTypes to exclude from the resulting SimInfo list.
        :type exclude_occult_types: Iterator[OccultType]
        :return: An iterable of Sims for all occult types of the Sim.
        :rtype: Iterator[SimInfo]
        """
        if sim_info is None:
            return tuple()
        exclude_occult_types: Tuple[OccultType] = tuple(exclude_occult_types)
        yield sim_info
        current_occult_type = CommonOccultUtils.get_current_occult_type(sim_info)
        for occult_type in OccultType.values:
            if occult_type in exclude_occult_types:
                continue
            if occult_type == current_occult_type:
                continue
            occult_sim_info: SimInfo = CommonOccultUtils.get_occult_sim_info(sim_info, occult_type)
            if occult_sim_info is None:
                continue
            yield occult_sim_info

    @staticmethod
    def has_any_occult(sim_info: SimInfo) -> bool:
        """has_any_occult(sim_info)

        Determine if a Sim has any Occult Types.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :return: True, if the specified Sim has any Non-Human Occult Types. False, if not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_occult_type_utils import CommonSimOccultTypeUtils
        occult_type = CommonSimOccultTypeUtils.determine_occult_type(sim_info)
        return occult_type not in (CommonOccultType.NON_OCCULT, CommonOccultType.NONE)

    @staticmethod
    def has_occult_type(sim_info: SimInfo, occult_type: OccultType) -> bool:
        """has_occult_type(sim_info, occult_type)

        Determine if a Sim has an Occult Type.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param occult_type: The Occult Type to check.
        :type occult_type: OccultType
        :return: True, if the Sim has the specified Occult Type. False, if not.
        :rtype: bool
        """
        return bool(CommonOccultUtils._get_occult_types(sim_info) & occult_type)

    @staticmethod
    def has_occult_sim_info(sim_info: SimInfo, occult_type: OccultType) -> bool:
        """has_occult_sim_info(sim_info, occult_type)

        Determine if a Sim has a SimInfo for an Occult.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :param occult_type: The Occult Type to check.
        :type occult_type: OccultType
        :return: True, if a SimInfo is available for the specified Occult for the Sim. False, if not.
        :rtype: bool
        """
        if not hasattr(sim_info, 'occult_tracker') or sim_info.occult_tracker is None:
            return False
        return sim_info.occult_tracker.has_occult_type(occult_type)

    @staticmethod
    def get_current_occult_sim_info(sim_info: SimInfo) -> Union[SimInfo, SimInfoBaseWrapper, None]:
        """get_current_occult_sim_info(sim_info)

        Retrieve the SimInfo for the Occult the Sim is currently.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :return: The SimInfo of the Sim or the SimInfoBaseWrapper for the Occult they are (If they are currently an occult).
        :rtype: Union[SimInfo, SimInfoBaseWrapper, None]
        """
        current_occult_type = CommonOccultUtils.get_current_occult_type(sim_info)
        return CommonOccultUtils.get_occult_sim_info(sim_info, current_occult_type)

    @staticmethod
    def get_occult_sim_info(sim_info: SimInfo, occult_type: OccultType) -> Union[SimInfo, SimInfoBaseWrapper, None]:
        """get_occult_sim_info(sim_info, occult_type)

        Retrieve the SimInfo for an Occult of a Sim.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :param occult_type: The Occult Type to retrieve the SimInfo of.
        :type occult_type: OccultType
        :return: The SimInfo of the Sim or the SimInfoBaseWrapper for the specified Occult or the original Sim Info, if the Sim did not have the occult type.
        :rtype: Union[SimInfo, SimInfoBaseWrapper, None]
        """
        if not hasattr(sim_info, 'occult_tracker') or sim_info.occult_tracker is None:
            return None
        occult_sim_info = sim_info.occult_tracker.get_occult_sim_info(occult_type)
        return occult_sim_info

    @staticmethod
    def add_occult(sim_info: SimInfo, occult_type: CommonOccultType) -> bool:
        """add_occult(sim_info, occult_type)

        Add an Occult Type to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param occult_type: The occult type to add.
        :type occult_type: CommonOccultType
        :return: True, if the specified Occult Type has been added to the Sim. False, if not.
        :rtype: bool
        """
        occult_type_add_mappings = {
            CommonOccultType.ALIEN: CommonOccultUtils.add_alien_occult,
            CommonOccultType.MERMAID: CommonOccultUtils.add_mermaid_occult,
            CommonOccultType.ROBOT: CommonOccultUtils.add_robot_occult,
            CommonOccultType.SKELETON: CommonOccultUtils.add_skeleton_occult,
            CommonOccultType.VAMPIRE: CommonOccultUtils.add_vampire_occult,
            CommonOccultType.WITCH: CommonOccultUtils.add_witch_occult
        }
        if occult_type not in occult_type_add_mappings:
            return False
        return occult_type_add_mappings[occult_type](sim_info)

    @staticmethod
    def remove_occult(sim_info: SimInfo, occult_type: CommonOccultType) -> bool:
        """remove_occult(sim_info, occult_type)

        Remove an Occult Type from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param occult_type: The occult type to remove.
        :type occult_type: CommonOccultType
        :return: True, if the specified Occult Type has been removed from the Sim. False, if not.
        :rtype: bool
        """
        occult_type_remove_mappings = {
            CommonOccultType.ALIEN: CommonOccultUtils.remove_alien_occult,
            CommonOccultType.MERMAID: CommonOccultUtils.remove_mermaid_occult,
            CommonOccultType.ROBOT: CommonOccultUtils.remove_robot_occult,
            CommonOccultType.SKELETON: CommonOccultUtils.remove_skeleton_occult,
            CommonOccultType.VAMPIRE: CommonOccultUtils.remove_vampire_occult,
            CommonOccultType.WITCH: CommonOccultUtils.remove_witch_occult
        }
        if occult_type not in occult_type_remove_mappings:
            return False
        return occult_type_remove_mappings[occult_type](sim_info)

    @staticmethod
    def add_alien_occult(sim_info: SimInfo) -> bool:
        """add_alien_occult(sim_info)

        Add the Alien Occult Type to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has successfully become an Alien. False, if not.
        :rtype: bool
        """
        if CommonOccultUtils.is_alien(sim_info):
            return True
        loot_action_ids: Tuple[int] = (
            # loot_Occult_AlienAdd
            103256,
            # loot_Occult_AlienSwitch
            103254
        )
        # noinspection PyPropertyAccess
        physique = sim_info.physique
        # noinspection PyPropertyAccess
        facial_attributes = sim_info.facial_attributes
        # noinspection PyPropertyAccess
        voice_pitch = sim_info.voice_pitch
        # noinspection PyPropertyAccess
        voice_actor = sim_info.voice_actor
        # noinspection PyPropertyAccess
        voice_effect = sim_info.voice_effect
        # noinspection PyPropertyAccess
        skin_tone = sim_info.skin_tone
        flags = sim_info.flags
        pelt_layers = None
        if hasattr(sim_info, 'pelt_layers'):
            # noinspection PyPropertyAccess
            pelt_layers = sim_info.pelt_layers
        base_trait_ids = None
        if hasattr(sim_info, 'base_trait_ids'):
            base_trait_ids = list(sim_info.base_trait_ids)
        # noinspection PyPropertyAccess
        genetic_data_b = sim_info.genetic_data
        if hasattr(genetic_data_b, 'SerializeToString'):
            genetic_data_b = genetic_data_b.SerializeToString()
        result = CommonSimLootActionUtils.apply_loot_actions_by_ids_to_sim(loot_action_ids, sim_info)
        human_sim_info = sim_info.occult_tracker.get_occult_sim_info(OccultType.HUMAN)
        human_sim_info.physique = physique
        human_sim_info.facial_attributes = facial_attributes
        human_sim_info.voice_pitch = voice_pitch
        human_sim_info.voice_actor = voice_actor
        human_sim_info.voice_effect = voice_effect
        human_sim_info.skin_tone = skin_tone
        human_sim_info.flags = flags
        if pelt_layers is not None:
            human_sim_info.pelt_layers = pelt_layers
        if base_trait_ids is not None:
            human_sim_info.base_trait_ids = list(base_trait_ids)
        if hasattr(human_sim_info.genetic_data, 'MergeFromString'):
            human_sim_info.genetic_data.MergeFromString(genetic_data_b)
        else:
            human_sim_info.genetic_data = genetic_data_b
        return result

    @staticmethod
    def remove_alien_occult(sim_info: SimInfo) -> bool:
        """remove_alien_occult(sim_info)

        Remove the Alien Occult Type from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Alien Occult Type has been successfully removed from the specified Sim. False, if not.
        :rtype: bool
        """
        if not CommonOccultUtils.is_alien(sim_info):
            return True
        CommonOccultUtils.switch_to_occult_form(sim_info, OccultType.HUMAN)
        sim_info.occult_tracker.remove_occult_type(OccultType.ALIEN)
        return True

    @staticmethod
    def add_mermaid_occult(sim_info: SimInfo) -> bool:
        """add_mermaid_occult(sim_info)

        Add the Mermaid Occult Type to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has successfully become a Mermaid. False, if not.
        :rtype: bool
        """
        if CommonOccultUtils.is_mermaid(sim_info):
            return True
        # loot_Mermaid_DebugAdd
        add_loot_action_id = 205399
        result = CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(add_loot_action_id, sim_info)
        return result

    @staticmethod
    def remove_mermaid_occult(sim_info: SimInfo) -> bool:
        """remove_mermaid_occult(sim_info)

        Remove the Mermaid Occult Type from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Mermaid Occult Type has been successfully removed from the specified Sim. False, if not.
        :rtype: bool
        """
        if not CommonOccultUtils.is_mermaid(sim_info):
            return True
        trait_ids: Tuple[int] = (
            CommonTraitId.OCCULT_MERMAID_MERMAID_FORM,
            CommonTraitId.OCCULT_MERMAID_DISCOVERED,
            CommonTraitId.OCCULT_MERMAID_TEMPORARY_DISCOVERED,
            CommonTraitId.OCCULT_MERMAID_TYAE,
            CommonTraitId.OCCULT_MERMAID,
        )
        CommonOccultUtils.switch_to_occult_form(sim_info, OccultType.HUMAN)
        return CommonTraitUtils.remove_trait(sim_info, *trait_ids)

    @staticmethod
    def add_robot_occult(sim_info: SimInfo) -> bool:
        """add_robot_occult(sim_info)

        Add the Robot Occult Type to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has successfully become a Robot. False, if not.
        :rtype: bool
        """
        if CommonOccultUtils.is_robot(sim_info):
            return True
        return CommonTraitUtils.add_trait(sim_info, CommonTraitId.OCCULT_ROBOT)

    @staticmethod
    def remove_robot_occult(sim_info: SimInfo) -> bool:
        """remove_robot_occult(sim_info)

        Remove the Robot Occult Type from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Robot Occult Type has been successfully removed from the specified Sim. False, if not.
        :rtype: bool
        """
        if not CommonOccultUtils.is_robot(sim_info):
            return True
        return CommonTraitUtils.remove_trait(sim_info, CommonTraitId.OCCULT_ROBOT)

    @staticmethod
    def add_skeleton_occult(sim_info: SimInfo) -> bool:
        """add_skeleton_occult(sim_info)

        Add the Skeleton Occult Type to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has successfully become a Skeleton. False, if not.
        :rtype: bool
        """
        if CommonOccultUtils.is_skeleton(sim_info):
            return True
        # loot_Skeleton_Add
        add_loot_id = 175969
        return CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(add_loot_id, sim_info)

    @staticmethod
    def remove_skeleton_occult(sim_info: SimInfo) -> bool:
        """remove_skeleton_occult(sim_info)

        Remove the Skeleton Occult Type from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Skeleton Occult Type has been successfully removed from the specified Sim. False, if not.
        :rtype: bool
        """
        if not CommonOccultUtils.is_skeleton(sim_info):
            return True
        # loot_Skeleton_Remove
        remove_loot_id = 175975
        return CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(remove_loot_id, sim_info)

    @staticmethod
    def add_vampire_occult(sim_info: SimInfo) -> bool:
        """add_vampire_occult(sim_info)

        Add the Vampire Occult Type to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has successfully become a Vampire. False, if not.
        :rtype: bool
        """
        if CommonOccultUtils.is_vampire(sim_info):
            return True
        # loot_VampireCreation_NewVampire
        add_loot_id = 149538
        return CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(add_loot_id, sim_info)

    @staticmethod
    def remove_vampire_occult(sim_info: SimInfo) -> bool:
        """remove_vampire_occult(sim_info)

        Remove the Vampire Occult Type from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Vampire Occult Type has been successfully removed from the specified Sim. False, if not.
        :rtype: bool
        """
        if not CommonOccultUtils.is_vampire(sim_info):
            return True
        loot_action_ids: Tuple[int] = (
            # loot_VampireCure_RemoveVampirism
            150170,
            # loot_Life_ResetProgress
            31238
        )
        return CommonSimLootActionUtils.apply_loot_actions_by_ids_to_sim(loot_action_ids, sim_info)

    @staticmethod
    def add_witch_occult(sim_info: SimInfo) -> bool:
        """add_witch_occult(sim_info)

        Add the Witch Occult Type to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has successfully become a Witch. False, if not.
        :rtype: bool
        """
        if CommonOccultUtils.is_witch(sim_info):
            return True
        # loot_WitchOccult_AddOccult
        add_loot_id = 215080
        return CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(add_loot_id, sim_info)

    @staticmethod
    def remove_witch_occult(sim_info: SimInfo) -> bool:
        """remove_witch_occult(sim_info)

        Remove the Witch Occult Type from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Witch Occult Type has been successfully removed from the specified Sim. False, if not.
        :rtype: bool
        """
        if not CommonOccultUtils.is_witch(sim_info):
            return True
        # loot_WitchOccult_RemoveOccult
        remove_loot_id = 215274
        return CommonSimLootActionUtils.apply_loot_actions_by_id_to_duo_sims(remove_loot_id, sim_info, sim_info)

    @staticmethod
    def add_all_occults(sim_info: SimInfo) -> bool:
        """add_all_occults(sim_info)

        Add all Occult Types to a Sim. i.e. Make them a Alien, Vampire, Witch, etc.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if all Occult Types were successfully added to the specified Sim. False, if not.
        :rtype: bool
        """
        CommonOccultUtils.switch_to_occult_form(sim_info, OccultType.HUMAN)
        CommonOccultUtils.add_alien_occult(sim_info)
        CommonOccultUtils.add_mermaid_occult(sim_info)
        CommonOccultUtils.add_robot_occult(sim_info)
        CommonOccultUtils.add_skeleton_occult(sim_info)
        CommonOccultUtils.add_vampire_occult(sim_info)
        CommonOccultUtils.add_witch_occult(sim_info)
        return True

    @staticmethod
    def remove_all_occults(sim_info: SimInfo) -> bool:
        """remove_all_occults(sim_info)

        Remove all Occult Types from a Sim. i.e. Make them a Non-Occult only.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if all Occult Types were successfully removed from the specified Sim. False, if not.
        :rtype: bool
        """
        CommonOccultUtils.switch_to_occult_form(sim_info, OccultType.HUMAN)
        CommonOccultUtils.remove_alien_occult(sim_info)
        CommonOccultUtils.remove_mermaid_occult(sim_info)
        CommonOccultUtils.remove_robot_occult(sim_info)
        CommonOccultUtils.remove_skeleton_occult(sim_info)
        CommonOccultUtils.remove_vampire_occult(sim_info)
        CommonOccultUtils.remove_witch_occult(sim_info)
        return True

    @staticmethod
    def switch_to_occult_form(sim_info: SimInfo, occult_type: Union[OccultType, CommonOccultType]) -> bool:
        """switch_to_occult_form(sim_info, occult_type)

        Switch a Sim to an Occult Form.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param occult_type: The type of Occult to switch to.
        :type occult_type: Union[OccultType, CommonOccultType]
        :return: True, if the Sim successfully switched to the specified Occult Type. False, if the Sim failed to switch to the specified Occult Type or if they do not have that Occult Type to switch to.
        :rtype: bool
        """
        if isinstance(occult_type, CommonOccultType):
            occult_type = CommonOccultType.convert_to_vanilla(occult_type)
            if occult_type is None:
                return False
        sim_info.occult_tracker.switch_to_occult_type(occult_type)
        return True

    @staticmethod
    def is_vampire(sim_info: SimInfo) -> bool:
        """is_vampire(sim_info)

        Determine if a Sim is a Vampire.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Vampire. False, if not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.OCCULT_VAMPIRE) or CommonOccultUtils.has_occult_type(sim_info, OccultType.VAMPIRE)

    @staticmethod
    def is_alien(sim_info: SimInfo) -> bool:
        """is_alien(sim_info)

        Determine if a Sim is an Alien.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is an Alien. False, if not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.OCCULT_ALIEN) or CommonOccultUtils.has_occult_type(sim_info, OccultType.ALIEN)

    @staticmethod
    def is_plant_sim(sim_info: SimInfo) -> bool:
        """is_plant_sim(sim_info)

        Determine if a Sim is a Plant Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Plant Sim. False, if not.
        :rtype: bool
        """
        return CommonTraitUtils.has_trait(sim_info, CommonTraitId.PLANT_SIM)

    @staticmethod
    def is_ghost(sim_info: SimInfo) -> bool:
        """is_ghost(sim_info)

        Determine if a Sim is a Ghost.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Ghost. False, if not.
        :rtype: bool
        """
        equipped_sim_traits = CommonTraitUtils.get_equipped_traits(sim_info)
        for trait in equipped_sim_traits:
            is_ghost_trait = getattr(trait, 'is_ghost_trait', None)
            if is_ghost_trait:
                return True
        return False

    @staticmethod
    def is_robot(sim_info: SimInfo) -> bool:
        """is_robot(sim_info)

        Determine if a Sim is a Robot.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Robot. False, if not.
        :rtype: bool
        """
        if not hasattr(TraitType, 'ROBOT'):
            return False
        equipped_sim_traits = CommonTraitUtils.get_equipped_traits(sim_info)
        for trait in equipped_sim_traits:
            trait_type = getattr(trait, 'trait_type', -1)
            if trait_type == TraitType.ROBOT:
                return True
        return False
    
    @staticmethod
    def is_skeleton(sim_info: SimInfo) -> bool:
        """is_skeleton(sim_info)

        Determine if a Sim is a Skeleton.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is the a Skeleton. False, if not.
        :rtype: bool
        """
        equipped_sim_traits = CommonTraitUtils.get_equipped_traits(sim_info)
        skeleton_trait_ids = {
            CommonTraitId.HIDDEN_SKELETON,
            CommonTraitId.HIDDEN_SKELETON_SERVICE_SKELETON,
            CommonTraitId.HIDDEN_SKELETON_TEMPLE_SKELETON
        }
        for trait in equipped_sim_traits:
            trait_id = CommonTraitUtils.get_trait_id(trait)
            if trait_id in skeleton_trait_ids:
                return True
        return False

    @staticmethod
    def is_witch(sim_info: SimInfo) -> bool:
        """is_witch(sim_info)

        Determine if a Sim is a Witch

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Witch. False, if not.
        :rtype: bool
        """
        if sim_info is None or not hasattr(OccultType, 'WITCH'):
            return False
        return CommonOccultUtils._has_occult_trait(sim_info, CommonTraitId.OCCULT_WITCH) or CommonOccultUtils.has_occult_type(sim_info, OccultType.WITCH)

    @staticmethod
    def is_mermaid(sim_info: SimInfo) -> bool:
        """is_mermaid(sim_info)

        Determine if a Sim is a Mermaid

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Mermaid. False, if not.
        :rtype: bool
        """
        if sim_info is None or not hasattr(OccultType, 'MERMAID'):
            return False
        return CommonOccultUtils._has_occult_trait(sim_info, CommonTraitId.OCCULT_MERMAID) or CommonOccultUtils.has_occult_type(sim_info, OccultType.MERMAID)

    @staticmethod
    def is_in_mermaid_form(sim_info: SimInfo) -> bool:
        """is_in_mermaid_form(sim_info)

        Determine if a Sim is in Mermaid Form (The Sim has a visible Tail).

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has their Mermaid tail out. False, if not.
        :rtype: bool
        """
        if sim_info is None or not hasattr(OccultType, 'MERMAID'):
            return False
        return CommonOccultUtils.get_current_occult_type(sim_info) == OccultType.MERMAID

    @staticmethod
    def is_mermaid_in_mermaid_form(sim_info: SimInfo) -> bool:
        """is_mermaid_in_mermaid_form(sim_info)

        Determine if a Sim is a Mermaid and is in Mermaid Form (Their Tail is visible).

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is a Mermaid with their tail out. False, if not.
        :rtype: bool
        """
        return CommonOccultUtils.is_mermaid(sim_info) and CommonOccultUtils.is_in_mermaid_form(sim_info)

    @staticmethod
    def is_currently_human(sim_info: SimInfo) -> bool:
        """is_currently_human(sim_info)

        Determine if a Sim is currently in their Human form (regardless of their Occult type).

        .. note:: The Human Occult is not the same as the Human Species! This means that Pets can have a "Human" Occult as their Non-Occult.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently a Human. False, if not.
        :rtype: bool
        """
        return CommonOccultUtils.is_currently_a_non_occult(sim_info)

    @staticmethod
    def is_currently_a_non_occult(sim_info: SimInfo) -> bool:
        """is_currently_a_non_occult(sim_info)

        Determine if a Sim is currently in a Non-Occult form (regardless of their Occult type).

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently in their Non-Occult form. False, if not.
        :rtype: bool
        """
        if sim_info is None or not hasattr(OccultType, 'HUMAN'):
            return False
        current_occult = CommonOccultUtils.get_current_occult_type(sim_info)
        return current_occult == OccultType.HUMAN

    @staticmethod
    def is_currently_a_mermaid(sim_info: SimInfo) -> bool:
        """is_currently_a_mermaid(sim_info)

        Determine if a Sim is currently in a Mermaid form. (Not disguised)

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently in their Mermaid form. False, if not.
        :rtype: bool
        """
        return CommonOccultUtils.is_in_mermaid_form(sim_info)

    @staticmethod
    def is_currently_a_robot(sim_info: SimInfo) -> bool:
        """is_currently_a_robot(sim_info)

        Determine if a Sim is currently in their Robot form.

        .. note:: In base game, if a Sim is a Robot then they are automatically in their Robot Form, since Robots do not have an alternative form.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently in their Robot form. False, if not.
        :rtype: bool
        """
        return CommonOccultUtils.is_robot(sim_info)

    @staticmethod
    def is_currently_a_skeleton(sim_info: SimInfo) -> bool:
        """is_currently_a_skeleton(sim_info)

        Determine if a Sim is currently in their Skeleton form.

        .. note:: In base game, if a Sim is a Skeleton then they are automatically in their Skeleton Form, since Skeletons do not have an alternative form.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently in their Skeleton form. False, if not.
        :rtype: bool
        """
        return CommonOccultUtils.is_skeleton(sim_info)

    @staticmethod
    def is_currently_a_plant_sim(sim_info: SimInfo) -> bool:
        """is_currently_a_plant_sim(sim_info)

        Determine if a Sim is currently in their Plant Sim form.

        .. note:: In base game, if a Sim is a Plant Sim then they are automatically in their Plant Sim Form, since Plant Sims do not have an alternative form.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently in their Plant Sim form. False, if not.
        :rtype: bool
        """
        return CommonOccultUtils.is_plant_sim(sim_info)

    @staticmethod
    def is_currently_a_ghost(sim_info: SimInfo) -> bool:
        """is_currently_a_ghost(sim_info)

        Determine if a Sim is currently in their Ghost form.

        .. note:: In base game, if a Sim is a Ghost then they are automatically in their Ghost Form, since Ghosts do not have an alternative form.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently in their Ghost form. False, if not.
        :rtype: bool
        """
        return CommonOccultUtils.is_ghost(sim_info)

    @staticmethod
    def is_currently_a_vampire(sim_info: SimInfo) -> bool:
        """is_currently_a_vampire(sim_info)

        Determine if a Sim is currently in their Vampire form. (Not disguised)

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently in their Vampire form. False, if not.
        :rtype: bool
        """
        if sim_info is None or not hasattr(OccultType, 'VAMPIRE'):
            return False
        return CommonOccultUtils.get_current_occult_type(sim_info) == OccultType.VAMPIRE

    @staticmethod
    def is_currently_an_alien(sim_info: SimInfo) -> bool:
        """is_currently_an_alien(sim_info)

        Determine if a Sim is currently in their Alien form. (Not disguised)

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently in their Alien form. False, if not.
        :rtype: bool
        """
        if sim_info is None or not hasattr(OccultType, 'ALIEN'):
            return False
        return CommonOccultUtils.get_current_occult_type(sim_info) == OccultType.ALIEN

    @staticmethod
    def is_currently_a_witch(sim_info: SimInfo) -> bool:
        """is_currently_a_witch(sim_info)

        Determine if a Sim is currently in their Witch form. (Not disguised)

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim is currently in their Witch form. False, if not.
        :rtype: bool
        """
        if sim_info is None or not hasattr(OccultType, 'WITCH'):
            return False
        return CommonOccultUtils.get_current_occult_type(sim_info) == OccultType.WITCH

    @staticmethod
    def get_sim_info_of_all_occults_gen(sim_info: SimInfo, *exclude_occult_types: OccultType) -> Iterator[SimInfo]:
        """get_sim_info_of_all_occults_gen(sim_info, *exclude_occult_types)

        Retrieve a generator of SimInfo objects for all Occults of a sim.

        .. warning:: Obsolete, please use :func:`~get_sim_info_for_all_occults_gen` instead.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :param exclude_occult_types: A collection of OccultTypes to exclude from the resulting SimInfo list.
        :type exclude_occult_types: OccultType
        :return: An iterable of Sims for all occult types of the Sim.
        :rtype: Iterator[SimInfo]
        """
        return CommonOccultUtils.get_sim_info_for_all_occults_gen(sim_info, exclude_occult_types)

    @staticmethod
    def _has_occult_trait(sim_info: SimInfo, trait_id: Union[int, CommonTraitId]) -> bool:
        return CommonOccultUtils._has_occult_traits(sim_info, (trait_id,))

    @staticmethod
    def _has_occult_traits(sim_info: SimInfo, trait_ids: Iterator[Union[int, CommonTraitId]]) -> bool:
        if sim_info is None:
            return False
        equipped_traits = CommonTraitUtils.get_equipped_traits(sim_info)
        for equipped_trait in equipped_traits:
            trait_id = CommonTraitUtils.get_trait_id(equipped_trait)
            if trait_id in trait_ids:
                return True
        return False

    @staticmethod
    def get_current_occult_type(sim_info: SimInfo) -> Union[OccultType, None]:
        """get_current_occult_type(sim_info)

        Retrieve the current occult type of the Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The current occult type of the Sim or None if the Sim does not have a current occult type.
        :rtype: Union[OccultType, None]
        """
        if sim_info is None:
            return OccultType.HUMAN
        if not hasattr(sim_info, 'current_occult_types'):
            if not hasattr(sim_info, '_base') or not hasattr(sim_info._base, 'current_occult_types'):
                return None
            return OccultType(sim_info._base.current_occult_types)
        # noinspection PyPropertyAccess
        return OccultType(sim_info.current_occult_types)

    @staticmethod
    def _get_occult_types(sim_info: SimInfo) -> OccultType:
        if not hasattr(sim_info, 'occult_types'):
            if not hasattr(sim_info, '_base') or not hasattr(sim_info._base, 'occult_types'):
                return CommonOccultUtils.get_current_occult_type(sim_info) or OccultType.HUMAN
            return sim_info._base.occult_types
        # noinspection PyPropertyAccess
        return sim_info.occult_types


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.switch_sim_to_occult',
    'Switch a Sim to an Occult form (If they have it)',
    command_arguments=(
        CommonConsoleCommandArgument('occult_type', 'CommonOccultType', f'The name of an Occult Type to switch the form of the Sim to. Valid Values: {CommonOccultType.get_comma_separated_names_string()}'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance Id or name of the Sim that will switch forms.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.switchsimtooccult',
        's4clib.switchoccult',
        's4clib.switch_occult',
        's4clib.switch_occult_type',
        's4clib.switchocculttype'
    )
)
def _common_switch_sim_to_occult(output: CommonConsoleCommandOutput, occult_type: CommonOccultType, sim_info: SimInfo=None):
    if sim_info is None:
        return
    if occult_type is None:
        return
    occult_type_name = occult_type.name
    output(f'Attempting to switch Sim {sim_info} to their {occult_type_name} form.')
    if CommonOccultUtils.switch_to_occult_form(sim_info, occult_type):
        output(f'SUCCESS: Successfully switched Sim {sim_info} to their {occult_type_name} form.')
    else:
        output(f'FAILED: Failed to switch Sim {sim_info} to their {occult_type_name} form.')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.add_occult_to_sim',
    'Add an Occult Type to a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('occult_type', 'CommonOccultType', f'The name of an Occult Type to add to the Sim. Valid Values: {CommonOccultType.get_comma_separated_names_string()}'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance Id or name of the Sim to add the occult to.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.addocculttosim',
        's4clib.add_occult',
        's4clib.addoccult',
        's4clib.add_occult_type',
        's4clib.addocculttype',
    )
)
def _common_add_occult_to_sim(output: CommonConsoleCommandOutput, occult_type: CommonOccultType, sim_info: SimInfo=None):
    if sim_info is None:
        return
    if occult_type is None:
        return
    occult_type_name = occult_type.name
    output(f'Attempting to add occult {occult_type_name} to Sim {sim_info}')
    if CommonOccultUtils.add_occult(sim_info, occult_type):
        output(f'SUCCESS: Successfully added occult {occult_type_name} to Sim {sim_info}.')
    else:
        output(f'FAILED: Failed to add occult {occult_type_name} to Sim {sim_info}.')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.remove_occult_from_sim',
    'Remove an Occult Type from a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('occult_type', 'CommonOccultType', f'The name of an Occult Type to remove from the Sim. Valid Values: {CommonOccultType.get_comma_separated_names_string()}'),
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance Id or name of the Sim to remove the occult from.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.removeoccultfromsim',
        's4clib.remove_occult',
        's4clib.removeoccult',
        's4clib.remove_occult_type',
        's4clib.removeocculttype',
    )
)
def _common_remove_occult_from_sim(output: CommonConsoleCommandOutput, occult_type: CommonOccultType, sim_info: SimInfo=None):
    if sim_info is None:
        return
    if occult_type is None:
        return
    occult_type_name = occult_type.name
    output(f'Attempting to remove occult {occult_type_name} from Sim {sim_info}')
    if CommonOccultUtils.remove_occult(sim_info, occult_type):
        output(f'SUCCESS: Successfully removed occult {occult_type_name} from Sim {sim_info}.')
    else:
        output(f'FAILED: Failed to remove occult {occult_type_name} from Sim {sim_info}.')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.remove_all_occults_from_sim',
    'Remove all Occult Types from a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance Id or name of the Sim to remove the occult types from.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.removealloccultsfromsim',
        's4clib.remove_all_occults',
        's4clib.removealloccults',
        's4clib.remove_all_occult_types',
        's4clib.removeallocculttypes',
    )
)
def _common_remove_all_occults_from_sim(output: CommonConsoleCommandOutput, sim_info: SimInfo=None):
    if sim_info is None:
        return
    output(f'Attempting to remove all occult types from Sim {sim_info}.')
    if CommonOccultUtils.remove_all_occults(sim_info):
        output(f'SUCCESS: Successfully removed all occult types from Sim {sim_info}.')
    else:
        output(f'FAILED: Failed to remove all occult types from Sim {sim_info}.')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.print_vanilla_occults',
    'Print a list of all vanilla OccultType values a Sim has.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance Id or name of the Sim to print the occult types of.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.printvanillaoccults',
    )
)
def _common_print_vanilla_occult_types_for_sim(output: CommonConsoleCommandOutput, sim_info: SimInfo=None):
    if sim_info is None:
        return
    occult_types_str = ', '.join([occult_type.name if hasattr(occult_type, 'name') else str(occult_type) for occult_type in CommonOccultUtils._get_occult_types(sim_info)])
    output(f'Occult Types: {occult_types_str}')
    current_occult_types_str = ', '.join([occult_type.name if hasattr(occult_type, 'name') else str(occult_type) for occult_type in CommonOccultUtils.get_current_occult_type(sim_info)])
    output(f'Current Occult Types: {current_occult_types_str}')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.print_occult_sim_infos',
    'Print information about the Occult Sim Infos of a Sim for each occult type they have.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance Id or name of the Sim to check.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib_testing.printoccultsiminfos',
    )
)
def _common_print_occult_sim_infos(output: CommonConsoleCommandOutput, sim_info: SimInfo=None):
    if sim_info is None:
        return
    output(f'Attempting to print Occult Information for Sim {sim_info}')
    for occult_type in OccultType.values:
        occult_type_name = occult_type.name
        occult_sim_info = CommonOccultUtils.get_occult_sim_info(sim_info, occult_type)
        if occult_sim_info is None:
            output(f'Occult Sim Info[{occult_type_name}]: None')
            continue
        occult_sim_id = CommonSimUtils.get_sim_id(occult_sim_info)
        obj_type_acronym = 'UnknownType'
        if CommonTypeUtils.is_sim_info(occult_sim_info):
            obj_type_acronym = 'SI'
        elif CommonTypeUtils.is_sim_instance(occult_sim_info):
            obj_type_acronym = 'S'
        elif CommonTypeUtils.is_sim_info_base_wrapper(occult_sim_info):
            obj_type_acronym = 'SIBW'
        from sims4communitylib.utils.sims.common_sim_type_utils import CommonSimTypeUtils
        sim_types = tuple(CommonSimTypeUtils.get_all_sim_types_gen(occult_sim_info, combine_teen_young_adult_and_elder_age=False, combine_child_dog_types=False))
        sim_types_str = ', '.join([sim_type.name for sim_type in sim_types])
        current_sim_type = CommonSimTypeUtils.determine_sim_type(occult_sim_info, combine_teen_young_adult_and_elder_age=False, combine_child_dog_types=False, use_current_occult_type=True)
        current_sim_type_name = current_sim_type.name
        output(f'Occult Sim Info [{occult_type_name}]: {occult_sim_info} ({occult_sim_id}, ({sim_types_str}), C:{current_sim_type_name}) [{obj_type_acronym}]')
