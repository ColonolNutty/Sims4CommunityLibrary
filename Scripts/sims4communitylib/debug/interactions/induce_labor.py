"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from interactions.context import InteractionContext
from sims.sim import Sim
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_pregnancy_utils import CommonSimPregnancyUtils
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils


class S4CLDebugInduceLaborInteraction(CommonImmediateSuperInteraction):
    """ Handle the interaction to Induce Labor. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cl_debug_induce_labor'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> CommonTestResult:
        if interaction_target is None or not CommonTypeUtils.is_sim_or_sim_info(interaction_target):
            cls.get_log().debug('Target is not a Sim.')
            return CommonTestResult.NONE
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        if not CommonSimPregnancyUtils.can_be_impregnated(target_sim_info):
            cls.get_log().format_with_message('Sim cannot be impregnated and thus cannot be pregnant.', target_sim=target_sim_info)
            return CommonTestResult.NONE
        if not hasattr(target_sim_info, 'pregnancy_tracker'):
            cls.get_log().format_with_message('Target does not have a pregnancy tracker.', target_sim=target_sim_info)
            return CommonTestResult.NONE
        cls.get_log().format_with_message('Checking if Sim is pregnant.', target_sim=target_sim_info)
        if not CommonSimPregnancyUtils.is_pregnant(target_sim_info):
            cls.get_log().format_with_message('Sim is not pregnant.', sim=target_sim_info)
            return CommonTestResult(False, reason=f'{target_sim_info} is not pregnant.', tooltip_text=CommonStringId.S4CL_SIM_IS_NOT_PREGNANT, tooltip_tokens=(target_sim_info,))
        cls.get_log().debug('Success.')
        return CommonTestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Sim) -> bool:
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        self.log.format_with_message('The baby wants out now! Labor induced in Sim.', target_sim=target_sim_info)
        CommonSimPregnancyUtils.induce_labor_in_sim(target_sim_info)
        return True
