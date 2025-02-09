"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Callable, Union

from rabbit_hole.rabbit_hole import RabbitHole
from services.rabbit_hole_service import RabbitHoleService
from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.sims.common_rabbit_hole_utils import CommonRabbitHoleUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimRabbitHoleUtils:
    """Utilities for manipulating Rabbit Holes for Sims."""
    @classmethod
    def get_first_rabbit_hole_id_for_sim(cls, sim_info: SimInfo) -> Union[int, None]:
        """get_rabbit_hole_id(sim_info)

        Retrieve the id of the rabbit hole a Sim is in.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The id of the first rabbit hole the Sim is in or None if not found.
        :rtype: Union[int, None]
        """
        sim_id = CommonSimUtils.get_sim_id(sim_info)
        rabbit_hole_service = CommonRabbitHoleUtils.get_rabbit_hole_service()
        rabbit_hole_id = rabbit_hole_service.get_head_rabbit_hole_id(sim_id)
        if rabbit_hole_id is None or rabbit_hole_id < 0:
            return None
        return rabbit_hole_id

    @classmethod
    def put_sim_into_rabbit_hole(cls, sim_info: SimInfo, rabbit_hole: Union[RabbitHole, int], on_exit_rabbit_hole_callback: Callable[[SimInfo, bool], None] = None) -> CommonTestResult:
        """put_sim_into_rabbit_hole(sim_info, rabbit_hole_identifier, on_exit_rabbit_hole_callback=None)

        Put a Sim into a Rabbit Hole.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param rabbit_hole: The identifier of a rabbit hole to put the Sim into.
        :type rabbit_hole: Union[RabbitHole, int]
        :param on_exit_rabbit_hole_callback: A callback invoked upon the Sim leaving the rabbit hole. Default is None.
        :type on_exit_rabbit_hole_callback: Callable[[SimInfo, bool], None]
        :return: A result indicating the success of putting the Sim into the rabbit hole.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        rabbit_hole_instance = CommonRabbitHoleUtils.load_rabbit_hole_by_id(rabbit_hole)
        if rabbit_hole_instance is None:
            return CommonTestResult(False, reason='RabbitHole was None.', hide_tooltip=True)

        sim_id = CommonSimUtils.get_sim_id(sim_info)
        existing_rabbit_hole_id = cls.get_first_rabbit_hole_id_for_sim(sim_info)
        if existing_rabbit_hole_id is not None:
            return CommonTestResult(False, reason=f'{sim_info} is already in a rabbit hole.', tooltip_text=CommonStringId.S4CL_SIM_IS_ALREADY_IN_A_RABBIT_HOLE, tooltip_tokens=(sim_info,))
        rabbit_hole_service = CommonRabbitHoleUtils.get_rabbit_hole_service()
        # noinspection PyTypeChecker
        rabbit_hole_id = rabbit_hole_service.put_sim_in_managed_rabbithole(sim_info, rabbit_hole_type=rabbit_hole_instance)

        if rabbit_hole_id is not None:
            if on_exit_rabbit_hole_callback is not None:
                def _on_exit_rabbit_hole(canceled: bool = False):
                    on_exit_rabbit_hole_callback(sim_info, canceled)
                    rabbit_hole_service.remove_rabbit_hole_expiration_callback(sim_id, rabbit_hole_id, _on_exit_rabbit_hole)

                rabbit_hole_service.set_rabbit_hole_expiration_callback(sim_id, rabbit_hole_id, _on_exit_rabbit_hole)
            return CommonTestResult.TRUE
        return CommonTestResult(False, reason=f'Failed to put {sim_info} into the rabbit hole.', tooltip_text=CommonStringId.S4CL_FAILED_TO_PUT_SIM_INTO_A_RABBIT_HOLE, tooltip_tokens=(sim_info,))

    @classmethod
    def try_remove_sim_from_rabbit_hole(cls, sim_info: SimInfo, on_remove_from_rabbit_hole_result_callback: Callable[[SimInfo, bool], None] = None) -> CommonTestResult:
        """try_remove_sim_from_rabbit_hole(sim_info, on_remove_from_rabbit_hole_result_callback=None)

        Remove a Sim from a rabbit hole.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param on_remove_from_rabbit_hole_result_callback: A callback invoked upon the Sim being removed from the rabbit hole. Default is None.
        :type on_remove_from_rabbit_hole_result_callback: Callable[[SimInfo, bool], None]
        :return: A result indicating the success of the removal.
        :rtype: CommonTestResult
        """
        if sim_info is None:
            raise AssertionError('Argument sim_info was None')
        existing_rabbit_hold_id = cls.get_first_rabbit_hole_id_for_sim(sim_info)
        if existing_rabbit_hold_id is None:
            return CommonTestResult.TRUE
        rabbit_hole_service: RabbitHoleService = CommonRabbitHoleUtils.get_rabbit_hole_service()

        def _remove_from_rabbit_hole_callback(result: bool):
            if on_remove_from_rabbit_hole_result_callback is not None:
                on_remove_from_rabbit_hole_result_callback(sim_info, result)

        sim_id = CommonSimUtils.get_sim_id(sim_info)
        rabbit_hole_service.try_remove_sim_from_rabbit_hole(sim_id, existing_rabbit_hold_id, callback=_remove_from_rabbit_hole_callback)
        return CommonTestResult.TRUE
