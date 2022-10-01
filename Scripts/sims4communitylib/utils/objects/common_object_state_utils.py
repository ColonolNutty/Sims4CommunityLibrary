"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Tuple, Dict

from event_testing.resolver import SingleObjectResolver
from event_testing.tests import TestSetInstance
from objects.components.state import StateComponent, ObjectStateValue, ObjectState
from objects.game_object import GameObject
from server_commands.argument_helpers import TunableInstanceParam
from sims4.resources import Types
from sims4communitylib.enums.common_object_state_ids import CommonObjectStateId
from sims4communitylib.enums.common_object_state_value_ids import CommonObjectStateValueId
from sims4communitylib.enums.common_object_quality import CommonObjectQuality
from sims4communitylib.enums.statistics_enum import CommonStatisticId
from sims4communitylib.enums.types.component_types import CommonComponentType
from sims4communitylib.logging._has_s4cl_class_log import _HasS4CLClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_component_utils import CommonComponentUtils
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from statistics.commodity import Commodity
from statistics.commodity_tracker import CommodityTracker


class CommonObjectStateUtils(_HasS4CLClassLog):
    """ Utilities for manipulating the state of Objects. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_object_state_utils'

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    @staticmethod
    def has_poor_quality(game_object: GameObject) -> bool:
        """has_poor_quality(game_object)

        Determine if an object has poor quality.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the specified Object has poor quality. False, if not.
        :rtype: bool
        """
        object_state = CommonObjectStateUtils.get_current_object_state(game_object, CommonObjectStateId.QUALITY)
        return CommonObjectStateUtils.get_object_state_value_guid(object_state) == CommonObjectStateValueId.QUALITY_POOR

    @staticmethod
    def has_normal_quality(game_object: GameObject) -> bool:
        """has_normal_quality(game_object)

        Determine if an object has normal quality.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the specified Object has normal quality. False, if not.
        :rtype: bool
        """
        object_state = CommonObjectStateUtils.get_current_object_state(game_object, CommonObjectStateId.QUALITY)
        return CommonObjectStateUtils.get_object_state_value_guid(object_state) == CommonObjectStateValueId.QUALITY_NORMAL

    @staticmethod
    def has_outstanding_quality(game_object: GameObject) -> bool:
        """has_outstanding_quality(game_object)

        Determine if an object has outstanding quality.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the specified Object has outstanding quality. False, if not.
        :rtype: bool
        """
        object_state = CommonObjectStateUtils.get_current_object_state(game_object, CommonObjectStateId.QUALITY)
        return CommonObjectStateUtils.get_object_state_value_guid(object_state) == CommonObjectStateValueId.QUALITY_OUTSTANDING

    @staticmethod
    def get_quality(game_object: GameObject) -> Union[CommonObjectQuality, None]:
        """get_quality(game_object)

        Retrieve the Quality of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: The CommonObjectQuality that represents the quality of the Object, or None if the quality could not be determined.
        :rtype: Union[CommonObjectQuality, None]
        """
        if CommonObjectStateUtils.has_poor_quality(game_object):
            return CommonObjectQuality.POOR
        if CommonObjectStateUtils.has_normal_quality(game_object):
            return CommonObjectQuality.NORMAL
        if CommonObjectStateUtils.has_outstanding_quality(game_object):
            return CommonObjectQuality.OUTSTANDING
        return None

    @staticmethod
    def get_quality_state(game_object: GameObject) -> Union[ObjectStateValue, None]:
        """get_quality_state(game_object)

        Retrieve the Quality State of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: The quality state of the Object or None when not found.
        :rtype: Union[ObjectStateValue, None]
        """
        return CommonObjectStateUtils.get_current_object_state(game_object, CommonObjectStateId.QUALITY)

    @staticmethod
    def set_quality(game_object: GameObject, quality: CommonObjectQuality) -> None:
        """set_quality(game_object, quality)

        Set the quality of an object.

        :param game_object: The object to modify.
        :type game_object: GameObject
        :param quality: The quality to set.
        :type quality: CommonObjectQuality
        """
        quality_state = CommonObjectStateUtils.convert_quality_to_object_state_value(quality)
        if quality_state is None:
            return None
        CommonObjectStateUtils.set_object_state(game_object, quality_state)

    @staticmethod
    def convert_quality_to_object_state_value(value: 'CommonObjectQuality') -> Union[ObjectStateValue, None]:
        """convert_quality_to_object_state_value(value)

        Convert CommonObjectQuality to an ObjectStateValue.

        :param value: The value to convert.
        :type value: CommonObjectQuality
        :return: The value translated to an ObjectStateValue, or None if the value could not be translated.
        :rtype: Union[ObjectStateValue, None]
        """
        if value is None:
            return None
        mapping: Dict[CommonObjectQuality, CommonObjectStateValueId] = {
            CommonObjectQuality.POOR: CommonObjectStateValueId.QUALITY_POOR,
            CommonObjectQuality.NORMAL: CommonObjectStateValueId.QUALITY_NORMAL,
            CommonObjectQuality.OUTSTANDING: CommonObjectStateValueId.QUALITY_OUTSTANDING,
        }
        quality_state_value_id = mapping.get(value, None)
        if quality_state_value_id is None:
            return None
        return CommonObjectStateUtils.load_object_state_value_by_id(quality_state_value_id)

    @staticmethod
    def convert_quality_from_object_state_value(value: ObjectStateValue) -> Union['CommonObjectQuality', None]:
        """convert_quality_from_object_state_value(value)

        Convert an ObjectStateValue to a matching CommonObjectQuality value.

        :param value: An instance of ObjectStateValue
        :type value: ObjectStateValue
        :return: The specified ObjectStateValue translated to CommonObjectQuality or None if the value could not be translated.
        :rtype: Union['CommonObjectQuality', None]
        """
        if value is None:
            return None
        if isinstance(value, CommonObjectQuality):
            return value
        mapping: Dict[int, CommonObjectQuality] = {
            CommonObjectStateValueId.QUALITY_POOR: CommonObjectQuality.POOR,
            CommonObjectStateValueId.QUALITY_NORMAL: CommonObjectQuality.NORMAL,
            CommonObjectStateValueId.QUALITY_OUTSTANDING: CommonObjectQuality.OUTSTANDING,
        }
        object_state_value_id = CommonObjectStateUtils.get_object_state_value_guid(value)
        return mapping.get(object_state_value_id, None)

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

    @classmethod
    def is_object_usable(cls, game_object: GameObject) -> bool:
        """is_object_usable(game_object)

        Determine if an Object is in a usable state.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: True, if the specified Object is in a usable state. False, if not.
        :rtype: bool
        """
        if game_object is None:
            return False
        state_component: StateComponent = cls.get_object_state_component(game_object)
        if state_component is None:
            return False
        return bool(state_component.is_object_usable)

    @classmethod
    def get_object_states(cls, game_object: GameObject) -> Tuple[ObjectStateValue]:
        """get_object_states(game_object)

        Retrieve the state values of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: A collection of ObjectStateValues.
        :rtype: Tuple[ObjectStateValue]
        """
        if game_object is None:
            return tuple()
        state_component: StateComponent = cls.get_object_state_component(game_object)
        if state_component is None:
            return tuple()
        return tuple(state_component.values())

    @classmethod
    def has_any_object_states(cls, game_object: GameObject, object_state_ids: Tuple[int]) -> bool:
        """has_any_object_states(game_object, object_state_ids)

        Determine if an Object has any of the specified object states.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param object_state_ids: A collection of decimal identifiers for object states.
        :type object_state_ids: Tuple[int]
        :return: True, if the object has any of the specified object states. False, if not.
        :rtype: bool
        """
        state_component: StateComponent = cls.get_object_state_component(game_object)
        if state_component is None:
            return False
        if not object_state_ids:
            return False
        for state_value in state_component.values():
            if CommonObjectStateUtils.get_object_state_value_guid(state_value) in object_state_ids:
                return True
        return False

    @classmethod
    def has_all_object_states(cls, game_object: GameObject, object_state_ids: Tuple[int]) -> bool:
        """has_all_object_states(game_object, object_state_ids)

        Determine if an Object has all of the specified object states.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param object_state_ids: A collection of decimal identifiers for object states.
        :type object_state_ids: Tuple[int]
        :return: True, if the object has all of the specified object states. False, if not.
        :rtype: bool
        """
        state_component: StateComponent = cls.get_object_state_component(game_object)
        if state_component is None:
            return False
        if not object_state_ids:
            return False
        for state_value in state_component.values():
            if CommonObjectStateUtils.get_object_state_value_guid(state_value) not in object_state_ids:
                return False
        return True

    @classmethod
    def get_object_state_guid(cls, object_state: ObjectState) -> Union[int, None]:
        """get_object_state_guid(object_state)

        Retrieve the GUID of an object state. (Not to be confused with the instance id)

        :param object_state: An instance of an object state.
        :type object_state: ObjectState
        :return: The GUID of the state or None if no identifier is found.
        :rtype: Union[int, None]
        """
        return cls.get_object_state_value_guid(object_state)

    @classmethod
    def get_object_state_value_guid(cls, object_state_value: ObjectStateValue) -> Union[int, None]:
        """get_object_state_value_guid(object_state_value)

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

    @classmethod
    def get_object_state_items(cls, game_object: GameObject) -> Dict[ObjectState, ObjectStateValue]:
        """get_object_state_items(game_object)

        Retrieve all Object States of an objects.

        :param game_object: The object to check.
        :type game_object: GameObject
        :return: A mapping of Object State to the current value of the object state.
        :rtype: Dict[ObjectState, ObjectStateValue]
        """
        # noinspection PyTypeChecker
        state_component: StateComponent = CommonObjectStateUtils.get_object_state_component(game_object)
        if state_component is None:
            cls.get_log().format_with_message('Object did not have a state component.', script_object=game_object)
            return dict()
        return state_component._states

    @classmethod
    def has_object_state(cls, game_object: GameObject, object_state_identifier: Union[int, CommonObjectStateId, CommonObjectStateValueId, ObjectState, ObjectStateValue]) -> bool:
        """has_object_state(game_object, object_state_identifier)

        Determine if an Object has an object state available.

        :param game_object: The Object to check.
        :type game_object: GameObject
        :param object_state_identifier: The identifier of the state to check.
        :type object_state_identifier: Union[int, CommonObjectStateId, CommonObjectStateValueId, ObjectState, ObjectStateValue]
        :return: True, if the Object has the specified object state as one of its available states (Not if the specified value is what the state on the object is set to). False, if not.
        :rtype: bool
        """
        if object_state_identifier is None:
            cls.get_log().format_with_message('Specified object state identifier was None.', game_object=game_object, object_state_identifier=object_state_identifier)
            return False
        object_states = cls.get_object_state_items(game_object)
        object_state = cls.load_object_state_by_id(object_state_identifier)
        object_state_value = cls.load_object_state_value_by_id(object_state_identifier)
        if object_state is None and object_state_value is not None:
            object_state = object_state_value.state
        else:
            object_state = object_state.state
        return object_state in object_states

    @classmethod
    def has_object_state_value(cls, game_object: GameObject, object_state_value_identifier: Union[int, CommonObjectStateValueId, ObjectStateValue]) -> bool:
        """has_object_state_value(game_object, object_state_value_identifier)

        Determine if an Object has a state set to an Object State Value

        :param game_object: The Object to check.
        :type game_object: GameObject
        :param object_state_value_identifier: The identifier of the object state value to check.
        :type object_state_value_identifier: Union[int, CommonObjectStateValueId, ObjectStateValue]
        :return: True, if the Object has the specified object state value set. False, if not.
        :rtype: bool
        """
        if object_state_value_identifier is None:
            cls.get_log().format_with_message('Specified object state value identifier was None.', game_object=game_object, object_state_value_identifier=object_state_value_identifier)
            return False
        # noinspection PyTypeChecker
        state_component: StateComponent = CommonObjectStateUtils.get_object_state_component(game_object)
        if state_component is None:
            cls.get_log().format_with_message('Object did not have a state component.', game_object=game_object, object_state_value_identifier=object_state_value_identifier)
            return False
        object_state_value = cls.load_object_state_value_by_id(object_state_value_identifier)
        if object_state_value is None:
            cls.get_log().format_with_message('Failed to locate object state value.', game_object=game_object, object_state_identifier=object_state_value_identifier)
            return False
        cls.get_log().format_with_message('Checking if object has state value.', target=game_object, state=object_state_value.state, state_value=object_state_value)
        state_value = cls.get_current_object_state(game_object, object_state_value.state)
        return cls.get_object_state_value_guid(state_value) == cls.get_object_state_value_guid(object_state_value)

    @classmethod
    def set_object_state(cls, game_object: GameObject, object_state_value: Union[int, CommonObjectStateValueId, ObjectStateValue]):
        """set_object_state(script_object, object_state)

        Set the object state of an Object.

        :param game_object: The Object to modify.
        :type game_object: GameObject
        :param object_state_value: The state to set.
        :type object_state_value: Union[int, CommonObjectStateValueId, ObjectStateValue]
        """
        if not cls.has_object_state(game_object, object_state_value):
            cls.get_log().format_with_message('Object did not have the required state.')
            return None
        # noinspection PyTypeChecker
        state_component: StateComponent = CommonObjectStateUtils.get_object_state_component(game_object)
        if state_component is None:
            cls.get_log().format_with_message('Object did not have a state component.', script_object=game_object, object_state=object_state_value)
            return
        object_state_value = cls.load_object_state_value_by_id(object_state_value)
        if object_state_value is None:
            cls.get_log().format_with_message('Failed to locate object state.', game_object=game_object, object_state_value=object_state_value)
            return
        cls.get_log().format_with_message('Setting state of object to value.', target=game_object, state=object_state_value.state, state_value=object_state_value)
        state_component.set_state(object_state_value.state, object_state_value)

    @classmethod
    def is_object_in_state(cls, game_object: GameObject, object_state_value: Union[int, CommonObjectStateValueId, ObjectStateValue]) -> bool:
        """is_object_in_state(game_object, object_state_value)

        Determine if an object is in a state.

        :param game_object: The object to check.
        :type game_object: GameObject
        :param object_state_value: The object state value to check.
        :type object_state_value: Union[int, CommonObjectStateValueId, ObjectStateValue]
        :return: True, if the state of an object has the specified object state value. False, if not.
        :rtype: bool
        """
        object_state_value = cls.load_object_state_value_by_id(object_state_value)
        if object_state_value is None:
            return False
        current_object_state_value = cls.get_current_object_state(game_object, object_state_value.state)
        if current_object_state_value is None:
            return False
        return current_object_state_value == object_state_value

    @classmethod
    def get_current_object_state(cls, game_object: GameObject, object_state: Union[int, CommonObjectStateId, ObjectState]) -> Union[ObjectStateValue, None]:
        """get_current_object_state(game_object, object_state)

        Get the value of a state on an Object.

        :param game_object: The Object to change.
        :type game_object: GameObject
        :param object_state: The state to use.
        :type object_state: Union[int, CommonObjectStateId, ObjectState]
        :return: The value of the specified state on an Object or None if a problem occurs.
        :rtype: Union[ObjectStateValue, None]
        """
        # noinspection PyTypeChecker
        state_component: StateComponent = CommonObjectStateUtils.get_object_state_component(game_object)
        if state_component is None:
            return None
        object_state = cls.load_object_state_by_id(object_state)
        if object_state is None:
            return None
        return state_component.get_state(object_state)

    @classmethod
    def load_object_state_by_id(cls, object_state: Union[int, CommonObjectStateId, ObjectState]) -> Union[ObjectState, None]:
        """load_object_state_by_id(object_state_value)

        Load an instance of an Object State by its identifier.

        :param object_state: The identifier of an Object State.
        :type object_state: Union[int, CommonObjectStateId, ObjectState]
        :return: An instance of an Object State Value matching the decimal identifier or None if not found.
        :rtype: Union[ObjectState, None]
        """
        if isinstance(object_state, ObjectStateValue):
            return object_state
        # noinspection PyBroadException
        try:
            object_state: int = int(object_state)
        except:
            # noinspection PyTypeChecker
            object_state: ObjectState = object_state
            return object_state

        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        result = CommonResourceUtils.load_instance(Types.OBJECT_STATE, object_state)
        return result

    @classmethod
    def load_object_state_value_by_id(cls, object_state_value: Union[int, CommonObjectStateValueId, ObjectStateValue]) -> Union[ObjectStateValue, None]:
        """load_object_state_value_by_id(object_state_value)

        Load an instance of an Object State Value by its identifier.

        :param object_state_value: The identifier of an Object State Value.
        :type object_state_value: Union[int, CommonObjectStateValueId, ObjectStateValue]
        :return: An instance of an Object State Value matching the decimal identifier or None if not found.
        :rtype: Union[ObjectStateValue, None]
        """
        if isinstance(object_state_value, ObjectStateValue):
            return object_state_value
        # noinspection PyBroadException
        try:
            object_state_value: int = int(object_state_value)
        except:
            # noinspection PyTypeChecker
            object_state_value: ObjectStateValue = object_state_value
            return object_state_value

        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        result = CommonResourceUtils.load_instance(Types.OBJECT_STATE, object_state_value)
        return result


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.print_object_states',
    'Print all states of an object.',
    command_arguments=(
        CommonConsoleCommandArgument('game_object', 'Obj Id', 'The object to check.'),
    )
)
def _common_print_object_states(output: CommonConsoleCommandOutput, game_object: GameObject) -> bool:
    log = CommonObjectStateUtils.get_log()
    try:
        log.enable()
        object_state_values_by_object_state = CommonObjectStateUtils.get_object_state_items(game_object)
        output(f'Printing game tags of {game_object}')
        log.debug(f'------------------Object states for {game_object}------------------')
        for (object_state, object_state_value) in object_state_values_by_object_state.items():
            object_state_value_guid = CommonObjectStateUtils.get_object_state_value_guid(object_state_value)
            log.debug(f'[{object_state}]: Current: {object_state_value} ({object_state_value_guid})')
            object_state: ObjectState = object_state
            log.debug(f'----------{object_state} Valid Values----------')
            for obj_state_value in object_state.values:
                obj_state_value_guid = CommonObjectStateUtils.get_object_state_value_guid(obj_state_value)
                log.debug(f'-- {obj_state_value} ({obj_state_value_guid})')
            log.debug('-------------------')
        log.debug('--------------------------------------------------------------------')
        output('Done')
        return True
    finally:
        log.disable()


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.set_object_state',
    'Set the state of an object.',
    command_arguments=(
        CommonConsoleCommandArgument('game_object', 'Obj Id', 'The object to set the state of.'),
        CommonConsoleCommandArgument('object_state', 'Object State Id Or Name', 'The state to set the object to.'),
    )
)
def _common_set_object_state(output: CommonConsoleCommandOutput, game_object: GameObject, object_state: TunableInstanceParam(Types.OBJECT_STATE)) -> bool:
    output('Setting object state.')
    if not CommonObjectStateUtils.has_object_state(game_object, object_state):
        output(f'Object {game_object} does not have state {object_state}.')
        return False
    CommonObjectStateUtils.set_object_state(game_object, object_state)
    output('Done setting object state.')
    return True


@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib.modify_object_state',
    'Modify the state of an object.',
    command_arguments=(
        CommonConsoleCommandArgument('game_object', 'Obj Id', 'The object to set the state of.'),
    )
)
def _common_modify_object_state(output: CommonConsoleCommandOutput, game_object: GameObject) -> bool:
    output(f'Opening dialog to modify object state of {game_object}.')
    from sims4communitylib.debug.dialogs.common_change_object_state_dialog import CommonChangeObjectStateDialog
    CommonChangeObjectStateDialog(game_object).open()
    return True
