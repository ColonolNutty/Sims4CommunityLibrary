"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple

from buffs.appearance_modifier.appearance_modifier import AppearanceModifier
from buffs.buff import Buff
from sims.sim_info import SimInfo
from sims4.tuning.tunable import TunableList, TunableTuple, TunableVariant, OptionalTunable
from sims4communitylib.classes.appearance_modifiers.common_attach_cas_parts_appearance_modifier import \
    CommonAttachCASPartsAppearanceModifier
from sims4communitylib.dtos.common_cas_part import CommonCASPart
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.cas.common_cas_utils import CommonCASUtils
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.utils.sims.common_gender_utils import CommonGenderUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
from tunable_multiplier import TunableMultiplier


class CommonExampleApplyBareFeetAppearanceModifier(AppearanceModifier):
    """An appearance modifier that applies bare feet to a Sim."""

    class CommonAttachBareFeetModifier(CommonAttachCASPartsAppearanceModifier):
        """Apply bare feet to a Sim."""
        # noinspection PyMissingOrEmptyDocstring
        @property
        def mod_identity(self) -> CommonModIdentity:
            return ModInfo.get_identity()

        # noinspection PyMissingOrEmptyDocstring
        @property
        def log_identifier(self) -> str:
            return 'common_example_apply_bare_feet'

        def _get_cas_parts(
            self,
            source_sim_info: SimInfo,
            modified_sim_info: SimInfo,
            original_unmodified_sim_info: SimInfo,
            random_seed: int
        ) -> Tuple[CommonCASPart]:
            # Human
            # yfShoes_Nude
            adult_human_female_bare_feet_id = 6543
            # ymShoes_Nude
            adult_human_male_bare_feet_id = 6563
            # cuShoes_Nude
            child_human_bare_feet_id = 22018
            # puShoes_Nude
            toddler_human_bare_feet_id = 132818

            # Dog
            # adShoes_Nude
            adult_large_dog_bare_feet_id = 125251
            # alShoes_Nude
            adult_small_dog_bare_feet_id = 148839
            # cdShoes_Nude
            child_dog_bare_feet_id = 158046

            # Cat
            # acShoes_Nude
            adult_cat_bare_feet_id = 150367
            # ccShoes_Nude
            child_cat_bare_feet_id = 164111

            # Fox
            adult_fox_bare_feet_id = 277492

            # Horse
            adult_horse_bare_feet_id = 337140
            child_horse_bare_feet_id = 343457

            bare_feet_cas_part_id = None
            if CommonAgeUtils.is_teen_adult_or_elder(original_unmodified_sim_info):
                if CommonSpeciesUtils.is_human(original_unmodified_sim_info):
                    if CommonGenderUtils.is_female(original_unmodified_sim_info):
                        bare_feet_cas_part_id = adult_human_female_bare_feet_id
                    elif CommonGenderUtils.is_male(original_unmodified_sim_info):
                        bare_feet_cas_part_id = adult_human_male_bare_feet_id
                elif CommonSpeciesUtils.is_large_dog(original_unmodified_sim_info):
                    bare_feet_cas_part_id = adult_large_dog_bare_feet_id
                elif CommonSpeciesUtils.is_small_dog(original_unmodified_sim_info):
                    bare_feet_cas_part_id = adult_small_dog_bare_feet_id
                elif CommonSpeciesUtils.is_cat(original_unmodified_sim_info):
                    bare_feet_cas_part_id = adult_cat_bare_feet_id
                elif CommonSpeciesUtils.is_fox(original_unmodified_sim_info):
                    bare_feet_cas_part_id = adult_fox_bare_feet_id
                elif CommonSpeciesUtils.is_horse(original_unmodified_sim_info):
                    bare_feet_cas_part_id = adult_horse_bare_feet_id
            elif CommonAgeUtils.is_child(original_unmodified_sim_info):
                if CommonSpeciesUtils.is_human(original_unmodified_sim_info):
                    bare_feet_cas_part_id = child_human_bare_feet_id
                elif CommonSpeciesUtils.is_large_dog(original_unmodified_sim_info) or CommonSpeciesUtils.is_small_dog(original_unmodified_sim_info):
                    bare_feet_cas_part_id = child_dog_bare_feet_id
                elif CommonSpeciesUtils.is_cat(original_unmodified_sim_info):
                    bare_feet_cas_part_id = child_cat_bare_feet_id
                elif CommonSpeciesUtils.is_horse(original_unmodified_sim_info):
                    bare_feet_cas_part_id = child_horse_bare_feet_id
            elif CommonAgeUtils.is_toddler(original_unmodified_sim_info):
                bare_feet_cas_part_id = toddler_human_bare_feet_id

            if bare_feet_cas_part_id is None:
                return tuple()

            return CommonCASPart(bare_feet_cas_part_id, CommonCASUtils.get_body_type_of_cas_part(bare_feet_cas_part_id)),

    # We override the original "appearance_modifiers" to so we can insert our custom appearance modifier.
    FACTORY_TUNABLES = {
        'appearance_modifiers': TunableList(
            description='\n            The specific appearance modifiers to use for this buff.\n            ',
            tunable=TunableList(
                description='\n                A tunable list of weighted modifiers. When applying modifiers\n                one of the modifiers in this list will be applied. The weight\n                will be used to run a weighted random selection.\n                ',
                tunable=TunableTuple(
                    description='\n                    A Modifier to apply and weight for the weighted random \n                    selection.\n                    ',
                    modifier=TunableVariant(
                        custom_bare_feet_modifier=CommonAttachBareFeetModifier.TunableFactory(),
                    ),
                    weight=TunableMultiplier.TunableFactory(
                        description='\n                        A weight with testable multipliers that is used to \n                        determine how likely this entry is to be picked when \n                        selecting randomly.\n                        '
                    )
                )
            )
        )
    }


# We use this buff in a Buff tuning and then apply the buff to the Sim.
class CommonExampleApplyBareFeetBuff(Buff):
    """A buff that applies bare feet to a Sim."""

    # We override the original "appearance_modifier" to so we can insert our custom appearance modifier.
    INSTANCE_TUNABLES = {
        'appearance_modifier': OptionalTunable(CommonExampleApplyBareFeetAppearanceModifier.TunableFactory()),
    }
