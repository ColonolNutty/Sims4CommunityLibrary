"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services
from io import BytesIO
from typing import ItemsView, Any, Union, Tuple, Type, ValuesView, Dict, TypeVar, List
try:
    from sims4.resources import ResourceLoader, Types
    from sims4.tuning.instance_manager import InstanceManager
    from sims4.tuning.merged_tuning_manager import get_manager
    from sims4.tuning.dynamic_enum import DynamicEnumLocked, DynamicEnum
    # noinspection PyUnresolvedReferences
    from sims4.tuning.serialization import ETreeTuningLoader
    from sims4.tuning.tunable_base import LoadingTags
except:
    # noinspection PyMissingOrEmptyDocstring
    class Types:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class ResourceLoader:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class InstanceManager:
        pass

    # noinspection PyMissingTypeHints,PyMissingOrEmptyDocstring
    def get_manager():
        pass

    # noinspection PyMissingOrEmptyDocstring
    class DynamicEnumLocked:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class DynamicEnum:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class ETreeTuningLoader:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class LoadingTags:
        pass

from sims4communitylib.classes.common_resource_key import CommonResourceKey
from sims4communitylib.enums.enumtypes.common_int import Int, CommonInt
from sims4communitylib.enums.enumtypes.common_int_flags import CommonIntFlags
from sims4communitylib.mod_support.mod_identity import CommonModIdentity

CommonEnumTypeValueType = TypeVar('CommonEnumTypeValueType', int, CommonInt, CommonIntFlags, Int, DynamicEnum, DynamicEnumLocked)

CommonExpectedReturnType = TypeVar('CommonExpectedReturnType', bound=Any)


class CommonResourceUtils:
    """Utilities for retrieving the Tuning files and instances of various resources. (Objects, Snippets, Statistics, etc.).

    """

    # noinspection PyUnusedLocal
    @staticmethod
    def load_instance(instance_type: Types, instance_id: int, return_type: Type[CommonExpectedReturnType] = Any) -> CommonExpectedReturnType:
        """load_instance(instance_type, instance_id, return_type=Any)

        Load an instance of the specified type.

        :Example Usage 1:

        .. highlight:: python
        .. code-block:: python

            # This will retrieve an instance for the Confident mood and will be of type statistics.mood.Mood
            mood_instance = CommonResourceUtils.load_instance(Types.MOOD, CommonMoodId.CONFIDENT)

        :Example Usage 2:

        .. highlight:: python
        .. code-block:: python

            # This will retrieve an instance for the Walk Style Angry buff and will be of type buffs.buff.Buff
            buff_instance = CommonResourceUtils.load_instance(Types.BUFF, CommonBuffId.WALK_STYLE_ANGRY)

        :param instance_type: The type of instance being loaded.
        :type instance_type: Types
        :param instance_id: The decimal identifier of an instance.
        :type instance_id: int
        :param return_type: The type of the returned value. (This is to make type hinting more accurate). It is not actually used in the function. Default is Any.
        :type return_type: Type[CommonExpectedReturnType], optional
        :return: An instance of the specified type or None if no instance was found.
        :rtype: Any
        """
        instance_manager = CommonResourceUtils.get_instance_manager(instance_type)
        return CommonResourceUtils.load_instance_from_manager(instance_manager, instance_id)

    # noinspection PyUnusedLocal
    @staticmethod
    def load_instance_from_manager(instance_manager: InstanceManager, instance_id: int, return_type: Type[CommonExpectedReturnType] = Any) -> CommonExpectedReturnType:
        """load_instance_from_manager(instance_manager, instance_id, return_type=Any)

        Load an instance from the specified InstanceManager.

        :param instance_manager: The InstanceManager an instance will be loaded from.
        :type instance_manager: InstanceManager
        :param instance_id: The decimal identifier of an instance.
        :type instance_id: int
        :param return_type: The type of the returned value. (This is to make type hinting more accurate). It is not actually used in the function. Default is Any.
        :type return_type: Type[CommonExpectedReturnType], optional
        :return: An instance of the specified type or None if no instance was found.
        :rtype: Any
        """
        return instance_manager.get(instance_id)

    # noinspection PyUnusedLocal
    @staticmethod
    def load_all_instances(instance_type: Types, return_type: Type[CommonExpectedReturnType] = Any) -> ItemsView[str, CommonExpectedReturnType]:
        """load_all_instances(instance_type, return_type=Any)

        Load all instances of the specified type.

        :param instance_type: The type of instances being loaded.
        :type instance_type: Types
        :param return_type: The type of the returned value. (This is to make type hinting more accurate). It is not actually used in the function. Default is Any.
        :type return_type: Type[CommonExpectedReturnType], optional
        :return: An items view of all instances of the specified type. (Resource Key, Instance)
        :rtype: ItemsView[str, Any]
        """
        return CommonResourceUtils.get_instance_manager(instance_type).types.items()

    # noinspection PyUnusedLocal
    @staticmethod
    def load_all_instances_as_guid_to_instance(instance_type: Types, return_type: Type[CommonExpectedReturnType] = Any) -> Dict[int, CommonExpectedReturnType]:
        """load_all_instances_as_guid_to_instance(instance_type, return_type=Any)

        Load all instances of the specified type and convert it to a dictionary mapping of GUID to Instance.

        :param instance_type: The type of instances being loaded.
        :type instance_type: Types
        :param return_type: The type of the returned value. (This is to make type hinting more accurate). It is not actually used in the function. Default is Any.
        :type return_type: Type[CommonExpectedReturnType], optional
        :return: A dictionary of instance GUID to instances of the specified type.
        :rtype: Dict[int, Any]
        """
        return dict([(value_key.instance, value) for (value_key, value) in CommonResourceUtils.load_all_instances(instance_type)])

    # noinspection PyUnusedLocal
    @staticmethod
    def load_all_instance_types(instance_type: Types, return_type: Type[CommonExpectedReturnType] = Any) -> Dict[str, CommonExpectedReturnType]:
        """load_all_instance_types(instance_type, return_type=Any)

        Load all instances of the specified type.

        :param instance_type: The type of instances being loaded.
        :type instance_type: Types
        :param return_type: The type of the returned value. (This is to make type hinting more accurate). It is not actually used in the function. Default is Any.
        :type return_type: Type[CommonExpectedReturnType], optional
        :return: A dictionary of resource keys to Instances of the specified type.
        :rtype: Dict[str, Any]
        """
        return CommonResourceUtils.get_instance_manager(instance_type).types

    # noinspection PyUnusedLocal
    @staticmethod
    def load_all_instance_values(instance_type: Types, return_type: Type[CommonExpectedReturnType] = Any) -> ValuesView[CommonExpectedReturnType]:
        """load_all_instance_values(instance_type, return_type=Any)

        Load all instance values of the specified type.

        :param instance_type: The type of instances being loaded.
        :type instance_type: Types
        :param return_type: The type of the returned value. (This is to make type hinting more accurate). It is not actually used in the function. Default is Any.
        :type return_type: Type[CommonExpectedReturnType], optional
        :return: All instance values of the specified type.
        :rtype: ValuesView[Any]
        """
        return CommonResourceUtils.get_instance_manager(instance_type).types.values()

    @staticmethod
    def get_instance_manager(instance_manager_type: Types) -> Union[InstanceManager, None]:
        """get_instance_manager(instance_manager_type)

        Get an InstanceManager for the specified type.

        :param instance_manager_type: The type of InstanceManager to get.
        :type instance_manager_type: Types
        :return: An InstanceManager for the specified type, or None if no InstanceManager is found.
        :rtype: Union[InstanceManager, None]
        """
        return services.get_instance_manager(instance_manager_type)

    @staticmethod
    def get_resource_key(resource_type: Types, resource_key: Union[int, str]) -> CommonResourceKey:
        """get_resource_key(resource_type, resource_key)

        Retrieve the resource key of a resource in the format: 00000000(Type):00000000(Group):00000000000000000(Instance Guid)

        .. note::

            Possible Usages:

            - Retrieve the identifier of an Icon to display next to an Interaction in the Pie Menu.
            - Retrieve the identifier of an Image for display in Dialogs or Notifications.

        :Example Usage:

        .. highlight:: python
        .. code-block:: python

            # This will retrieve the key for the image with identifier 1234
            icon_resource_key = CommonResourceUtils.get_resource_key(Types.PNG, 1234)

        :param resource_type: The type of resource being loaded.
        :type resource_type: Types
        :param resource_key: The decimal identifier or string resource key of the resource.
        :type resource_key: Union[int, str]
        :return: The resource key of an instance or None if no instance was found.
        :rtype: CommonResourceKey
        """
        from sims4.resources import get_resource_key, ResourceKeyWrapper
        key = get_resource_key(resource_key, resource_type)
        if isinstance(key, str) and ':' in key:
            # noinspection PyBroadException
            try:
                key = CommonResourceKey.from_resource_key(ResourceKeyWrapper(key))
                return key
            except:
                return key
        result = CommonResourceKey.from_resource_key(key)
        return result

    @staticmethod
    def load_instances_with_any_tags(resource_type: Types, tags: Tuple[str], return_type: Type[CommonExpectedReturnType] = Any) -> Tuple[CommonExpectedReturnType]:
        """load_instances_with_any_tags(resource_type, tags, return_type=Any)

        Retrieve all resources that contain the specified tag names within their tuning file.

        .. note::

            Possible Usages:

            - Load all Snippet files containing properties with any of the specified tags.

        :param resource_type: The type of resource being loaded.
        :type resource_type: Types
        :param tags: A collection of tag names to locate within a tuning file.
        :type tags: Tuple[str]
        :param return_type: The type of the returned value. (This is to make type hinting more accurate). It is not actually used in the function. Default is Any.
        :type return_type: Type[CommonExpectedReturnType], optional
        :return: A collection of resources that contain any of the specified tags.
        :rtype: Tuple[Any]
        """
        instances: List[CommonExpectedReturnType] = []
        for (_, instance_class) in CommonResourceUtils.load_all_instances(resource_type, return_type=return_type):
            for tag in tags:
                if not hasattr(instance_class, tag):
                    continue
                instances.append(instance_class)
                break
        return tuple(instances)

    @staticmethod
    def get_enum_by_name(name: str, enum_type: Type[CommonEnumTypeValueType], default_value: CommonEnumTypeValueType = None) -> CommonEnumTypeValueType:
        """get_enum_by_name(name, enum_type, default_value=None)

        Retrieve an enum value by its name.

        :param name: The name of the enum value to retrieve.
        :type name: str
        :param enum_type: The type of enum to retrieve.
        :type enum_type: Any
        :param default_value: The default value to return if an enum value was not found using the specified name. Default is None.
        :type default_value: Any, optional
        :return: The enum value with a name matching the specified name.
        :rtype: Any
        """
        if hasattr(enum_type, name):
            return getattr(enum_type, name)
        # noinspection PyBroadException
        try:
            # noinspection PyTypeChecker
            if name in enum_type:
                return enum_type[name]
        except:
            pass
        if hasattr(enum_type, 'name_to_value') and name in enum_type.name_to_value:
            return enum_type.name_to_value.get(name)
        return default_value

    @staticmethod
    def get_enum_by_int_value(value: int, enum_type: Type[CommonEnumTypeValueType], default_value: CommonEnumTypeValueType = None) -> CommonEnumTypeValueType:
        """get_enum_by_int_value(value, enum_type, default_value=None)

        Retrieve an enum value by its value.

        :param value: The integer value of the enum value to retrieve.
        :type value: int
        :param enum_type: The type of enum to retrieve.
        :type enum_type: Any
        :param default_value: The default value to return if an enum value was not found using the specified name. Default is None.
        :type default_value: Any, optional
        :return: The enum value with a value matching the specified value or the default value if not found.
        :rtype: Any
        """
        if hasattr(enum_type, 'value_to_name') and value in enum_type.value_to_name:
            return CommonResourceUtils.get_enum_by_name(enum_type.value_to_name[value], enum_type, default_value=default_value)
        return default_value

    @staticmethod
    def convert_str_to_fnv32(text: str, seed: int = 2166136261, high_bit: bool = True) -> int:
        """convert_str_to_fnv32(text, seed=2166136261, high_bit=True)

        Convert a text string into an FNV32 decimal identifier.

        :param text: The text to convert.
        :type text: str
        :param seed: A seed to use when converting. Default value is 2166136261.
        :type seed: int
        :param high_bit: If True, the high FNV bit will be returned. If False, a low FNV bit will be returned.
        :type high_bit: bool
        :return: The text converted to a FNV32 decimal identifier.
        :rtype: int
        """
        fnv_hash = CommonResourceUtils._str_to_fnv(text, seed, 16777619, 4294967296)
        if high_bit:
            fnv_hash |= 2147483648
        return fnv_hash

    @staticmethod
    def convert_str_to_fnv64(text: str, seed: int = 14695981039346656037, high_bit: bool = True) -> int:
        """convert_str_to_fnv64(text, seed=14695981039346656037, high_bit=True)

        Convert a text string into an FNV64 decimal identifier.

        :param text: The text to convert.
        :type text: str
        :param seed: A seed to use when converting. Default value is 14695981039346656037.
        :type seed: int
        :param high_bit: If True, a high bit version of the FNV bit will be returned. If False, a low bit version of the FNV bit will be returned.
        :type high_bit: bool
        :return: The text converted to an FNV64 decimal identifier.
        :rtype: int
        """
        fnv_hash = CommonResourceUtils._str_to_fnv(text, seed, 1099511628211, 18446744073709551616)
        if high_bit:
            fnv_hash |= 9223372036854775808
        return fnv_hash

    @staticmethod
    def register_tuning(mod_identity: CommonModIdentity, class_type: Type, tuning_type: Types, tuning_id: int, tuning_contents: str):
        """register_tuning(mod_identity, class_type, tuning_type, tuning_identifier, tuning_contents)

        Dynamically register a tuning instance.

        :param mod_identity: The identity of the mod registering the tuning.
        :type mod_identity: CommonModIdentity
        :param class_type: The type of class being registered.
        :type class_type: Type
        :param tuning_type: The type of tuning being registered.
        :type tuning_type: Types
        :param tuning_id: The decimal identifier of the tuning being registered.
        :type tuning_id: int
        :param tuning_contents: The xml contents of the tuning.
        :type tuning_contents: str
        """
        from sims4.resources import TYPE_RES_DICT
        tuning_instance_key = CommonResourceUtils.get_resource_key(tuning_type, tuning_id)
        # noinspection PyArgumentList
        tuning_loader = ETreeTuningLoader(class_type, '[{}] Dynamic Instance: {}'.format(mod_identity.name.replace(' ', '_'), class_type), loading_tag=LoadingTags.Instance)
        # noinspection PyUnresolvedReferences
        tuning_loader.feed(BytesIO(tuning_contents.encode('utf-8')))
        if tuning_instance_key.type in TYPE_RES_DICT:
            res_ext = TYPE_RES_DICT[tuning_instance_key.type]
            mtg = get_manager()
            # noinspection PyUnresolvedReferences
            mtg._tuning_resources[res_ext][tuning_instance_key.instance] = tuning_loader.root
        else:
            # noinspection PyUnresolvedReferences
            cls = tuning_loader.module
            tuning_manage = CommonResourceUtils.get_instance_manager(tuning_type)
            tuning_manage.register_tuned_class(cls, tuning_instance_key)

    @staticmethod
    def _str_to_fnv(text: str, seed: int, prime: int, size: int) -> int:
        string_bytes = text.lower().encode(encoding='utf-8')
        hash_value = seed
        for byte in string_bytes:
            hash_value = hash_value * prime % size
            hash_value = hash_value ^ byte
        return hash_value

    @staticmethod
    def load_resource_bytes(resource_key: CommonResourceKey, silent_fail: bool = True) -> BytesIO:
        """load_resource_bytes(resource_key, silent_fail=True)

        Retrieve the bytes of a resource.

        :param resource_key: The key of the resource.
        :type resource_key: CommonResourceKey
        :param silent_fail: Set to True to ignore errors if they occur. Set to False to throw errors when they occur. Default is True.
        :type silent_fail: bool, optional
        :return: An Input Output Byte reader/writer for the resource.
        :rtype: BytesIO
        """
        return ResourceLoader(resource_key).load(silent_fail=silent_fail)

    @staticmethod
    def load_resource_bytes_by_name(resource_type: Types, resource_name: str, has_fnv64_identifier: bool = True, has_high_bit_identifier: bool = False) -> Union[BytesIO, None]:
        """load_resource_bytes_by_name(resource_type, resource_name, fnv64=True, high_bit=False)

        Load the bytes of a resource into a Bytes Reader.

        .. note:: This function will only work if the instance key/decimal identifier of the resource equates to the name of the resource.

        :param resource_type: The type of resource being loaded.
        :type resource_type: Types
        :param resource_name: The tuning name of the resource.
        :type resource_name: str
        :param has_fnv64_identifier: Set to True to indicate the resource uses a 64 bit identifier. Set to False to indicate the resource uses a 32 bit identifier. Default is True.
        :type has_fnv64_identifier: bool, optional
        :param has_high_bit_identifier: Set to True to indicate the resource uses a high bit identifier. Set to False to indicate the resource uses a low bit identifier. Default is False.
        :type has_high_bit_identifier: bool, optional
        :return: An Input Output Byte reader/writer for the resource or None if a problem occurs.
        :rtype: Union[BytesIO, None]
        """
        conversion_func = CommonResourceUtils.convert_str_to_fnv32
        if has_fnv64_identifier:
            conversion_func = CommonResourceUtils.convert_str_to_fnv64
        resource_key = CommonResourceUtils.get_resource_key(resource_type, conversion_func(resource_name, high_bit=has_high_bit_identifier))
        if resource_key is None:
            return None
        return CommonResourceUtils.load_resource_bytes(resource_key)
