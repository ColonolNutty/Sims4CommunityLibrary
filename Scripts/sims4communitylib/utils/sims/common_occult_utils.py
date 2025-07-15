"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import random
from typing import Iterator, Tuple, Union

from cas.cas import OutfitOverrideOptionFlags
from sims.occult.occult_enums import OccultType
from sims.outfits.outfit_enums import BodyType
from sims.sim_info import SimInfo
from sims.sim_info_base_wrapper import SimInfoBaseWrapper
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.dtos.common_cas_part import CommonCASPart
from sims4communitylib.enums.buffs_enum import CommonBuffId
from sims4communitylib.enums.common_bucks_types import CommonBucksType
from sims4communitylib.enums.common_occult_type import CommonOccultType
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.logging._has_s4cl_class_log import _HasS4CLClassLog
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.cas.common_cas_utils import CommonCASUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.sims.common_buff_utils import CommonBuffUtils
from sims4communitylib.utils.sims.common_sim_appearance_modifier_utils import CommonSimAppearanceModifierUtils
from sims4communitylib.utils.sims.common_sim_bucks_utils import CommonSimBucksUtils
from sims4communitylib.utils.sims.common_sim_loot_action_utils import CommonSimLootActionUtils
from sims4communitylib.utils.sims.common_sim_spell_utils import CommonSimSpellUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
try:
    from traits.trait_type import TraitType
except ModuleNotFoundError:
    from traits.traits import TraitType


class CommonOccultUtils(_HasS4CLClassLog):
    """Utilities for manipulating the Occults of Sims.

    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_occult_utils'

    @classmethod
    def get_all_occult_types_for_sim_gen(cls, sim_info: SimInfo) -> Iterator[OccultType]:
        """get_all_occult_types_for_sim_gen(sim_info)

        Retrieve a generator of OccultType for all Occults of a Sim.

        .. note:: Results include the occult type of the sim_info specified.\
            If they are Human by default, the Human occult type will be included.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :return: An iterator of OccultType for all occults of the Sim. (Results will not include Occult Types not within the OccultTypes enum, such as Skeleton, Robot, and Ghost! Use :class:`.CommonSimOccultTypeUtils` for more accurate results.)
        :rtype: Iterator[OccultType]
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        yield OccultType.HUMAN
        sim_occult_types = CommonOccultUtils._get_occult_types(sim_info)
        for occult_type in OccultType.values:
            if occult_type == OccultType.HUMAN:
                continue
            if sim_occult_types & occult_type:
                yield occult_type

    @classmethod
    def get_sim_info_for_all_occults_gen(cls, sim_info: SimInfo, exclude_occult_types: Iterator[OccultType]) -> Iterator[SimInfo]:
        """get_sim_info_for_all_occults_gen(sim_info, exclude_occult_types)

        Retrieve a generator of SimInfo objects for all Occults of a sim.

        .. note:: Results include the occult type of the sim_info specified.\
            If they are Human by default, the Human occult Sim info will be included.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :param exclude_occult_types: A collection of OccultTypes to exclude from the resulting SimInfo list.
        :type exclude_occult_types: Iterator[OccultType]
        :return: An iterator of Sims for all occult types of the Sim.
        :rtype: Iterator[SimInfo]
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
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

    @classmethod
    def has_any_occult(cls, sim_info: SimInfo) -> CommonTestResult:
        """has_any_occult(sim_info)

        Determine if a Sim has any Occult Types.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the specified Sim has any Non-Human Occult Types. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        from sims4communitylib.utils.sims.common_sim_occult_type_utils import CommonSimOccultTypeUtils
        occult_type = CommonSimOccultTypeUtils.determine_occult_type(sim_info)
        if occult_type not in (CommonOccultType.NON_OCCULT, CommonOccultType.NONE):
            return CommonTestResult(True, reason=f'{sim_info} is not an Occult Sim.', tooltip_text=CommonStringId.S4CL_SIM_IS_NOT_AN_OCCULT_SIM, tooltip_tokens=(sim_info,))
        return CommonTestResult(False, reason=f'{sim_info} has occult type. {occult_type}', tooltip_text=CommonStringId.S4CL_SIM_HAS_OCCULT_TYPE, tooltip_tokens=(sim_info, str(occult_type)))

    @classmethod
    def has_occult_type(cls, sim_info: SimInfo, occult_type: OccultType) -> CommonTestResult:
        """has_occult_type(sim_info, occult_type)

        Determine if a Sim has an Occult Type.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param occult_type: The Occult Type to check.
        :type occult_type: OccultType
        :return: The result of testing. True, if the Sim has the specified Occult Type. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        if bool(CommonOccultUtils._get_occult_types(sim_info) & occult_type):
            return CommonTestResult(True, reason=f'{sim_info} has occult type {occult_type}.', tooltip_text=CommonStringId.S4CL_SIM_HAS_OCCULT_TYPE, tooltip_tokens=(sim_info, CommonOccultType.convert_to_localized_string_id(occult_type)))
        return CommonTestResult(False, reason=f'{sim_info} did not have occult type {occult_type}', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_OCCULT_TYPE, tooltip_tokens=(sim_info, CommonOccultType.convert_to_localized_string_id(occult_type)))

    @classmethod
    def has_occult_sim_info(cls, sim_info: SimInfo, occult_type: OccultType) -> CommonTestResult:
        """has_occult_sim_info(sim_info, occult_type)

        Determine if a Sim has a SimInfo for an Occult.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :param occult_type: The Occult Type to check.
        :type occult_type: OccultType
        :return: The result of testing. True, if a SimInfo is available for the specified Occult for the Sim. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            return CommonTestResult(False, reason=f'sim_info was None!', hide_tooltip=True)
        if not hasattr(sim_info, 'occult_tracker') or sim_info.occult_tracker is None:
            return CommonTestResult(False, reason=f'{sim_info} did not have an occult tracker, thus they did not have any occult types.', hide_tooltip=True)
        occult_type = CommonOccultType.convert_to_vanilla(occult_type)
        if sim_info.occult_tracker.has_occult_type(occult_type):
            return CommonTestResult(True, reason=f'{sim_info} has a Sim Info for Occult Type {occult_type}. (Meaning the Occult has an alternative form.)', tooltip_text=CommonStringId.S4CL_SIM_HAS_OCCULT_SIM_INFO_FOR_OCCULT_TYPE, tooltip_tokens=(sim_info, CommonOccultType.convert_to_localized_string_id(occult_type)))
        return CommonTestResult(False, reason=f'{sim_info} did not have a Sim Info Occult Type {occult_type}. (Meaning the Occult likely does not have an alternative form.)', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_OCCULT_SIM_INFO_FOR_OCCULT_TYPE, tooltip_tokens=(sim_info, CommonOccultType.convert_to_localized_string_id(occult_type)))

    @classmethod
    def get_current_occult_sim_info(cls, sim_info: SimInfo) -> Union[SimInfo, SimInfoBaseWrapper, None]:
        """get_current_occult_sim_info(sim_info)

        Retrieve the SimInfo for the Occult the Sim is currently.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :return: The SimInfo of the Sim or the SimInfoBaseWrapper for the Occult they are (If they are currently an occult).
        :rtype: Union[SimInfo, SimInfoBaseWrapper, None]
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        current_occult_type = CommonOccultUtils.get_current_occult_type(sim_info)
        return CommonOccultUtils.get_occult_sim_info(sim_info, current_occult_type)

    @classmethod
    def get_occult_sim_info(cls, sim_info: SimInfo, occult_type: OccultType) -> Union[SimInfo, SimInfoBaseWrapper]:
        """get_occult_sim_info(sim_info, occult_type)

        Retrieve the SimInfo for an Occult of a Sim.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :param occult_type: The Occult Type to retrieve the SimInfo of.
        :type occult_type: OccultType
        :return: The SimInfo of the Sim or the SimInfoBaseWrapper for the specified Occult or the original Sim Info, if the Sim did not have the occult type.
        :rtype: Union[SimInfo, SimInfoBaseWrapper, None]
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        if not hasattr(sim_info, 'occult_tracker') or sim_info.occult_tracker is None:
            return sim_info
        occult_sim_info = sim_info.occult_tracker.get_occult_sim_info(occult_type)
        return occult_sim_info

    @classmethod
    def add_occult(cls, sim_info: SimInfo, occult_type: CommonOccultType) -> CommonExecutionResult:
        """add_occult(sim_info, occult_type)

        Add an Occult Type to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param occult_type: The occult type to add.
        :type occult_type: CommonOccultType
        :return: The result of adding the occult. True, if the specified Occult Type has been added to the Sim. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_occult_available_result = CommonOccultUtils.is_occult_available(occult_type)
        if not is_occult_available_result:
            return is_occult_available_result
        occult_type_add_mappings = {
            CommonOccultType.ALIEN: CommonOccultUtils.add_alien_occult,
            CommonOccultType.FAIRY: CommonOccultUtils.add_fairy_occult,
            CommonOccultType.MERMAID: CommonOccultUtils.add_mermaid_occult,
            CommonOccultType.PLANT_SIM: CommonOccultUtils.add_plant_sim_occult,
            CommonOccultType.ROBOT: CommonOccultUtils.add_robot_occult,
            CommonOccultType.SCARECROW: CommonOccultUtils.add_scarecrow_occult,
            CommonOccultType.SKELETON: CommonOccultUtils.add_skeleton_occult,
            CommonOccultType.VAMPIRE: CommonOccultUtils.add_vampire_occult,
            CommonOccultType.WITCH: CommonOccultUtils.add_witch_occult,
            CommonOccultType.WEREWOLF: CommonOccultUtils.add_werewolf_occult
        }
        if occult_type not in occult_type_add_mappings:
            return CommonExecutionResult(False, reason=f'{occult_type.name} did not have an add function, meaning it has not been implemented yet.', tooltip_text=CommonStringId.S4CL_OCCULT_TYPE_DID_NOT_HAVE_AN_ADD_FUNCTION, tooltip_tokens=(CommonOccultType.convert_to_localized_string_id(occult_type),))
        return occult_type_add_mappings[occult_type](sim_info)

    @classmethod
    def remove_occult(cls, sim_info: SimInfo, occult_type: CommonOccultType) -> CommonExecutionResult:
        """remove_occult(sim_info, occult_type)

        Remove an Occult Type from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param occult_type: The occult type to remove.
        :type occult_type: CommonOccultType
        :return: The result of removing the occult. True, if the specified Occult Type has been removed from the Sim. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_occult_available_result = CommonOccultUtils.is_occult_available(occult_type)
        if not is_occult_available_result:
            return is_occult_available_result.reverse_result()
        occult_type_remove_mappings = {
            CommonOccultType.ALIEN: CommonOccultUtils.remove_alien_occult,
            CommonOccultType.FAIRY: CommonOccultUtils.remove_fairy_occult,
            CommonOccultType.MERMAID: CommonOccultUtils.remove_mermaid_occult,
            CommonOccultType.PLANT_SIM: CommonOccultUtils.remove_plant_sim_occult,
            CommonOccultType.ROBOT: CommonOccultUtils.remove_robot_occult,
            CommonOccultType.SCARECROW: CommonOccultUtils.remove_scarecrow_occult,
            CommonOccultType.SKELETON: CommonOccultUtils.remove_skeleton_occult,
            CommonOccultType.VAMPIRE: CommonOccultUtils.remove_vampire_occult,
            CommonOccultType.WITCH: CommonOccultUtils.remove_witch_occult,
            CommonOccultType.WEREWOLF: CommonOccultUtils.remove_werewolf_occult
        }
        if occult_type not in occult_type_remove_mappings:
            return CommonExecutionResult(False, reason=f'{occult_type.name} did not have a remove function, meaning it has not been implemented yet.', tooltip_text=CommonStringId.S4CL_OCCULT_TYPE_DID_NOT_HAVE_A_REMOVE_FUNCTION, tooltip_tokens=(CommonOccultType.convert_to_localized_string_id(occult_type),))
        return occult_type_remove_mappings[occult_type](sim_info)

    @classmethod
    def add_alien_occult(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """add_alien_occult(sim_info)

        Add the Alien Occult Type to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of adding the Alien occult. True, if the Sim has successfully become an Alien. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_alien_available_result = CommonOccultUtils.is_alien_occult_available()
        if not is_alien_available_result:
            return is_alien_available_result
        is_alien_result = CommonOccultUtils.is_alien(sim_info)
        if is_alien_result:
            return is_alien_result
        loot_action_ids: Tuple[int, ...] = (
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
        if result:
            return CommonExecutionResult.TRUE
        return CommonExecutionResult.FALSE

    @classmethod
    def remove_alien_occult(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """remove_alien_occult(sim_info)

        Remove the Alien Occult Type from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of removing the alien occult. True, if the Alien Occult Type has been successfully removed from the specified Sim. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_alien_available_result = CommonOccultUtils.is_alien_occult_available()
        if not is_alien_available_result:
            return is_alien_available_result.reverse_result()
        is_alien_result = CommonOccultUtils.is_alien(sim_info)
        if not is_alien_result:
            return is_alien_result.reverse_result()
        CommonOccultUtils.switch_to_occult_form(sim_info, OccultType.HUMAN)
        sim_info.occult_tracker.remove_occult_type(OccultType.ALIEN)
        return CommonExecutionResult.TRUE

    @classmethod
    def add_mermaid_occult(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """add_mermaid_occult(sim_info)

        Add the Mermaid Occult Type to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of adding the mermaid occult. True, if the Sim has successfully become a Mermaid. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_mermaid_available_result = CommonOccultUtils.is_mermaid_occult_available()
        if not is_mermaid_available_result:
            return is_mermaid_available_result
        is_mermaid_result = CommonOccultUtils.is_mermaid(sim_info)
        if is_mermaid_result:
            return is_mermaid_result
        # loot_Mermaid_DebugAdd
        add_loot_action_id = 205399
        if CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(add_loot_action_id, sim_info):
            return CommonExecutionResult.TRUE
        return CommonExecutionResult.FALSE

    @classmethod
    def remove_mermaid_occult(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """remove_mermaid_occult(sim_info)

        Remove the Mermaid Occult Type from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of removing the mermaid occult. True, if the Mermaid Occult Type has been successfully removed from the specified Sim. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_mermaid_available_result = CommonOccultUtils.is_mermaid_occult_available()
        if not is_mermaid_available_result:
            return is_mermaid_available_result.reverse_result()
        is_mermaid_result = CommonOccultUtils.is_mermaid(sim_info)
        if not is_mermaid_result:
            return is_mermaid_result.reverse_result()
        traits: Tuple[Union[int, CommonTraitId], ...] = (
            CommonTraitId.OCCULT_MERMAID_MERMAID_FORM,
            CommonTraitId.OCCULT_MERMAID_DISCOVERED,
            CommonTraitId.OCCULT_MERMAID_TEMPORARY_DISCOVERED,
            CommonTraitId.OCCULT_MERMAID_TYAE,
            CommonTraitId.OCCULT_MERMAID,
        )
        CommonOccultUtils.switch_to_occult_form(sim_info, OccultType.HUMAN)
        return CommonTraitUtils.remove_traits(sim_info, traits)

    @classmethod
    def add_fairy_occult(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """add_fairy_occult(sim_info)

        Add the Fairy Occult Type to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of adding the Fairy occult. True, if the Sim has successfully become a Fairy. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_fairy_available_result = CommonOccultUtils.is_fairy_occult_available()
        if not is_fairy_available_result:
            return is_fairy_available_result
        is_fairy_result = CommonOccultUtils.is_fairy(sim_info)
        if is_fairy_result:
            return is_fairy_result
        # loot_FairyOccult_AddOccult
        add_loot_action_id = 420057
        if CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(add_loot_action_id, sim_info):
            return CommonExecutionResult.TRUE
        return CommonExecutionResult.FALSE

    @classmethod
    def remove_fairy_occult(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """remove_fairy_occult(sim_info)

        Remove the Fairy Occult Type from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of removing the Fairy occult. True, if the Fairy Occult Type has been successfully removed from the specified Sim. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_fairy_available_result = CommonOccultUtils.is_fairy_occult_available()
        if not is_fairy_available_result:
            return is_fairy_available_result.reverse_result()
        is_fairy_result = CommonOccultUtils.is_fairy(sim_info)
        if not is_fairy_result:
            return is_fairy_result.reverse_result()
        traits: Tuple[Union[int, CommonTraitId], ...] = (
            CommonTraitId.OCCULT_FAIRY_ALL_AGES,
            CommonTraitId.OCCULT_FAIRY_TYAE,
            CommonTraitId.OCCULT_FAIRY_FAIRY_FORM,
            CommonTraitId.OCCULT_FAIRY_FLYING_DISALLOWED,
            CommonTraitId.OCCULT_FAIRY_FLYING_WALK_STYLE,
            CommonTraitId.OCCULT_FAIRY_HIGH_FAE_LINEAGE,
        )
        try:
            from cas.cas import remove_caspart_by_bodytype
            subject = sim_info
            occult_sim_info = subject.occult_tracker._sim_info_map[OccultType.FAIRY]
            if occult_sim_info is not None:
                modified_sim_info = SimInfoBaseWrapper(gender=subject.gender, age=subject.age, species=subject.species, first_name=subject.first_name, last_name=subject.last_name, breed_name=subject.breed_name, full_name_key=subject.full_name_key, breed_name_key=subject.breed_name_key)
                remove_caspart_by_bodytype(subject._base, modified_sim_info._base, BodyType.WINGS, True, True)
                option_flags = OutfitOverrideOptionFlags.DEFAULT
                from cas.cas import apply_siminfo_override
                apply_siminfo_override(subject._base, modified_sim_info._base, subject._base, option_flags)
                apply_siminfo_override(occult_sim_info._base, modified_sim_info._base, occult_sim_info._base, option_flags)
                occult_human_sim_info = subject.occult_tracker._sim_info_map[OccultType.HUMAN]
                if occult_human_sim_info is not None:
                    occult_human_sim_info.pelt_layers = modified_sim_info.pelt_layers
                    occult_human_sim_info._base.pelt_layers = modified_sim_info._base.pelt_layers
        except Exception as ex:
            cls.get_log().format_error_with_message('Failed to remove fairy wings from Sim.', sim=sim_info, exception=ex)
        CommonOccultUtils.switch_to_occult_form(sim_info, OccultType.HUMAN)
        return CommonTraitUtils.remove_traits(sim_info, traits)

    @classmethod
    def add_plant_sim_occult(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """add_plant_sim_occult(sim_info)

        Add the Plant Sim Occult Type to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of adding the Plant Sim occult. True, if the Sim has successfully become a Plant Sim. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_plant_sim_available_result = CommonOccultUtils.is_plant_sim_occult_available()
        if not is_plant_sim_available_result:
            return is_plant_sim_available_result
        # loot_Buff_PlantSims_BecomePlantSim
        add_loot_action_id = 163440
        if CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(add_loot_action_id, sim_info):
            return CommonExecutionResult.TRUE
        return CommonExecutionResult.FALSE

    @classmethod
    def remove_plant_sim_occult(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """remove_plant_sim_occult(sim_info)

        Remove the Plant Sim Occult Type from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of removing the Plant Sim occult. True, if the Plant Sim Occult Type has been successfully removed from the specified Sim. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_plant_sim_available_result = CommonOccultUtils.is_plant_sim_occult_available()
        if not is_plant_sim_available_result:
            return is_plant_sim_available_result.reverse_result()
        remove_result = CommonBuffUtils.remove_buff(sim_info, CommonBuffId.PLANT_SIMS_MAIN_VISIBLE)
        if not remove_result:
            return remove_result
        return CommonExecutionResult.TRUE

    @classmethod
    def add_robot_occult(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """add_robot_occult(sim_info)

        Add the Robot Occult Type to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of adding the robot occult. True, if the Sim has successfully become a Robot. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_robot_available_result = CommonOccultUtils.is_robot_occult_available()
        if not is_robot_available_result:
            return is_robot_available_result
        is_robot_result = CommonOccultUtils.is_robot(sim_info)
        if is_robot_result:
            return is_robot_result
        return CommonTraitUtils.add_trait(sim_info, CommonTraitId.OCCULT_ROBOT)

    @classmethod
    def remove_robot_occult(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """remove_robot_occult(sim_info)

        Remove the Robot Occult Type from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of removing the robot occult. True, if the Robot Occult Type has been successfully removed from the specified Sim. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_robot_available_result = CommonOccultUtils.is_robot_occult_available()
        if not is_robot_available_result:
            return is_robot_available_result.reverse_result()
        is_robot_result = CommonOccultUtils.is_robot(sim_info)
        if not is_robot_result:
            return is_robot_result.reverse_result()
        return CommonTraitUtils.remove_trait(sim_info, CommonTraitId.OCCULT_ROBOT)

    @classmethod
    def add_scarecrow_occult(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """add_scarecrow_occult(sim_info)

        Add the Scarecrow Occult Type to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of adding the Scarecrow occult. True, if the Sim has successfully become a Scarecrow. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_scarecrow_available_result = CommonOccultUtils.is_scarecrow_occult_available()
        if not is_scarecrow_available_result:
            return is_scarecrow_available_result
        is_scarecrow_result = CommonOccultUtils.is_scarecrow(sim_info)
        if is_scarecrow_result:
            return is_scarecrow_result

        if not CommonTraitUtils.add_trait(sim_info, CommonTraitId.SCARECROW):
            return CommonTestResult(False, reason=f'Failed to add scarecrow trait to {sim_info}.', hide_tooltip=True)

        scarecrow_cas_part_ids = (
            # yuBody_EP05ScareCrow_Gray
            198149,
            # yuBody_EP05ScareCrow_Red
            198148,
            # yuBody_EP05ScareCrow_Purple
            198147
        )
        chosen_id = random.choice(scarecrow_cas_part_ids)
        from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
        if CommonCASUtils.attach_cas_part_to_all_outfits_of_sim(sim_info, CommonCASPart(chosen_id)):
            current_outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)
            CommonOutfitUtils.trigger_outfit_generated(sim_info, current_outfit_category_and_index)
            CommonOutfitUtils.set_outfit_dirty(sim_info, current_outfit_category_and_index[0])
            CommonOutfitUtils.set_current_outfit(sim_info, current_outfit_category_and_index)
            return CommonExecutionResult.TRUE
        CommonSimAppearanceModifierUtils.evaluate_appearance_modifiers(sim_info)
        return CommonExecutionResult.FALSE

    @classmethod
    def remove_scarecrow_occult(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """remove_scarecrow_occult(sim_info)

        Remove the Scarecrow Occult Type from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of removing the Scarecrow occult. True, if the Scarecrow Occult Type has been successfully removed from the specified Sim. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_scarecrow_available_result = CommonOccultUtils.is_scarecrow_occult_available()
        if not is_scarecrow_available_result:
            return is_scarecrow_available_result.reverse_result()
        is_scarecrow_result = CommonOccultUtils.is_scarecrow(sim_info)
        if not is_scarecrow_result:
            return is_scarecrow_result.reverse_result()
        scarecrow_cas_parts = (
            # yuBody_EP05ScareCrow_Gray
            CommonCASPart(198149),
            # yuBody_EP05ScareCrow_Red
            CommonCASPart(198148),
            # yuBody_EP05ScareCrow_Purple
            CommonCASPart(198147)
        )

        from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
        if CommonCASUtils.detach_cas_parts_from_all_outfits_of_sim(sim_info, scarecrow_cas_parts):
            current_outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)
            CommonOutfitUtils.trigger_outfit_generated(sim_info, current_outfit_category_and_index)
            CommonOutfitUtils.set_outfit_dirty(sim_info, current_outfit_category_and_index[0])
            CommonOutfitUtils.set_current_outfit(sim_info, current_outfit_category_and_index)
        return CommonTraitUtils.remove_trait(sim_info, CommonTraitId.SCARECROW)

    @classmethod
    def add_skeleton_occult(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """add_skeleton_occult(sim_info)

        Add the Skeleton Occult Type to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of adding the Skeleton occult. True, if the Sim has successfully become a Skeleton. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_skeleton_available_result = CommonOccultUtils.is_skeleton_occult_available()
        if not is_skeleton_available_result:
            return is_skeleton_available_result
        is_skeleton_result = CommonOccultUtils.is_skeleton(sim_info)
        if is_skeleton_result:
            return is_skeleton_result
        # loot_Skeleton_Add
        add_loot_id = 175969
        if CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(add_loot_id, sim_info):
            return CommonExecutionResult.TRUE
        return CommonExecutionResult.FALSE

    @classmethod
    def remove_skeleton_occult(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """remove_skeleton_occult(sim_info)

        Remove the Skeleton Occult Type from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of removing the Skeleton occult. True, if the Skeleton Occult Type has been successfully removed from the specified Sim. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_skeleton_available_result = CommonOccultUtils.is_skeleton_occult_available()
        if not is_skeleton_available_result:
            return is_skeleton_available_result.reverse_result()
        is_skeleton_result = CommonOccultUtils.is_skeleton(sim_info)
        if not is_skeleton_result:
            return is_skeleton_result.reverse_result()
        # loot_Skeleton_Remove
        remove_loot_id = 175975
        if CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(remove_loot_id, sim_info):
            return CommonExecutionResult.TRUE
        return CommonExecutionResult.FALSE

    @classmethod
    def add_vampire_occult(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """add_vampire_occult(sim_info)

        Add the Vampire Occult Type to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of adding the Vampire occult. True, if the Sim has successfully become a Vampire. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_vampire_available_result = CommonOccultUtils.is_vampire_occult_available()
        if not is_vampire_available_result:
            return is_vampire_available_result
        is_vampire_result = CommonOccultUtils.is_vampire(sim_info)
        if is_vampire_result:
            return is_vampire_result
        # loot_VampireCreation_NewVampire
        add_loot_id = 149538
        if CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(add_loot_id, sim_info):
            return CommonExecutionResult.TRUE
        return CommonExecutionResult.FALSE

    @classmethod
    def remove_vampire_occult(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """remove_vampire_occult(sim_info)

        Remove the Vampire Occult Type from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of removing the Vampire occult. True, if the Vampire Occult Type has been successfully removed from the specified Sim. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_vampire_available_result = CommonOccultUtils.is_vampire_occult_available()
        if not is_vampire_available_result:
            return is_vampire_available_result.reverse_result()
        is_vampire_result = CommonOccultUtils.is_vampire(sim_info)
        if not is_vampire_result:
            is_vampire_result.reverse_result()
        loot_action_ids: Tuple[int, ...] = (
            # loot_VampireCure_RemoveVampirism
            150170,
            # loot_Life_ResetProgress
            31238
        )
        result = CommonSimLootActionUtils.apply_loot_actions_by_ids_to_sim(loot_action_ids, sim_info)
        if result:
            CommonSimBucksUtils.remove_all_perks(sim_info, CommonBucksType.VAMPIRE_POWER, reason='Vampire removed', remove_perk_points=True)
            CommonSimBucksUtils.remove_all_perks(sim_info, CommonBucksType.VAMPIRE_WEAKNESS, reason='Vampire removed', remove_perk_points=True)
            return CommonExecutionResult.TRUE
        return CommonExecutionResult.FALSE

    @classmethod
    def add_witch_occult(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """add_witch_occult(sim_info)

        Add the Witch Occult Type to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of adding the Witch occult. True, if the Sim has successfully become a Witch. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_witch_available_result = CommonOccultUtils.is_witch_occult_available()
        if not is_witch_available_result:
            return is_witch_available_result
        is_witch_result = CommonOccultUtils.is_witch(sim_info)
        if is_witch_result:
            return is_witch_result
        # loot_WitchOccult_AddOccult
        add_loot_id = 215080
        if CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(add_loot_id, sim_info):
            return CommonExecutionResult.TRUE
        return CommonExecutionResult.FALSE

    @classmethod
    def remove_witch_occult(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """remove_witch_occult(sim_info)

        Remove the Witch Occult Type from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of removing the Witch occult. True, if the Witch Occult Type has been successfully removed from the specified Sim. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_witch_available_result = CommonOccultUtils.is_witch_occult_available()
        if not is_witch_available_result:
            is_witch_available_result.reverse_result()
        is_witch_result = CommonOccultUtils.is_witch(sim_info)
        if not is_witch_result:
            return is_witch_result.reverse_result()
        # loot_WitchOccult_RemoveOccult
        remove_loot_id = 215274
        result = CommonSimLootActionUtils.apply_loot_actions_by_id_to_duo_sims(remove_loot_id, sim_info, sim_info)
        if result:
            CommonSimBucksUtils.remove_all_perks(sim_info, CommonBucksType.WITCH_PERK, reason='Witch removed', remove_perk_points=True)
            CommonSimSpellUtils.remove_all_spells(sim_info)
            return CommonExecutionResult.TRUE
        return CommonExecutionResult.FALSE

    @classmethod
    def add_werewolf_occult(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """add_werewolf_occult(sim_info)

        Add the Werewolf Occult Type to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of adding the Werewolf occult. True, if the Sim has successfully become a Werewolf. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_werewolf_available_result = CommonOccultUtils.is_werewolf_occult_available()
        if not is_werewolf_available_result:
            return is_werewolf_available_result
        is_werewolf_result = CommonOccultUtils.is_werewolf(sim_info)
        if is_werewolf_result:
            return is_werewolf_result
        # loot_Werewolf_AddOccultTrait
        add_loot_id = 290058
        if CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(add_loot_id, sim_info):
            return CommonExecutionResult.TRUE
        return CommonExecutionResult.FALSE

    @classmethod
    def remove_werewolf_occult(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """remove_werewolf_occult(sim_info)

        Remove the Werewolf Occult Type from a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of removing the Werewolf occult. True, if the Werewolf Occult Type has been successfully removed from the specified Sim. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_werewolf_available_result = CommonOccultUtils.is_werewolf_occult_available()
        if not is_werewolf_available_result:
            return is_werewolf_available_result.reverse_result()
        is_werewolf_result = CommonOccultUtils.is_werewolf(sim_info)
        if not is_werewolf_result:
            return is_werewolf_result.reverse_result()
        # loot_WerewolfCreation_WerewolfCure
        remove_loot_id = 291816
        result = CommonSimLootActionUtils.apply_loot_actions_by_id_to_sim(remove_loot_id, sim_info)
        if result:
            CommonSimBucksUtils.remove_all_perks(sim_info, CommonBucksType.WEREWOLF_ABILITY, reason='Werewolf removed', remove_perk_points=True)
            return CommonExecutionResult.TRUE
        return CommonExecutionResult.FALSE

    @classmethod
    def add_all_occults(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """add_all_occults(sim_info)

        Add all Occult Types to a Sim. i.e. Make them an Alien, a Vampire, a Witch, etc.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of adding all occult types. True, if all Occult Types were successfully added to the specified Sim. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        switch_to_non_occult_form_result = CommonOccultUtils.switch_to_occult_form(sim_info, OccultType.HUMAN)
        if not switch_to_non_occult_form_result:
            return switch_to_non_occult_form_result
        for occult_type in CommonOccultType.get_all(exclude_occult_types=(CommonOccultType.NON_OCCULT, CommonOccultType.GHOST, CommonOccultType.PLANT_SIM, CommonOccultType.ROBOT, CommonOccultType.SKELETON)):
            if not CommonOccultUtils.is_occult_available(occult_type):
                continue
            add_result = CommonOccultUtils.add_occult(sim_info, occult_type)
            if not add_result:
                return add_result
        return CommonExecutionResult.TRUE

    @classmethod
    def remove_all_occults(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """remove_all_occults(sim_info)

        Remove all Occult Types from a Sim. i.e. Make them a Non-Occult only.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of removing all occult types. True, if all Occult Types were successfully removed from the specified Sim. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        switch_to_non_occult_form_result = CommonOccultUtils.switch_to_occult_form(sim_info, OccultType.HUMAN)
        if not switch_to_non_occult_form_result:
            return switch_to_non_occult_form_result
        for occult_type in CommonOccultType.get_all(exclude_occult_types=(CommonOccultType.NON_OCCULT, CommonOccultType.GHOST, CommonOccultType.PLANT_SIM)):
            if not CommonOccultUtils.is_occult_available(occult_type):
                continue
            remove_result = CommonOccultUtils.remove_occult(sim_info, occult_type)
            if not remove_result:
                return remove_result

        if CommonOccultUtils.is_occult_available(CommonOccultType.GHOST):
            remove_result = CommonOccultUtils.remove_occult(sim_info, CommonOccultType.GHOST)
            if not remove_result:
                return remove_result

        if CommonOccultUtils.is_occult_available(CommonOccultType.PLANT_SIM):
            remove_result = CommonOccultUtils.remove_occult(sim_info, CommonOccultType.PLANT_SIM)
            if not remove_result:
                return remove_result
        return CommonExecutionResult.TRUE

    @classmethod
    def switch_to_occult_form(cls, sim_info: SimInfo, occult_type: Union[OccultType, CommonOccultType]) -> CommonExecutionResult:
        """switch_to_occult_form(sim_info, occult_type)

        Switch a Sim to an Occult Form.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param occult_type: The type of Occult to switch to.
        :type occult_type: Union[OccultType, CommonOccultType]
        :return: The result of switching a Sim to an occult form. True, if the Sim successfully switched to the specified Occult Type. False, if the Sim failed to switch to the specified Occult Type or if they do not have that Occult Type to switch to.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            return CommonTestResult(False, reason='sim_info was None!', hide_tooltip=True)
        if isinstance(occult_type, CommonOccultType):
            vanilla_occult_type = CommonOccultType.convert_to_vanilla(occult_type)
            if vanilla_occult_type is None:
                return CommonExecutionResult(False, reason=f'{sim_info} failed to switch to occult type {occult_type.name}. Occult Type has no vanilla type associated with it.', tooltip_text=CommonStringId.S4CL_SIM_FAILED_TO_SWITCH_TO_OCCULT_TYPE_VANILLA_OCCULT_TYPE_DOES_NOT_EXIST, tooltip_tokens=(sim_info, CommonOccultType.convert_to_localized_string_id(occult_type)))
        else:
            vanilla_occult_type = occult_type
        # noinspection PyPropertyAccess
        sim_info.occult_tracker.set_pending_occult_type(vanilla_occult_type)
        sim_info.occult_tracker.switch_to_occult_type(vanilla_occult_type)
        return CommonExecutionResult.TRUE

    @classmethod
    def is_vampire(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_vampire(sim_info)

        Determine if a Sim is a Vampire.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is a Vampire. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_vampire_available_result = CommonOccultUtils.is_vampire_occult_available()
        if not is_vampire_available_result:
            return is_vampire_available_result
        if CommonTraitUtils.has_trait(sim_info, CommonTraitId.OCCULT_VAMPIRE) or CommonOccultUtils._has_occult_trait(sim_info, CommonTraitId.OCCULT_ALIEN):
            return CommonTestResult(True, reason=f'{sim_info} is a Vampire. They had Occult Vampire Trait.', tooltip_text=CommonStringId.S4CL_SIM_IS_A_VAMPIRE, tooltip_tokens=(sim_info,))
        if CommonOccultUtils.has_occult_type(sim_info, OccultType.VAMPIRE):
            return CommonTestResult(True, reason=f'{sim_info} is a Vampire. They had Occult Type Vampire.', tooltip_text=CommonStringId.S4CL_SIM_IS_A_VAMPIRE, tooltip_tokens=(sim_info,))
        return CommonTestResult(False, reason=f'{sim_info} is not a Vampire.', tooltip_text=CommonStringId.S4CL_SIM_IS_NOT_A_VAMPIRE, tooltip_tokens=(sim_info,))

    @classmethod
    def is_alien(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_alien(sim_info)

        Determine if a Sim is an Alien.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is an Alien. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_alien_available_result = CommonOccultUtils.is_alien_occult_available()
        if not is_alien_available_result:
            return is_alien_available_result
        if CommonTraitUtils.has_trait(sim_info, CommonTraitId.OCCULT_ALIEN) or CommonOccultUtils._has_occult_trait(sim_info, CommonTraitId.OCCULT_ALIEN):
            return CommonTestResult(True, reason=f'{sim_info} is an Alien. They had Occult Alien Trait.', tooltip_text=CommonStringId.S4CL_SIM_IS_AN_ALIEN, tooltip_tokens=(sim_info,))
        if CommonOccultUtils.has_occult_type(sim_info, OccultType.ALIEN):
            return CommonTestResult(True, reason=f'{sim_info} is an Alien. They had Occult Type Alien.', tooltip_text=CommonStringId.S4CL_SIM_IS_AN_ALIEN, tooltip_tokens=(sim_info,))
        return CommonTestResult(False, reason=f'{sim_info} is not an Alien.', tooltip_text=CommonStringId.S4CL_SIM_IS_NOT_AN_ALIEN, tooltip_tokens=(sim_info,))

    @classmethod
    def is_fairy(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_fairy(sim_info)

        Determine if a Sim is a Fairy.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is a Fairy. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_fairy_available_result = CommonOccultUtils.is_fairy_occult_available()
        if not is_fairy_available_result:
            return is_fairy_available_result
        if CommonTraitUtils.has_trait(sim_info, CommonTraitId.OCCULT_FAIRY_ALL_AGES) or CommonOccultUtils._has_occult_trait(sim_info, CommonTraitId.OCCULT_FAIRY_ALL_AGES):
            return CommonTestResult(True, reason=f'{sim_info} is a Fairy. They had Occult Fairy Trait.', tooltip_text=CommonStringId.S4CL_SIM_IS_A_FAIRY, tooltip_tokens=(sim_info,))
        if CommonOccultUtils.has_occult_type(sim_info, OccultType.FAIRY):
            return CommonTestResult(True, reason=f'{sim_info} is a Fairy. They had Occult Type Fairy.', tooltip_text=CommonStringId.S4CL_SIM_IS_A_FAIRY, tooltip_tokens=(sim_info,))
        return CommonTestResult(False, reason=f'{sim_info} is not a Fairy.', tooltip_text=CommonStringId.S4CL_SIM_IS_NOT_A_FAIRY, tooltip_tokens=(sim_info,))

    @classmethod
    def is_plant_sim(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_plant_sim(sim_info)

        Determine if a Sim is a Plant Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is a Plant Sim. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_plant_sim_available_result = CommonOccultUtils.is_plant_sim_occult_available()
        if not is_plant_sim_available_result:
            return is_plant_sim_available_result
        if CommonTraitUtils.has_trait(sim_info, CommonTraitId.PLANT_SIM):
            return CommonTestResult(False, reason=f'{sim_info} is a Plant Sim.', tooltip_text=CommonStringId.S4CL_SIM_IS_A_PLANT_SIM, tooltip_tokens=(sim_info,))
        return CommonTestResult(False, reason=f'{sim_info} is not a Plant Sim.', tooltip_text=CommonStringId.S4CL_SIM_IS_NOT_A_PLANT_SIM, tooltip_tokens=(sim_info,))

    @classmethod
    def is_ghost(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_ghost(sim_info)

        Determine if a Sim is a Ghost.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is a Ghost. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_ghost_available_result = CommonOccultUtils.is_ghost_occult_available()
        if not is_ghost_available_result:
            return is_ghost_available_result
        equipped_sim_traits = CommonTraitUtils.get_equipped_traits(sim_info)
        for trait in equipped_sim_traits:
            if CommonTraitUtils.is_ghost_trait(trait):
                return CommonTestResult(False, reason=f'{sim_info} is a Ghost.', tooltip_text=CommonStringId.S4CL_SIM_IS_A_GHOST, tooltip_tokens=(sim_info,))
        return CommonTestResult(False, reason=f'{sim_info} is not a Ghost.', tooltip_text=CommonStringId.S4CL_SIM_IS_NOT_A_GHOST, tooltip_tokens=(sim_info,))

    @classmethod
    def is_scarecrow(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_scarecrow(sim_info)

        Determine if a Sim is a Scarecrow.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is a Scarecrow. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_scarecrow_available_result = CommonOccultUtils.is_scarecrow_occult_available()
        if not is_scarecrow_available_result:
            return is_scarecrow_available_result
        if CommonTraitUtils.has_trait(sim_info, CommonTraitId.SCARECROW):
            return CommonTestResult(True, reason=f'{sim_info} is a Scarecrow.', tooltip_text=CommonStringId.S4CL_SIM_IS_A_SCARECROW, tooltip_tokens=(sim_info,))
        return CommonTestResult(False, reason=f'{sim_info} is not a Scarecrow.', tooltip_text=CommonStringId.S4CL_SIM_IS_NOT_A_SCARECROW, tooltip_tokens=(sim_info,))

    @classmethod
    def is_robot(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_robot(sim_info)

        Determine if a Sim is a Robot.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is a Robot. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_robot_available_result = CommonOccultUtils.is_robot_occult_available()
        if not is_robot_available_result:
            return is_robot_available_result
        equipped_sim_traits = CommonTraitUtils.get_equipped_traits(sim_info)
        for trait in equipped_sim_traits:
            trait_type = getattr(trait, 'trait_type', -1)
            if trait_type == TraitType.ROBOT:
                return CommonTestResult(True, reason=f'{sim_info} is a Robot.', tooltip_text=CommonStringId.S4CL_SIM_IS_A_ROBOT, tooltip_tokens=(sim_info,))
        return CommonTestResult(False, reason=f'{sim_info} is not a Robot.', tooltip_text=CommonStringId.S4CL_SIM_IS_NOT_A_ROBOT, tooltip_tokens=(sim_info,))
    
    @classmethod
    def is_skeleton(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_skeleton(sim_info)

        Determine if a Sim is a Skeleton.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is the a Skeleton. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_skeleton_available_result = CommonOccultUtils.is_skeleton_occult_available()
        if not is_skeleton_available_result:
            return is_skeleton_available_result
        equipped_sim_traits = CommonTraitUtils.get_equipped_traits(sim_info)
        skeleton_trait_ids = {
            CommonTraitId.HIDDEN_SKELETON,
            CommonTraitId.HIDDEN_SKELETON_SERVICE_SKELETON,
            CommonTraitId.HIDDEN_SKELETON_TEMPLE_SKELETON
        }
        for trait in equipped_sim_traits:
            trait_id = CommonTraitUtils.get_trait_id(trait)
            if trait_id in skeleton_trait_ids:
                return CommonTestResult(True, reason=f'{sim_info} is a Skeleton.', tooltip_text=CommonStringId.S4CL_SIM_IS_A_SKELETON, tooltip_tokens=(sim_info,))
        return CommonTestResult(False, reason=f'{sim_info} is not a Skeleton.', tooltip_text=CommonStringId.S4CL_SIM_IS_NOT_A_SKELETON, tooltip_tokens=(sim_info,))

    @classmethod
    def is_werewolf(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_werewolf(sim_info)

        Determine if a Sim is a Werewolf

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is a Werewolf. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_werewolf_available_result = CommonOccultUtils.is_werewolf_occult_available()
        if not is_werewolf_available_result:
            return is_werewolf_available_result
        if CommonOccultUtils._has_occult_trait(sim_info, CommonTraitId.OCCULT_WEREWOLF):
            return CommonTestResult(True, reason=f'{sim_info} is a Werewolf. They had Occult Werewolf Trait.', tooltip_text=CommonStringId.S4CL_SIM_IS_A_WEREWOLF, tooltip_tokens=(sim_info,))
        if CommonOccultUtils.has_occult_type(sim_info, OccultType.WEREWOLF):
            return CommonTestResult(True, reason=f'{sim_info} is a Werewolf. They had Occult Type Werewolf.', tooltip_text=CommonStringId.S4CL_SIM_IS_A_WEREWOLF, tooltip_tokens=(sim_info,))
        return CommonTestResult(False, reason=f'{sim_info} is not a Werewolf.', tooltip_text=CommonStringId.S4CL_SIM_IS_NOT_A_WEREWOLF, tooltip_tokens=(sim_info,))

    @classmethod
    def is_witch(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_witch(sim_info)

        Determine if a Sim is a Witch

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is a Witch. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_witch_available_result = CommonOccultUtils.is_witch_occult_available()
        if not is_witch_available_result:
            return is_witch_available_result
        if CommonOccultUtils._has_occult_trait(sim_info, CommonTraitId.OCCULT_WITCH):
            return CommonTestResult(True, reason=f'{sim_info} is a Witch. They had Occult Witch Trait.', tooltip_text=CommonStringId.S4CL_SIM_IS_A_WITCH, tooltip_tokens=(sim_info,))
        if CommonOccultUtils.has_occult_type(sim_info, OccultType.WITCH):
            return CommonTestResult(True, reason=f'{sim_info} is a Witch. They had Occult Type Witch.', tooltip_text=CommonStringId.S4CL_SIM_IS_A_WITCH, tooltip_tokens=(sim_info,))
        return CommonTestResult(False, reason=f'{sim_info} is not a Witch.', tooltip_text=CommonStringId.S4CL_SIM_IS_NOT_A_WITCH, tooltip_tokens=(sim_info,))

    @classmethod
    def is_mermaid(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_mermaid(sim_info)

        Determine if a Sim is a Mermaid

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is a Mermaid. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_mermaid_available_result = CommonOccultUtils.is_mermaid_occult_available()
        if not is_mermaid_available_result:
            return is_mermaid_available_result
        if CommonOccultUtils._has_occult_trait(sim_info, CommonTraitId.OCCULT_MERMAID):
            return CommonTestResult(True, reason=f'{sim_info} is a Mermaid. They had Occult Mermaid Trait.', tooltip_text=CommonStringId.S4CL_SIM_IS_A_MERMAID, tooltip_tokens=(sim_info,))
        if CommonOccultUtils.has_occult_type(sim_info, OccultType.MERMAID):
            return CommonTestResult(True, reason=f'{sim_info} is a Mermaid. They had Occult Type Mermaid.', tooltip_text=CommonStringId.S4CL_SIM_IS_A_MERMAID, tooltip_tokens=(sim_info,))
        return CommonTestResult(False, reason=f'{sim_info} is not a Mermaid.', tooltip_text=CommonStringId.S4CL_SIM_IS_NOT_A_MERMAID, tooltip_tokens=(sim_info,))

    @classmethod
    def is_in_mermaid_form(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_in_mermaid_form(sim_info)

        Determine if a Sim is in Mermaid Form (The Sim has a visible Tail).

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim has their Mermaid tail out. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_mermaid_available_result = CommonOccultUtils.is_mermaid_occult_available()
        if not is_mermaid_available_result:
            return is_mermaid_available_result
        if CommonOccultUtils.get_current_occult_type(sim_info) == OccultType.MERMAID:
            return CommonTestResult(True, reason=f'{sim_info} is currently in Mermaid Form.', tooltip_text=CommonStringId.S4CL_SIM_IS_CURRENTLY_IN_MERMAID_FORM, tooltip_tokens=(sim_info,))
        return CommonTestResult(False, reason=f'{sim_info} is not currently in Mermaid Form.', tooltip_text=CommonStringId.S4CL_SIM_IS_CURRENTLY_NOT_IN_MERMAID_FORM, tooltip_tokens=(sim_info,))

    @classmethod
    def is_mermaid_in_mermaid_form(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_mermaid_in_mermaid_form(sim_info)

        Determine if a Sim is a Mermaid and is in Mermaid Form (Their Tail is visible).

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is a Mermaid with their tail out. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_mermaid_available_result = CommonOccultUtils.is_mermaid_occult_available()
        if not is_mermaid_available_result:
            return is_mermaid_available_result
        is_mermaid_result = CommonOccultUtils.is_mermaid(sim_info)
        if not is_mermaid_result:
            return is_mermaid_result
        is_in_mermaid_form_result = CommonOccultUtils.is_in_mermaid_form(sim_info)
        if not is_in_mermaid_form_result:
            return is_in_mermaid_form_result
        return is_in_mermaid_form_result

    @classmethod
    def is_currently_human(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """is_currently_human(sim_info)

        Determine if a Sim is currently in their Human form (regardless of their Occult type).

        .. note:: The Human Occult is not the same as the Human Species! This means that Pets can have a "Human" Occult as their Non-Occult.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is currently a Human. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        return CommonOccultUtils.is_currently_a_non_occult(sim_info)

    @classmethod
    def is_currently_a_non_occult(cls, sim_info: SimInfo) -> CommonExecutionResult:
        """is_currently_a_non_occult(sim_info)

        Determine if a Sim is currently in a Non-Occult form (regardless of their Occult type).

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is currently in their Non-Occult form. False, if not.
        :rtype: CommonExecutionResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        if not hasattr(OccultType, 'HUMAN'):
            return CommonExecutionResult(False, reason='Humans (i.e. Non Occult Sims) do not exist. They are a myth! (At least in this game, possibly missing DLC or bugged Mods?)', tooltip_text=CommonStringId.S4CL_HUMAN_OCCULT_DOES_NOT_EXIST, tooltip_tokens=(sim_info,))
        current_occult = CommonOccultUtils.get_current_occult_type(sim_info)
        if current_occult == OccultType.HUMAN:
            return CommonExecutionResult(True, reason=f'{sim_info} is currently in Non Occult Form.', tooltip_text=CommonStringId.S4CL_SIM_IS_CURRENTLY_IN_NON_OCCULT_FORM, tooltip_tokens=(sim_info,))
        return CommonExecutionResult(False, reason=f'{sim_info} is currently in Occult Form.', tooltip_text=CommonStringId.S4CL_SIM_IS_CURRENTLY_IN_OCCULT_FORM, tooltip_tokens=(sim_info,))

    @classmethod
    def is_currently_a_mermaid(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_currently_a_mermaid(sim_info)

        Determine if a Sim is currently in a Mermaid form. (Not disguised)

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is currently in their Mermaid form. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        return CommonOccultUtils.is_in_mermaid_form(sim_info)

    @classmethod
    def is_currently_a_robot(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_currently_a_robot(sim_info)

        Determine if a Sim is currently in their Robot form.

        .. note:: In base game, if a Sim is a Robot then they are automatically in their Robot Form, since Robots do not have an alternative form.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is currently in their Robot form. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        return CommonOccultUtils.is_robot(sim_info)

    @classmethod
    def is_currently_a_scarecrow(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_currently_a_scarecrow(sim_info)

        Determine if a Sim is currently in their Scarecrow form.

        .. note:: In base game, if a Sim is a Scarecrow then they are automatically in their Scarecrow Form, since Scarecrows do not have an alternative form.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is currently in their Scarecrow form. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        return CommonOccultUtils.is_scarecrow(sim_info)

    @classmethod
    def is_currently_a_skeleton(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_currently_a_skeleton(sim_info)

        Determine if a Sim is currently in their Skeleton form.

        .. note:: In base game, if a Sim is a Skeleton then they are automatically in their Skeleton Form, since Skeletons do not have an alternative form.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is currently in their Skeleton form. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        return CommonOccultUtils.is_skeleton(sim_info)

    @classmethod
    def is_currently_a_plant_sim(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_currently_a_plant_sim(sim_info)

        Determine if a Sim is currently in their Plant Sim form.

        .. note:: In base game, if a Sim is a Plant Sim then they are automatically in their Plant Sim Form, since Plant Sims do not have an alternative form.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is currently in their Plant Sim form. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        return CommonOccultUtils.is_plant_sim(sim_info)

    @classmethod
    def is_currently_a_ghost(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_currently_a_ghost(sim_info)

        Determine if a Sim is currently in their Ghost form.

        .. note:: In base game, if a Sim is a Ghost then they are automatically in their Ghost Form, since Ghosts do not have an alternative form.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is currently in their Ghost form. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        return CommonOccultUtils.is_ghost(sim_info)

    @classmethod
    def is_currently_a_vampire(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_currently_a_vampire(sim_info)

        Determine if a Sim is currently in their Vampire form. (Not disguised)

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is currently in their Vampire form. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_vampire_available_result = CommonOccultUtils.is_vampire_occult_available()
        if not is_vampire_available_result:
            return is_vampire_available_result
        if CommonOccultUtils.get_current_occult_type(sim_info) == OccultType.VAMPIRE:
            return CommonTestResult(True, reason=f'{sim_info} is currently in Vampire Form.', tooltip_text=CommonStringId.S4CL_SIM_IS_CURRENTLY_IN_VAMPIRE_FORM, tooltip_tokens=(sim_info,))
        return CommonTestResult(False, reason=f'{sim_info} is not currently in Vampire Form.', tooltip_text=CommonStringId.S4CL_SIM_IS_CURRENTLY_NOT_IN_VAMPIRE_FORM, tooltip_tokens=(sim_info,))

    @classmethod
    def is_currently_an_alien(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_currently_an_alien(sim_info)

        Determine if a Sim is currently in their Alien form. (Not disguised)

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is currently in their Alien form. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_alien_available_result = CommonOccultUtils.is_alien_occult_available()
        if not is_alien_available_result:
            return is_alien_available_result
        if CommonOccultUtils.get_current_occult_type(sim_info) == OccultType.ALIEN:
            return CommonTestResult(True, reason=f'{sim_info} is currently in Alien Form.', tooltip_text=CommonStringId.S4CL_SIM_IS_CURRENTLY_IN_ALIEN_FORM, tooltip_tokens=(sim_info,))
        return CommonTestResult(False, reason=f'{sim_info} is not currently in Alien Form.', tooltip_text=CommonStringId.S4CL_SIM_IS_CURRENTLY_NOT_IN_ALIEN_FORM, tooltip_tokens=(sim_info,))

    @classmethod
    def is_currently_a_fairy(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_currently_a_fairy(sim_info)

        Determine if a Sim is currently in their Fairy form.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is currently in their Fairy form. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        if CommonTraitUtils.has_trait(sim_info, CommonTraitId.OCCULT_FAIRY_FAIRY_FORM):
            return CommonTestResult(True, reason=f'{sim_info} is currently in Fairy Form.', tooltip_text=CommonStringId.S4CL_SIM_IS_CURRENTLY_IN_FAIRY_FORM, tooltip_tokens=(sim_info,))
        return CommonTestResult(False, reason=f'{sim_info} is not currently in Fairy Form.', tooltip_text=CommonStringId.S4CL_SIM_IS_CURRENTLY_NOT_IN_FAIRY_FORM, tooltip_tokens=(sim_info,))

    @classmethod
    def is_currently_a_werewolf(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_currently_a_werewolf(sim_info)

        Determine if a Sim is currently in their Werewolf form.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is currently in their Werewolf form. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        if CommonTraitUtils.has_trait(sim_info, CommonTraitId.OCCULT_WEREWOLF_WEREFORM):
            return CommonTestResult(True, reason=f'{sim_info} is currently in Werewolf Form.', tooltip_text=CommonStringId.S4CL_SIM_IS_CURRENTLY_IN_WEREWOLF_FORM, tooltip_tokens=(sim_info,))
        return CommonTestResult(False, reason=f'{sim_info} is not currently in Werewolf Form.', tooltip_text=CommonStringId.S4CL_SIM_IS_CURRENTLY_NOT_IN_WEREWOLF_FORM, tooltip_tokens=(sim_info,))

    @classmethod
    def is_currently_a_witch(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_currently_a_witch(sim_info)

        Determine if a Sim is currently in their Witch form. (Not disguised)

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of testing. True, if the Sim is currently in their Witch form. False, if not.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        is_witch_available_result = CommonOccultUtils.is_witch_occult_available()
        if not is_witch_available_result:
            return is_witch_available_result
        if CommonOccultUtils.get_current_occult_type(sim_info) == OccultType.WITCH:
            return CommonTestResult(True, reason=f'{sim_info} is currently in Witch Form.', tooltip_text=CommonStringId.S4CL_SIM_IS_CURRENTLY_IN_WITCH_FORM, tooltip_tokens=(sim_info,))
        return CommonTestResult(False, reason=f'{sim_info} is not currently in Witch Form.', tooltip_text=CommonStringId.S4CL_SIM_IS_CURRENTLY_NOT_IN_WITCH_FORM, tooltip_tokens=(sim_info,))

    @classmethod
    def get_sim_info_of_all_occults_gen(cls, sim_info: SimInfo, *exclude_occult_types: OccultType) -> Iterator[SimInfo]:
        """get_sim_info_of_all_occults_gen(sim_info, *exclude_occult_types)

        Retrieve a generator of SimInfo objects for all Occults of a sim.

        .. warning:: Obsolete, please use :func:`~get_sim_info_for_all_occults_gen` instead.

        :param sim_info: The Sim to locate the Occults of.
        :type sim_info: SimInfo
        :param exclude_occult_types: A collection of OccultTypes to exclude from the resulting SimInfo list.
        :type exclude_occult_types: OccultType
        :return: An iterator of Sims for all occult types of the Sim.
        :rtype: Iterator[SimInfo]
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        return CommonOccultUtils.get_sim_info_for_all_occults_gen(sim_info, exclude_occult_types)

    @classmethod
    def has_full_body_cas_part_assigned_to_current_occult_of(cls, sim_info: SimInfo) -> CommonTestResult:
        """has_full_body_cas_part_assigned_to_occult(sim_info)

        Determine if the Sim is currently an occult that has a Full Body CAS Part associated with it. Such as a Skeleton (Skeleton Part) or Robot (Humanoid Bot Frame).

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of the test. True, if the Sim is currently an occult with a full body outfit. False, if not.
        :rtype: CommonTestResult
        """
        current_occult_type = CommonOccultType.determine_current_occult_type(sim_info)
        return cls.occult_has_full_body_cas_part(current_occult_type)

    @classmethod
    def occult_has_full_body_cas_part(cls, occult_type: CommonOccultType) -> CommonTestResult:
        """occult_has_full_body_cas_part(occult_type)

        Determine an occult type has a Full Body CAS Part associated with it. Such as a Skeleton (Skeleton Part) or Robot (Humanoid Bot Frame).

        :param occult_type: The occult type to check.
        :type occult_type: CommonOccultType
        :return: The result of the test. True, if the occult type has a full body outfit associated with it. False, if not.
        :rtype: CommonTestResult
        """
        if occult_type in (CommonOccultType.ROBOT, CommonOccultType.SKELETON, CommonOccultType.SCARECROW):
            return CommonTestResult.TRUE
        return CommonTestResult.FALSE

    @classmethod
    def _has_occult_trait(cls, sim_info: SimInfo, trait_id: Union[int, CommonTraitId]) -> bool:
        return CommonOccultUtils._has_occult_traits(sim_info, (trait_id,))

    @classmethod
    def _has_occult_traits(cls, sim_info: SimInfo, trait_ids: Iterator[Union[int, CommonTraitId]]) -> bool:
        if sim_info is None:
            return False
        equipped_traits = CommonTraitUtils.get_equipped_traits(sim_info)
        for equipped_trait in equipped_traits:
            trait_id = CommonTraitUtils.get_trait_id(equipped_trait)
            if trait_id in trait_ids:
                return True
        return False

    @classmethod
    def get_current_occult_type(cls, sim_info: SimInfo) -> Union[OccultType, None]:
        """get_current_occult_type(sim_info)

        Retrieve the current occult type of the Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The current occult type of the Sim or None if the Sim does not have a current occult type.
        :rtype: Union[OccultType, None]
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        if not hasattr(sim_info, 'current_occult_types'):
            if not hasattr(sim_info, '_base') or not hasattr(sim_info._base, 'current_occult_types'):
                return None
            return OccultType(sim_info._base.current_occult_types)
        # noinspection PyPropertyAccess
        return OccultType(sim_info.current_occult_types)

    @classmethod
    def is_occult_available(cls, occult_type: CommonOccultType) -> CommonTestResult:
        """is_occult_available(occult_type)

        Determine if an Occult is available for us.

        .. note:: An Occult is available for use usually when it exists in a persons game, such as the WITCH occult existing only when someone has the Realm Of Magic DLC, but does not exist otherwise.

        :param occult_type: An occult type.
        :type occult_type: CommonOccultType
        :return: The result of testing. True, if the occult is available for use. False, if not.
        :rtype: CommonTestResult
        """
        if occult_type == CommonOccultType.NON_OCCULT:
            return CommonTestResult(True, reason='Obviously the Non Occult "occult type" is available, what did you expect?', hide_tooltip=True)
        occult_type_mappings = {
            CommonOccultType.ALIEN: CommonOccultUtils.is_alien_occult_available,
            CommonOccultType.FAIRY: CommonOccultUtils.is_fairy_occult_available,
            CommonOccultType.MERMAID: CommonOccultUtils.is_mermaid_occult_available,
            CommonOccultType.ROBOT: CommonOccultUtils.is_robot_occult_available,
            CommonOccultType.SCARECROW: CommonOccultUtils.is_scarecrow_occult_available,
            CommonOccultType.SKELETON: CommonOccultUtils.is_skeleton_occult_available,
            CommonOccultType.VAMPIRE: CommonOccultUtils.is_vampire_occult_available,
            CommonOccultType.WITCH: CommonOccultUtils.is_witch_occult_available,
            CommonOccultType.PLANT_SIM: CommonOccultUtils.is_plant_sim_occult_available,
            CommonOccultType.GHOST: CommonOccultUtils.is_ghost_occult_available,
            CommonOccultType.WEREWOLF: CommonOccultUtils.is_werewolf_occult_available,
        }
        if occult_type not in occult_type_mappings:
            return CommonTestResult(False, reason=f'Occult Type {occult_type} is not available because it is not a valid occult type or it has not been implemented yet.', tooltip_text=CommonStringId.S4CL_OCCULT_TYPE_IS_NOT_AVAILABLE_OR_SUPPORT_FOR_IT_HAS_NOT_BEEN_IMPLEMENTED, tooltip_tokens=(CommonOccultType.convert_to_localized_string_id(occult_type),))
        return occult_type_mappings[occult_type]()

    @classmethod
    def is_alien_occult_available(cls) -> CommonTestResult:
        """is_alien_occult_available()

        Determine if the Alien Occult is available.

        :return: The result of testing. True, if the Alien Occult is available. False, if not.
        :rtype: CommonTestResult
        """
        if not hasattr(OccultType, 'ALIEN'):
            return CommonTestResult(False, reason='Aliens do not exist. They are a myth! (At least in this game, possibly missing DLC or bugged Mods?)', tooltip_text=CommonStringId.S4CL_ALIEN_OCCULT_DOES_NOT_EXIST)
        if not CommonTraitUtils.is_trait_available(CommonTraitId.OCCULT_ALIEN):
            return CommonTestResult(False, reason='The Alien trait is not available.', tooltip_text=CommonStringId.S4CL_ALIEN_TRAIT_DOES_NOT_EXIST)
        return CommonTestResult.TRUE

    @classmethod
    def is_fairy_occult_available(cls) -> CommonTestResult:
        """is_fairy_occult_available()

        Determine if the Fairy Occult is available.

        :return: The result of testing. True, if the Fairy Occult is available.. False, if not.
        :rtype: CommonTestResult
        """
        if not hasattr(OccultType, 'FAIRY'):
            return CommonTestResult(False, reason='Fairies do not exist. They are a myth! (At least in this game, possibly missing DLC or bugged Mods?)', tooltip_text=CommonStringId.S4CL_FAIRY_OCCULT_DOES_NOT_EXIST)
        if not CommonTraitUtils.is_trait_available(CommonTraitId.OCCULT_FAIRY_ALL_AGES):
            return CommonTestResult(False, reason='The Fairy trait is not available.', tooltip_text=CommonStringId.S4CL_FAIRY_TRAIT_DOES_NOT_EXIST)
        return CommonTestResult.TRUE

    @classmethod
    def is_mermaid_occult_available(cls) -> CommonTestResult:
        """is_mermaid_occult_available()

        Determine if the Mermaid Occult is available.

        :return: The result of testing. True, if the Mermaid Occult is available.. False, if not.
        :rtype: CommonTestResult
        """
        if not hasattr(OccultType, 'MERMAID'):
            return CommonTestResult(False, reason='Mermaids do not exist. They are a myth! (At least in this game, possibly missing DLC or bugged Mods?)', tooltip_text=CommonStringId.S4CL_MERMAID_OCCULT_DOES_NOT_EXIST)
        if not CommonTraitUtils.is_trait_available(CommonTraitId.OCCULT_MERMAID):
            return CommonTestResult(False, reason='The Mermaid trait is not available.', tooltip_text=CommonStringId.S4CL_MERMAID_TRAIT_DOES_NOT_EXIST)
        return CommonTestResult.TRUE

    @classmethod
    def is_robot_occult_available(cls) -> CommonTestResult:
        """is_robot_occult_available()

        Determine if the Robot Occult is available.

        :return: The result of testing. True, if the Robot Occult is available.. False, if not.
        :rtype: CommonTestResult
        """
        if not hasattr(TraitType, 'ROBOT'):
            return CommonTestResult(False, reason='Robots do not exist. They are a myth! (At least in this game, possibly missing DLC or bugged Mods?)', tooltip_text=CommonStringId.S4CL_ROBOT_OCCULT_DOES_NOT_EXIST)
        if not CommonTraitUtils.is_trait_available(CommonTraitId.OCCULT_ROBOT):
            return CommonTestResult(False, reason='The Robot trait is not available.', tooltip_text=CommonStringId.S4CL_ROBOT_TRAIT_DOES_NOT_EXIST)
        return CommonTestResult.TRUE

    @classmethod
    def is_scarecrow_occult_available(cls) -> CommonTestResult:
        """is_scarecrow_occult_available()

        Determine if the Scarecrow Occult is available.

        :return: The result of testing. True, if the Scarecrow Occult is available.. False, if not.
        :rtype: CommonTestResult
        """
        if not CommonTraitUtils.is_trait_available(CommonTraitId.SCARECROW):
            return CommonTestResult(False, reason='Scarecrows do not exist. They are a myth! (At least in this game, possibly missing DLC or bugged Mods?)', tooltip_text=CommonStringId.S4CL_SCARECROW_OCCULT_DOES_NOT_EXIST)
        return CommonTestResult.TRUE

    @classmethod
    def is_skeleton_occult_available(cls) -> CommonTestResult:
        """is_skeleton_occult_available()

        Determine if the Skeleton Occult is available.

        :return: The result of testing. True, if the Skeleton Occult is available.. False, if not.
        :rtype: CommonTestResult
        """
        if not CommonTraitUtils.is_trait_available(CommonTraitId.HIDDEN_SKELETON):
            return CommonTestResult(False, reason='Skeletons do not exist. They are a myth! (At least in this game, possibly missing DLC or bugged Mods?)', tooltip_text=CommonStringId.S4CL_SKELETON_OCCULT_DOES_NOT_EXIST)
        return CommonTestResult.TRUE

    @classmethod
    def is_vampire_occult_available(cls) -> CommonTestResult:
        """is_vampire_occult_available()

        Determine if the Vampire Occult is available.

        :return: The result of testing. True, if the Vampire Occult is available.. False, if not.
        :rtype: CommonTestResult
        """
        if not hasattr(OccultType, 'VAMPIRE'):
            return CommonTestResult(False, reason='Vampires do not exist. They are a myth! (At least in this game, possibly missing DLC or bugged Mods?)', tooltip_text=CommonStringId.S4CL_VAMPIRE_OCCULT_DOES_NOT_EXIST)
        if not CommonTraitUtils.is_trait_available(CommonTraitId.OCCULT_VAMPIRE):
            return CommonTestResult(False, reason='The Vampire trait is not available.', tooltip_text=CommonStringId.S4CL_VAMPIRE_TRAIT_DOES_NOT_EXIST)
        return CommonTestResult.TRUE

    @classmethod
    def is_witch_occult_available(cls) -> CommonTestResult:
        """is_witch_occult_available()

        Determine if the Witch Occult is available.

        :return: The result of testing. True, if the Witch Occult is available.. False, if not.
        :rtype: CommonTestResult
        """
        if not hasattr(OccultType, 'WITCH'):
            return CommonTestResult(False, reason='Witches do not exist. They are a myth! (At least in this game, possibly missing DLC or bugged Mods?)', tooltip_text=CommonStringId.S4CL_WITCH_OCCULT_DOES_NOT_EXIST)
        if not CommonTraitUtils.is_trait_available(CommonTraitId.OCCULT_WITCH):
            return CommonTestResult(False, reason='The Witch trait is not available.', tooltip_text=CommonStringId.S4CL_WITCH_TRAIT_DOES_NOT_EXIST)
        return CommonTestResult.TRUE

    @classmethod
    def is_plant_sim_occult_available(cls) -> CommonTestResult:
        """is_plant_sim_occult_available()

        Determine if the Plant Sim Occult is available.

        :return: The result of testing. True, if the Plant Sim Occult is available.. False, if not.
        :rtype: CommonTestResult
        """
        if not CommonTraitUtils.is_trait_available(CommonTraitId.PLANT_SIM):
            return CommonTestResult(False, reason='Plant Sims do not exist. They are a myth! (At least in this game, possibly missing DLC or bugged Mods?)', tooltip_text=CommonStringId.S4CL_PLANT_OCCULT_DOES_NOT_EXIST)
        return CommonTestResult.TRUE

    @classmethod
    def is_werewolf_occult_available(cls) -> CommonTestResult:
        """is_werewolf_occult_available()

        Determine if the Werewolf Occult is available.

        :return: The result of testing. True, if the Werewolf Occult is available.. False, if not.
        :rtype: CommonTestResult
        """
        if not hasattr(OccultType, 'WEREWOLF'):
            return CommonTestResult(False, reason='Werewolves do not exist. They are a myth! (At least in this game, possibly missing DLC or bugged Mods?)', tooltip_text=CommonStringId.S4CL_WEREWOLF_OCCULT_DOES_NOT_EXIST)
        if not CommonTraitUtils.is_trait_available(CommonTraitId.OCCULT_WEREWOLF):
            return CommonTestResult(False, reason='The Werewolf trait is not available.', tooltip_text=CommonStringId.S4CL_WEREWOLF_TRAIT_DOES_NOT_EXIST)
        return CommonTestResult.TRUE

    @classmethod
    def is_ghost_occult_available(cls) -> CommonTestResult:
        """is_ghost_occult_available()

        Determine if the Ghost Occult is available.

        :return: The result of testing. True, if the Ghost Occult is available.. False, if not.
        :rtype: CommonTestResult
        """
        if not hasattr(TraitType, 'GHOST'):
            return CommonTestResult(False, reason='Ghosts do not exist. They are a myth! (At least in this game, possibly missing DLC or bugged Mods?)', tooltip_text=CommonStringId.S4CL_GHOST_OCCULT_DOES_NOT_EXIST)
        ghost_traits = (
            CommonTraitId.GHOST_ANGER,
            CommonTraitId.GHOST_ANIMAL_OBJECTS_KILLER_CHICKEN,
            CommonTraitId.GHOST_ANIMAL_OBJECTS_KILLER_RABBIT,
            CommonTraitId.GHOST_BEETLE,
            CommonTraitId.GHOST_CAULDRON_POTION_IMMORTALITY_FAILURE,
            CommonTraitId.GHOST_CLIMBING_ROUTE,
            CommonTraitId.GHOST_COW_PLANT,
            CommonTraitId.GHOST_CURSES_NIGHT_STALKER_STALKER,
            CommonTraitId.GHOST_DEATH_FLOWER,
            CommonTraitId.GHOST_DROWN,
            CommonTraitId.GHOST_ELDER_EXHAUSTION,
            CommonTraitId.GHOST_ELECTROCUTION,
            CommonTraitId.GHOST_EMBARRASSMENT,
            CommonTraitId.GHOST_FIRE,
            CommonTraitId.GHOST_FLIES,
            CommonTraitId.GHOST_FROZEN,
            CommonTraitId.GHOST_HUNGER,
            CommonTraitId.GHOST_LAUGHTER,
            CommonTraitId.GHOST_LIGHTNING,
            CommonTraitId.GHOST_MOTHER_PLANT,
            CommonTraitId.GHOST_MURPHY_BED,
            CommonTraitId.GHOST_OLD_AGE,
            CommonTraitId.GHOST_OVERHEAT,
            CommonTraitId.GHOST_POISON,
            CommonTraitId.GHOST_PUFFER_FISH,
            CommonTraitId.GHOST_RISEN,
            CommonTraitId.GHOST_RODENT_DISEASE,
            CommonTraitId.GHOST_SEANCE_TABLE,
            CommonTraitId.GHOST_STEAM,
            CommonTraitId.GHOST_VAMPIRE_SUN,
            CommonTraitId.GHOST_VENDING_MACHINE,
            CommonTraitId.GHOST_WITCH_OVERLOAD
        )
        for ghost_trait in ghost_traits:
            if CommonTraitUtils.is_trait_available(ghost_trait):
                return CommonTestResult.TRUE
        return CommonTestResult(False, reason='No Ghost traits were available.', tooltip_text=CommonStringId.S4CL_NO_GHOST_TRAITS_EXISTED)

    @classmethod
    def _get_occult_types(cls, sim_info: SimInfo) -> OccultType:
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
def _common_switch_sim_to_occult(output: CommonConsoleCommandOutput, occult_type: CommonOccultType, sim_info: SimInfo = None):
    if sim_info is None:
        return
    if occult_type is None:
        return
    occult_type_name = occult_type.name
    output(f'Attempting to switch Sim {sim_info} to their {occult_type_name} form.')
    result = CommonOccultUtils.switch_to_occult_form(sim_info, occult_type)
    if result:
        output(f'SUCCESS: Successfully switched Sim {sim_info} to their {occult_type_name} form: {result}')
    else:
        output(f'FAILED: Failed to switch Sim {sim_info} to their {occult_type_name} form: {result}')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.add_all_occults_to_sim',
    f'Add all Occult Types to a Sim. They will have all available Occult types added to them: {CommonOccultType.get_comma_separated_names_string(exclude_occult_types=(CommonOccultType.NON_OCCULT, CommonOccultType.GHOST, CommonOccultType.PLANT_SIM))}',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance Id or name of the Sim to add the occults to.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.addalloccultstosim',
        's4clib.add_all_occults',
        's4clib.addalloccults',
        's4clib.add_all_occults_type',
        's4clib.addalloccultstype',
    )
)
def _common_add_all_occults_to_sim(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    if sim_info is None:
        return
    output(f'Attempting to add all occults to Sim {sim_info}')
    result = CommonOccultUtils.add_all_occults(sim_info)
    if result:
        output(f'SUCCESS: Successfully added all occults to Sim {sim_info}: {result}')
    else:
        output(f'FAILED: Failed to add all occults to Sim {sim_info}: {result}')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.remove_all_occults_from_sim',
    f'Remove all Occult Types from a Sim. They will have all available Occult Types removed from them: {CommonOccultType.get_comma_separated_names_string(exclude_occult_types=(CommonOccultType.NON_OCCULT, CommonOccultType.GHOST, CommonOccultType.PLANT_SIM))}',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance Id or name of the Sim to remove the occults from.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib.removealloccultsfromsim',
        's4clib.remove_all_occults',
        's4clib.removealloccults',
        's4clib.remove_all_occults_type',
        's4clib.removealloccultstype',
    )
)
def _common_remove_all_occults_from_sim(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    if sim_info is None:
        return
    output(f'Attempting to remove all occults from Sim {sim_info}')
    result = CommonOccultUtils.remove_all_occults(sim_info)
    if result:
        output(f'SUCCESS: Successfully removeed all occults from Sim {sim_info}: {result}')
    else:
        output(f'FAILED: Failed to remove all occults from Sim {sim_info}: {result}')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.add_occult_to_sim',
    'Add an Occult Type to a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('occult_type', 'CommonOccultType', f'The name of an Occult Type to add to the Sim. Valid Values: {CommonOccultType.get_comma_separated_names_string(exclude_occult_types=(CommonOccultType.NON_OCCULT, CommonOccultType.GHOST))}'),
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
def _common_add_occult_to_sim(output: CommonConsoleCommandOutput, occult_type: CommonOccultType, sim_info: SimInfo = None):
    if sim_info is None:
        return
    if occult_type is None:
        return
    occult_type_name = occult_type.name
    output(f'Attempting to add occult {occult_type_name} to Sim {sim_info}')
    result = CommonOccultUtils.add_occult(sim_info, occult_type)
    if result:
        output(f'SUCCESS: Successfully added occult {occult_type_name} to Sim {sim_info}: {result}')
    else:
        output(f'FAILED: Failed to add occult {occult_type_name} to Sim {sim_info}: {result}')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.remove_occult_from_sim',
    'Remove an Occult Type from a Sim.',
    command_arguments=(
        CommonConsoleCommandArgument('occult_type', 'CommonOccultType', f'The name of an Occult Type to remove from the Sim. Valid Values: {CommonOccultType.get_comma_separated_names_string(exclude_occult_types=(CommonOccultType.NON_OCCULT, CommonOccultType.GHOST))}'),
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
def _common_remove_occult_from_sim(output: CommonConsoleCommandOutput, occult_type: CommonOccultType, sim_info: SimInfo = None):
    if sim_info is None:
        return
    if occult_type is None:
        return
    occult_type_name = occult_type.name
    output(f'Attempting to remove occult {occult_type_name} from Sim {sim_info}')
    result = CommonOccultUtils.remove_occult(sim_info, occult_type)
    if result:
        output(f'SUCCESS: Successfully removed occult {occult_type_name} from Sim {sim_info}: {result}')
    else:
        output(f'FAILED: Failed to remove occult {occult_type_name} from Sim {sim_info}: {result}')


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
def _common_remove_all_occults_from_sim(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
    if sim_info is None:
        return
    output(f'Attempting to remove all occult types from Sim {sim_info}.')
    result = CommonOccultUtils.remove_all_occults(sim_info)
    if result:
        output(f'SUCCESS: Successfully removed all occult types from Sim {sim_info}: {result}')
    else:
        output(f'FAILED: Failed to remove all occult types from Sim {sim_info}: {result}')


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_dev.print_vanilla_occults',
    'Print a list of all vanilla OccultType values a Sim has.',
    command_arguments=(
        CommonConsoleCommandArgument('sim_info', 'Sim Id or Name', 'The instance Id or name of the Sim to print the occult types of.', is_optional=True, default_value='Active Sim'),
    ),
    command_aliases=(
        's4clib_dev.printvanillaoccults',
    ),
    show_with_help_command=False
)
def _s4clib_testing_print_vanilla_occult_types_for_sim(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
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
def _common_print_occult_sim_infos(output: CommonConsoleCommandOutput, sim_info: SimInfo = None):
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
