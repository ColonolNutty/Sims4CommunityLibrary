"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Tuple

from event_testing.resolver import SingleObjectResolver
from event_testing.tests import TestSetInstance
from objects.components.state import StateComponent, ObjectStateValue
from objects.game_object import GameObject
from sims4.resources import Types
from sims4communitylib.enums.statistics_enum import CommonStatisticId
from sims4communitylib.enums.types.component_types import CommonComponentType
from sims4communitylib.utils.common_component_utils import CommonComponentUtils
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from statistics.commodity import Commodity
from statistics.commodity_tracker import CommodityTracker


class CommonObjectStateUtils:
    """ Utilities for manipulating the state of Objects. """

    @staticmethod
    def can_become_broken(game_object: GameObject) -> bool:
        """can_become_broken(game_object)

        Determine if an Object is able to break.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the specified Object is able to break. False, if not.
        :rtype: bool
        """
        if game_object is None or not hasattr(game_object, 'commodity_tracker'):
            return False
        if CommonTypeUtils.is_sim_or_sim_info(game_object):
            return False
        commodity: Commodity = CommonResourceUtils.load_instance(Types.STATISTIC, int(CommonStatisticId.OBJECT_BROKENNESS))
        commodity_tracker: CommodityTracker = game_object.commodity_tracker
        if commodity_tracker is None:
            return False
        return commodity_tracker.has_statistic(commodity)

    @staticmethod
    def can_become_dirty(game_object: GameObject) -> bool:
        """can_become_dirty(game_object)

        Determine if an Object is able to get dirty.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the specified Object is able to get dirty. False, if not.
        :rtype: bool
        """
        if game_object is None or not hasattr(game_object, 'commodity_tracker'):
            return False
        if CommonTypeUtils.is_sim_or_sim_info(game_object):
            return False
        commodity: Commodity = CommonResourceUtils.load_instance(Types.STATISTIC, int(CommonStatisticId.DIRTINESS))
        commodity_tracker: CommodityTracker = game_object.commodity_tracker
        if commodity_tracker is None:
            return False
        return commodity_tracker.has_statistic(commodity)

    @staticmethod
    def is_broken(game_object: GameObject) -> bool:
        """is_broken(game_object)

        Determine if an Object is broken.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the specified Object is broken. False, if not.
        :rtype: bool
        """
        if game_object is None or not hasattr(game_object, 'commodity_tracker'):
            return False
        if CommonTypeUtils.is_sim_or_sim_info(game_object):
            return False
        # testSet_StateBroken
        test_set_instance: TestSetInstance = CommonResourceUtils.load_instance(Types.SNIPPET, 33738)
        # noinspection PyUnresolvedReferences
        tests: CompoundTestList = test_set_instance.test
        resolver = SingleObjectResolver(game_object)
        result = tests.run_tests(resolver)
        return bool(result)

    @staticmethod
    def is_dirty(game_object: GameObject) -> bool:
        """is_dirty(game_object)

        Determine if an Object is dirty.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the specified Object is dirty. False, if not.
        :rtype: bool
        """
        if game_object is None or not hasattr(game_object, 'commodity_tracker'):
            return False
        commodity: Commodity = CommonResourceUtils.load_instance(Types.STATISTIC, int(CommonStatisticId.DIRTINESS))
        commodity_tracker: CommodityTracker = game_object.commodity_tracker
        if commodity_tracker is None:
            return False
        if not commodity_tracker.has_statistic(commodity):
            return False
        return commodity_tracker.get_value(commodity) == commodity.min_value

    @staticmethod
    def break_object(game_object: GameObject) -> bool:
        """break_object(game_object)

        Break an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the specified Object has been broken. False, if not.
        :rtype: bool
        """
        if game_object is None or not hasattr(game_object, 'commodity_tracker'):
            return False
        commodity: Commodity = CommonResourceUtils.load_instance(Types.STATISTIC, int(CommonStatisticId.OBJECT_BROKENNESS))
        commodity_tracker: CommodityTracker = game_object.commodity_tracker
        if commodity_tracker is None:
            return False
        if not commodity_tracker.has_statistic(commodity):
            return False
        return commodity_tracker.set_min(commodity)

    @staticmethod
    def fix_object(game_object: GameObject) -> bool:
        """fix_object(game_object)

        Fix an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the specified Object has been fixed. False, if not.
        :rtype: bool
        """
        if game_object is None or not hasattr(game_object, 'commodity_tracker'):
            return False
        commodity: Commodity = CommonResourceUtils.load_instance(Types.STATISTIC, int(CommonStatisticId.OBJECT_BROKENNESS))
        commodity_tracker: CommodityTracker = game_object.commodity_tracker
        if commodity_tracker is None:
            return False
        if not commodity_tracker.has_statistic(commodity):
            return False
        return commodity_tracker.set_max(commodity)

    @staticmethod
    def make_dirty(game_object: GameObject) -> bool:
        """make_dirty(game_object)

        Make an Object dirty.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the specified Object has been made dirty. False, if not.
        :rtype: bool
        """
        if game_object is None or not hasattr(game_object, 'commodity_tracker'):
            return False
        commodity: Commodity = CommonResourceUtils.load_instance(Types.STATISTIC, int(CommonStatisticId.DIRTINESS))
        commodity_tracker: CommodityTracker = game_object.commodity_tracker
        if commodity_tracker is None:
            return False
        if not commodity_tracker.has_statistic(commodity):
            return False
        return commodity_tracker.set_min(commodity)

    @staticmethod
    def make_clean(game_object: GameObject) -> bool:
        """make_clean(game_object)

        Make an Object clean.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the specified Object has been made clean. False, if not.
        :rtype: bool
        """
        if game_object is None or not hasattr(game_object, 'commodity_tracker'):
            return False
        commodity: Commodity = CommonResourceUtils.load_instance(Types.STATISTIC, int(CommonStatisticId.DIRTINESS))
        commodity_tracker: CommodityTracker = game_object.commodity_tracker
        if commodity_tracker is None:
            return False
        if not commodity_tracker.has_statistic(commodity):
            return False
        return commodity_tracker.set_max(commodity)

    @staticmethod
    def is_object_usable(game_object: GameObject) -> bool:
        """is_object_usable(game_object)

        Determine if an Object is in a usable state.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the specified Object is in a usable state. False, if not.
        :rtype: bool
        """
        if game_object is None:
            return False
        state_component: StateComponent = CommonComponentUtils.get_component(game_object, CommonComponentType.STATE)
        if state_component is None:
            return False
        return state_component.is_object_usable

    @staticmethod
    def get_object_states(game_object: GameObject) -> Tuple[ObjectStateValue]:
        """get_object_states(game_object)

        Retrieve the state values of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: A collection of ObjectStateValues.
        :rtype: Tuple[ObjectStateValue]
        """
        if game_object is None:
            return tuple()
        state_component: StateComponent = CommonComponentUtils.get_component(game_object, CommonComponentType.STATE)
        if state_component is None:
            return tuple()
        return tuple(state_component.values())

    @staticmethod
    def has_any_object_states(game_object: GameObject, object_state_ids: Tuple[int]) -> bool:
        """has_any_object_states(game_object, object_state_ids)

        Determine if an Object has any of the specified object states.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param object_state_ids: A collection of decimal identifiers for object states.
        :type object_state_ids: Tuple[int]
        :return: True, if the object has any of the specified object states. False, if not.
        :rtype: bool
        """
        state_component: StateComponent = CommonComponentUtils.get_component(game_object, CommonComponentType.STATE)
        if state_component is None:
            return False
        if not object_state_ids:
            return False
        for state_value in state_component.values():
            if CommonObjectStateUtils.get_object_state_value_guid(state_value) in object_state_ids:
                return True
        return False

    @staticmethod
    def has_all_object_states(game_object: GameObject, object_state_ids: Tuple[int]) -> bool:
        """has_all_object_states(game_object, object_state_ids)

        Determine if an Object has all of the specified object states.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param object_state_ids: A collection of decimal identifiers for object states.
        :type object_state_ids: Tuple[int]
        :return: True, if the object has all of the specified object states. False, if not.
        :rtype: bool
        """
        state_component: StateComponent = CommonComponentUtils.get_component(game_object, CommonComponentType.STATE)
        if state_component is None:
            return False
        if not object_state_ids:
            return False
        for state_value in state_component.values():
            if CommonObjectStateUtils.get_object_state_value_guid(state_value) not in object_state_ids:
                return False
        return True

    @staticmethod
    def get_object_state_value_guid(object_state_value: ObjectStateValue) -> Union[int, None]:
        """get_object_state_value_guid(state_value)

        Retrieve the GUID of an object state. (Not to be confused with the instance id)

        :param object_state_value: An instance of an object state.
        :type object_state_value: ObjectStateValue
        :return: The GUID of the state value or None if no identifier is found.
        :rtype: Union[int, None]
        """
        if object_state_value is None:
            return None
        return getattr(object_state_value, 'guid64', None)

    @staticmethod
    def get_object_state_component(game_object: GameObject) -> Union[StateComponent, None]:
        """get_object_state_component(game_object)

        Retrieve the State Component of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: The State Component of the specified Object or None if no state component is found.
        :rtype: Union[StateComponent, None]
        """
        if game_object is None:
            return None
        return CommonComponentUtils.get_component(game_object, CommonComponentType.STATE)
