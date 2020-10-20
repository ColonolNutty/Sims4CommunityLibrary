"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from event_testing.results import TestResult
from interactions.context import InteractionContext
from sims.sim import Sim
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_pregnancy_utils import CommonSimPregnancyUtils
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.sims.common_buff_utils import CommonBuffUtils


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
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> TestResult:
        cls.get_log().format_with_message('Running \'{}\' on_test.'.format(cls.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target, interaction_context=interaction_context, kwargles=kwargs)
        if interaction_target is None or not CommonTypeUtils.is_sim_or_sim_info(interaction_target):
            cls.get_log().debug('Target is not a Sim.')
            return TestResult.NONE
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        target_sim_name = CommonSimNameUtils.get_full_name(target_sim_info)
        if not CommonSimPregnancyUtils.can_be_impregnated(target_sim_info):
            cls.get_log().debug('\'{}\' cannot be impregnated and thus cannot be pregnant.')
            return TestResult.NONE
        if not hasattr(target_sim_info, 'pregnancy_tracker'):
            cls.get_log().debug('Target does not have a pregnancy tracker.')
            return TestResult.NONE
        cls.get_log().debug('Checking if \'{}\' is pregnant.'.format(target_sim_name))
        if not CommonSimPregnancyUtils.is_pregnant(target_sim_info):
            cls.get_log().format_with_message('\'{}\' is not pregnant.'.format(target_sim_name))
            return cls.create_test_result(False, reason='\'{}\' is not pregnant.'.format(target_sim_name), tooltip=CommonLocalizationUtils.create_localized_tooltip(CommonStringId.S4CL_SIM_IS_NOT_PREGNANT, tooltip_tokens=(target_sim_info, )))
        cls.get_log().debug('Success.')
        return TestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Sim) -> bool:
        self.log.format_with_message('Running \'{}\' on_started.'.format(self.__class__.__name__), interaction_sim=interaction_sim, interaction_target=interaction_target)
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        target_sim_name = CommonSimNameUtils.get_full_name(target_sim_info)
        buff_id = CommonSimPregnancyUtils.get_in_labor_buff(target_sim_info)
        if buff_id != -1:
            self.log.debug('The baby wants out now! Labor induced in \'{}\'. Chosen buff identifier: {}'.format(target_sim_name, str(buff_id)))
            return CommonBuffUtils.add_buff(target_sim_info, buff_id)
        self.log.debug('Failed to induce labor in \'{}\'.'.format(target_sim_name))
        return False
