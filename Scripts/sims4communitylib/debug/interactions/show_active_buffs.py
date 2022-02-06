"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any, List

from distributor.shared_messages import IconInfoData
from interactions.context import InteractionContext
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.sims.common_buff_utils import CommonBuffUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class S4CLDebugShowActiveBuffsInteraction(CommonImmediateSuperInteraction):
    """S4CLDebugShowActiveBuffsInteraction(*_, **__)

    Show the currently active Buffs of a Sim.
    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cl_debug_show_active_buffs'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> CommonTestResult:
        if interaction_target is None or not CommonTypeUtils.is_sim_or_sim_info(interaction_target):
            cls.get_log().debug('Failed, Target is not a Sim.')
            return CommonTestResult.NONE
        cls.get_log().debug('Success, can show active Buffs.')
        return CommonTestResult.TRUE

    # noinspection PyMissingOrEmptyDocstring
    def on_started(self, interaction_sim: Sim, interaction_target: Sim) -> bool:
        target_sim_info = CommonSimUtils.get_sim_info(interaction_target)
        target_sim_name = CommonSimNameUtils.get_full_name(target_sim_info)
        sim_buff_strings: List[str] = list()
        for buff in CommonBuffUtils.get_buffs(target_sim_info):
            buff_name = CommonBuffUtils.get_buff_name(buff)
            buff_id = CommonBuffUtils.get_buff_id(buff)
            sim_buff_strings.append('{} ({})'.format(buff_name, buff_id))
        sim_buff_strings = sorted(sim_buff_strings, key=lambda x: x)
        sim_buffs = ', '.join(sim_buff_strings)
        text = ''
        text += 'Active Buffs:\n{}\n\n'.format(sim_buffs)
        self.log.enable()
        sim_buffs_for_log = ',\n'.join(sim_buff_strings)
        for_log_text = 'Active Buffs:\n{}\n\n'.format(sim_buffs_for_log)
        self.log.debug(f'{target_sim_name} ({CommonSimUtils.get_sim_id(target_sim_info)}): {for_log_text}')
        self.log.disable()
        CommonBasicNotification(
            CommonLocalizationUtils.create_localized_string('{} Active Buffs ({})'.format(target_sim_name, CommonSimUtils.get_sim_id(target_sim_info))),
            CommonLocalizationUtils.create_localized_string(text)
        ).show(
            icon=IconInfoData(obj_instance=interaction_target)
        )
        return True
