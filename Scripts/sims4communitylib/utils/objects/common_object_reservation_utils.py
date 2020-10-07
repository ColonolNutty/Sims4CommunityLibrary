"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Tuple, List, Iterator

from objects.components.slot_component import SlotComponent
from objects.game_object import GameObject
from objects.part import Part
from objects.prop_object import BasicPropObject
from reservation.reservation_handler import _ReservationHandler
from reservation.reservation_result import ReservationResult
from sims.sim_info import SimInfo
from sims4communitylib.enums.common_slot_type import CommonSlotType
from sims4communitylib.enums.types.component_types import CommonComponentType
from sims4communitylib.utils.common_component_utils import CommonComponentUtils
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonObjectReservationUtils:
    """ Utilities for object reservations. """
    @staticmethod
    def is_in_use(game_object: GameObject) -> bool:
        """is_in_use(game_object)

        Determine if an Object is in use.

        :param game_object: An instance of an object.
        :type game_object: GameObject
        :return: True, if the object is in use. False, if not.
        :rtype: bool
        """
        if game_object is None:
            return False
        return game_object.self_or_part_in_use

    @staticmethod
    def is_in_use_by(game_object: GameObject, sim_info: SimInfo) -> bool:
        """is_in_use_by(game_object, sim_info)

        Determine if an Object is in use by the specified Sim.

        :param game_object: An instance of an object.
        :type game_object: GameObject
        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the object is in use by the specified Sim. False, if not.
        :rtype: bool
        """
        if game_object is None:
            return False
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return False
        return game_object.in_use_by(sim)

    @staticmethod
    def get_sims_using_object(game_object: GameObject) -> Tuple[SimInfo]:
        """get_sims_using_object(game_object)

        Retrieve a collection of Sims using the object.

        :param game_object: An instance of an object.
        :type game_object: GameObject
        :return: A collection of Sims using the object.
        :rtype: Tuple[SimInfo]
        """
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        if game_object is None:
            return tuple()
        sim_info_user_list: List[SimInfo] = []
        for sim in game_object.get_users(sims_only=True):
            sim_info_user_list.append(CommonSimUtils.get_sim_info(sim))
        return tuple(sim_info_user_list)

    @staticmethod
    def can_be_reserved_by(game_object: GameObject, sim_info: SimInfo) -> bool:
        """can_be_reserved_by(game_object, sim_info)

        Determine if an object can be reserved by the Sim.

        :param game_object: An instance of an object.
        :type game_object: GameObject
        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the object can be reserved. False, if not.
        :rtype: bool
        """
        reservation_sim_info_list = CommonObjectReservationUtils.get_sims_using_object(game_object)
        if len(reservation_sim_info_list) > 1:
            return False
        if len(reservation_sim_info_list) == 1 and sim_info not in reservation_sim_info_list:
            return False
        return True

    @staticmethod
    def has_all_free_slots(game_object: GameObject, slot_types: Iterator[CommonSlotType]=()) -> bool:
        """has_all_free_slots(game_object, slot_types=())

        Determine if an Object has all of the specified slots available for use.

        :param game_object: An instance of an object.
        :type game_object: GameObject
        :param slot_types: A collection of CommonSlotTypes. Default is an empty collection.
        :type slot_types: Tuple[CommonSlotTypes], optional
        :return: True, if all of the specified slots are free on the Object. False, if not.
        :rtype: bool
        """
        slot_types = tuple(slot_types)
        game_object = CommonObjectUtils.get_root_parent(game_object)
        slot_component: SlotComponent = CommonComponentUtils.get_component(game_object, CommonComponentType.SLOT)
        if slot_component is None:
            return True
        for runtime_slot in slot_component.get_runtime_slots_gen():
            if runtime_slot.empty:
                continue
            if not slot_types:
                return False
            if not runtime_slot.slot_types:
                continue
            for slot_type in runtime_slot.slot_types:
                if slot_type.__name__ in slot_types:
                    return False
        return True

    @staticmethod
    def begin_reservation(reservation_handler: _ReservationHandler) -> ReservationResult:
        """begin_reservation(reservation_handler)

        Begin reservation for the specified reservation handler.

        :param reservation_handler: The reservation handler to start.
        :type reservation_handler: _ReservationHandler
        :return: The result of beginning the reservation.
        :rtype: ReservationResult
        """
        if reservation_handler is None:
            return ReservationResult(False, 'No reservation handler specified.')
        result = reservation_handler.begin_reservation()
        if isinstance(result, bool):
            return ReservationResult(result, 'Failed to reserve the object for some reason.')
        return result

    @staticmethod
    def end_reservation(reservation_handler: _ReservationHandler) -> ReservationResult:
        """end_reservation(reservation_handler)

        End reservation for the specified reservation handler.

        :param reservation_handler: The reservation handler to end.
        :type reservation_handler: _ReservationHandler
        :return: The result of ending the reservation.
        :rtype: bool
        """
        if reservation_handler is None:
            return ReservationResult(False, 'No reservation handler specified.')
        return reservation_handler.end_reservation()

    @staticmethod
    def create_reservation_handler(
        object_instance: Union[GameObject, Part, BasicPropObject],
        sim_info: SimInfo,
        **kwargs
    ) -> Union[_ReservationHandler, None]:
        """create_reservation_handler(object_instance, sim_info, **kwargs)

        Create a reservation handler for a Sim to reserve an object.

        :param object_instance: An instance of an object.
        :type object_instance: Union[GameObject, Part, BasicPropObject]
        :param sim_info: An instance of a Sim. This Sim will be reserving the object.
        :type sim_info: SimInfo
        :param kwargs: Keyword arguments used when creating the reservation handler.
        :type kwargs: Any
        :return: An instance of a Reservation Handler or None if a problem occurs.
        :rtype: Union[_ReservationHandler, None]
        """
        if object_instance is None or sim_info is None:
            return None
        sim = CommonSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return None
        if not hasattr(object_instance, 'get_reservation_handler'):
            return None
        return object_instance.get_reservation_handler(sim, **kwargs)
