"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Union, Any

from postures.posture import Posture
from postures.posture_state import PostureState
from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.common_posture_id import CommonPostureId
from sims4communitylib.enums.enumtypes.common_int import CommonInt
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.logging._has_s4cl_class_log import _HasS4CLClassLog
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimPostureUtils(_HasS4CLClassLog):
    """Utilities for managing the posture of Sims."""

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_sim_posture_utils'

    @classmethod
    def has_posture(cls, sim_info: SimInfo, posture: Union[int, CommonPostureId, Posture, CommonInt]) -> CommonTestResult:
        """has_posture(sim_info, posture)

        Determine if a Sim has a posture.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param posture: The identifier of the posture to check.
        :type posture: Union[int, CommonPostureId, Posture, CommonInt]
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return CommonTestResult(False, reason=f'Posture test failed because the {sim_info} is non-instantiated.', hide_tooltip=True)
        posture_instance = cls.load_posture_by_id(posture)
        if posture_instance is None:
            return CommonTestResult(False, reason=f'No posture was found with id.', hide_tooltip=True)
        for aspect in cls.get_posture_aspects(sim_info):
            if not posture_instance.multi_sim and aspect.posture_type is posture_instance:
                return CommonTestResult.TRUE
        return CommonTestResult(False, reason=f'{sim_info} does not have posture {posture_instance}.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_POSTURE, tooltip_tokens=(sim_info, str(posture_instance)))

    @classmethod
    def has_posture_with_sim(cls, sim_info: SimInfo, target_sim_info: SimInfo, posture: Union[int, CommonPostureId, Posture, CommonInt]) -> CommonTestResult:
        """has_posture_with_sim(sim_info, target_sim_info, posture)

        Determine if a Sim has a posture with another Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param target_sim_info: An instance of another Sim.
        :type target_sim_info: SimInfo
        :param posture: The identifier of the posture to check.
        :type posture: Union[int, CommonPostureId, Posture, CommonInt]
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return CommonTestResult(False, reason=f'Posture test failed because the {sim_info} is non-instantiated.', hide_tooltip=True)
        target_sim = CommonSimUtils.get_sim_instance(target_sim_info)
        if target_sim is None:
            return CommonTestResult(False, reason=f'Posture test failed because the {target_sim_info} is non-instantiated.', hide_tooltip=True)
        posture_instance = cls.load_posture_by_id(posture)
        if posture_instance is None:
            return CommonTestResult(False, reason=f'No posture was found with id.', hide_tooltip=True)
        for aspect in cls.get_posture_aspects(sim_info):
            if aspect.posture_type is posture_instance and (not posture_instance.multi_sim or aspect.linked_sim is target_sim):
                break
        return CommonTestResult(False, reason=f'{sim_info} does not have posture {posture_instance}.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_POSTURE, tooltip_tokens=(sim_info, str(posture_instance)))

    @classmethod
    def can_sim_be_picked_up(cls, sim_info: SimInfo) -> CommonTestResult:
        """can_be_picked_up(sim_info)

        Determine if a Sim can be picked up.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim can be picked up. False, it not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils
        from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
        if CommonSpeciesUtils.is_fox(sim_info) or CommonSpeciesUtils.is_small_dog(sim_info) or CommonSpeciesUtils.is_cat(sim_info):
            cls.get_log().format_with_message('Success, Sim is a fox, small dog, or cat and thus may be picked up.', sim=sim_info)
            return CommonTestResult.TRUE
        if CommonSpeciesUtils.is_animal(sim_info) and CommonAgeUtils.is_child(sim_info):
            cls.get_log().format_with_message('Success, Sim is a child animal and thus may be picked up.', sim=sim_info)
            return CommonTestResult.TRUE
        if CommonSpeciesUtils.is_human(sim_info) and (CommonAgeUtils.is_toddler(sim_info) or CommonAgeUtils.is_baby(sim_info)):
            cls.get_log().format_with_message('Success, Sim is a toddler or baby human and thus may be picked up.', sim=sim_info)
            return CommonTestResult.TRUE
        from sims4communitylib.enums.strings_enum import CommonStringId
        return CommonTestResult(False, reason=f'{sim_info} cannot be picked up.', tooltip_text=CommonStringId.S4CL_SIM_CANNOT_BE_PICKED_UP, tooltip_tokens=(sim_info,))

    @classmethod
    def is_on_container_supporting_posture(cls, sim_info: SimInfo, posture: Union[int, CommonPostureId, Posture, CommonInt]) -> CommonTestResult:
        """is_on_container_supporting_posture(sim_info, posture)

        Determine if the container a Sim is interacting with has a posture.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param posture: The identifier of the posture to check.
        :type posture: Union[int, CommonPostureId, Posture, CommonInt]
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return CommonTestResult(False, reason=f'Posture test failed because the {sim_info} is non-instantiated.', hide_tooltip=True)
        posture_instance = cls.load_posture_by_id(posture)
        if posture_instance is None:
            return CommonTestResult(False, reason=f'No posture was found with id.', hide_tooltip=True)
        container = cls.get_posture_target(sim_info)
        if container is None or not container.is_part:
            sim_posture = cls.get_posture(sim_info)
            return CommonTestResult(False, reason=f'Posture container for {sim_posture} is None or not a part', hide_tooltip=True)
        parts = {container}
        parts.update(container.get_overlapping_parts())
        for container_part in parts:
            if container_part.supports_posture_type(posture_instance):
                return CommonTestResult.TRUE
        return CommonTestResult(False, reason=f'Posture container {container} does not support Posture {posture_instance}', tooltip_text=CommonStringId.S4CL_POSTURE_CONTAINER_DOES_NOT_SUPPORT_POSTURE, tooltip_tokens=(str(container), str(posture_instance)))

    @classmethod
    def is_on_container_supporting_posture_with_sim(cls, sim_info: SimInfo, target_sim_info: SimInfo, posture: Union[int, CommonPostureId, Posture, CommonInt]) -> CommonTestResult:
        """is_on_container_supporting_posture(sim_info, target_sim_info, posture)

        Determine if the container a Sim is interacting with has a posture that supports another Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param target_sim_info: An instance of another Sim.
        :type target_sim_info: SimInfo
        :param posture: The identifier of the posture to check.
        :type posture: Union[int, CommonPostureId, Posture, CommonInt]
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return CommonTestResult(False, reason=f'Posture test failed because the {sim_info} is non-instantiated.', hide_tooltip=True)
        target_sim = CommonSimUtils.get_sim_instance(target_sim_info)
        if target_sim is None:
            return CommonTestResult(False, reason=f'Posture test failed because the {target_sim_info} is non-instantiated.', hide_tooltip=True)
        posture_instance = cls.load_posture_by_id(posture)
        if posture_instance is None:
            return CommonTestResult(False, reason=f'No posture was found with id.', hide_tooltip=True)
        container = cls.get_posture_target(sim_info)
        if container is None or not container.is_part:
            sim_posture = cls.get_posture(sim_info)
            return CommonTestResult(False, reason=f'Posture container for {sim_posture} is None or not a part', hide_tooltip=True)
        parts = {container}
        parts.update(container.get_overlapping_parts())
        if not any(container_parts.supports_posture_type(posture_instance) for container_parts in parts):
            return CommonTestResult(False, reason=f'Posture container {container} does not support {posture_instance}', tooltip_text=CommonStringId.S4CL_POSTURE_CONTAINER_DOES_NOT_SUPPORT_POSTURE, tooltip_tokens=(str(container), str(posture_instance)))
        if posture_instance.multi_sim:
            if target_sim is None:
                return CommonTestResult(False, reason=f'Posture test failed because the target is None', hide_tooltip=True)
            if target_sim is None:
                return CommonTestResult(False, reason=f'Posture test failed because the target is non-instantiated.', hide_tooltip=True)
            if not container.has_adjacent_part(target_sim):
                return CommonTestResult(False, reason=f'Posture container {container} requires an adjacent part for {target_sim} since {posture_instance} is multi-Sim', tooltip_text=CommonStringId.S4CL_POSTURE_CONTAINER_REQUIRES_AN_ADJACENT_PART_FOR_SIM_SINCE_POSTURE_IS_MULTI_SIM, tooltip_tokens=(str(container), target_sim_info, str(posture_instance)))
        return CommonTestResult.TRUE

    @classmethod
    def get_posture_target(cls, sim_info: SimInfo) -> Union[Any, None]:
        """get_posture_target(sim_info)

        Retrieve the target of the posture of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The target of the posture of a Sim.
        :rtype: Union[Any, None]
        """
        posture = cls.get_posture(sim_info)
        if posture is None:
            return None
        return posture.target

    @classmethod
    def get_posture(cls, sim_info: SimInfo) -> Union[Posture, None]:
        """get_posture(sim_info)

        Retrieve the posture of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The posture of a Sim.
        :rtype: Union[Posture, None]
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return None
        return sim.posture

    @classmethod
    def get_posture_aspects(cls, sim_info: SimInfo) -> Tuple[Posture]:
        """get_posture_aspects(sim_info)

        Retrieve the posture aspects of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The aspects of the posture of the Sim.
        :rtype: Tuple[Posture]
        """
        posture_state = cls.get_posture_state(sim_info)
        if posture_state is None:
            return tuple()
        return posture_state.aspects

    @classmethod
    def get_posture_state(cls, sim_info: SimInfo) -> Union[PostureState, None]:
        """get_posture_state(sim_info)

        Retrieve the posture aspects of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The posture state of a Sim.
        :rtype: Union[PostureState, None]
        """
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return None
        # noinspection PyPropertyAccess
        return sim.posture_state

    @classmethod
    def load_posture_by_id(cls, posture: Union[int, CommonPostureId, Posture, CommonInt]) -> Union[Posture, None]:
        """load_posture_by_id(posture)

        Load an instance of a Posture by its identifier.

        :param posture: The identifier of a Posture.
        :type posture: Union[int, CommonPostureId, Posture, CommonInt]
        :return: An instance of a Posture matching the decimal identifier or None if not found.
        :rtype: Union[Posture, None]
        """
        if isinstance(posture, Posture):
            return posture
        # noinspection PyBroadException
        try:
            # noinspection PyCallingNonCallable
            posture_instance = posture()
            if isinstance(posture_instance, Posture):
                # noinspection PyTypeChecker
                return posture
        except:
            pass
        # noinspection PyBroadException
        try:
            posture: int = int(posture)
        except:
            # noinspection PyTypeChecker
            posture: Posture = posture
            return posture

        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.POSTURE, posture)
