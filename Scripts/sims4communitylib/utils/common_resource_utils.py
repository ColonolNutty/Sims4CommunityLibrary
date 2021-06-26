"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import services
from io import BytesIO
from typing import ItemsView, Any, Union, Tuple
from sims4.resources import ResourceLoader, get_resource_key, Types
from sims4.tuning.instance_manager import InstanceManager
from sims4communitylib.classes.common_resource_key import CommonResourceKey


class CommonResourceUtils:
    """Utilities for retrieving the Tuning files and instances of various resources. (Objects, Snippets, Statistics, etc.).

    """
    @staticmethod
    def load_instance(instance_type: Types, instance_id: int) -> Any:
        """load_instance(instance_type, instance_id)

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
        :return: An instance of the specified type or None if no instance was found.
        :rtype: Any
        """
        instance_manager = CommonResourceUtils.get_instance_manager(instance_type)
        return CommonResourceUtils.load_instance_from_manager(instance_manager, instance_id)

    @staticmethod
    def load_instance_from_manager(instance_manager: InstanceManager, instance_id: int) -> Any:
        """load_instance_from_manager(instance_manager, instance_id)

        Load an instance from the specified InstanceManager.

        :param instance_manager: The InstanceManager an instance will be loaded from.
        :type instance_manager: InstanceManager
        :param instance_id: The decimal identifier of an instance.
        :type instance_id: int
        :return: An instance of the specified type or None if no instance was found.
        :rtype: Any
        """
        return instance_manager.get(instance_id)

    @staticmethod
    def load_all_instances(instance_type: Types) -> ItemsView[Any, Any]:
        """load_all_instances(instance_type)

        Load all instances of the specified type.

        :param instance_type: The type of instance being loaded.
        :type instance_type: Types
        :return: All instances of the specified type.
        :rtype: ItemsView[Any, Any]
        """
        return CommonResourceUtils.get_instance_manager(instance_type).types.items()

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
    def get_resource_key(resource_type: Types, instance_id: int) -> CommonResourceKey:
        """get_resource_key(resource_type, instance_id)

        Retrieve the resource key of a resource in the format: 00000000(Type):00000000(Group):00000000000000000(Instance Guid)

        .. note::

            Possible Usages:

            - Retrieve the identifier of an Icon to display next to an Interaction in the Pie Menu.
            - Retrieve the identifier of an Image for display in Dialogs or Notifications.

        :Example Usage:

        .. highlight:: python
        .. code-block:: python

            # This will retrieve the key for the image with identifier 1234
            icon_key = CommonResourceUtils.get_resource_key(Types.PNG, 1234)

        :param resource_type: The type of resource being loaded.
        :type resource_type: Types
        :param instance_id: The decimal identifier of the resource.
        :type instance_id: int
        :return: The resource key of an instance or None if no instance was found.
        :rtype: CommonResourceKey
        """
        return get_resource_key(instance_id, resource_type)

    @staticmethod
    def load_instances_with_any_tags(resource_type: Types, tags: Tuple[str]) -> Tuple[Any]:
        """load_instances_with_any_tags(resource_type, tags)

        Retrieve all resources that contain the specified tag names within their tuning file.

        .. note::

            Possible Usages:

            - Load all Snippet files containing properties with any of the specified tags.

        :param resource_type: The type of resource being loaded.
        :type resource_type: Types
        :param tags: A collection of tag names to locate within a tuning file.
        :type tags: Tuple[str]
        :return: A collection of resources that contain any of the specified tags.
        :rtype: Tuple[Any]
        """
        instances = []
        for (_, instance_class) in CommonResourceUtils.load_all_instances(resource_type):
            for tag in tags:
                if not hasattr(instance_class, tag):
                    continue
                instances.append(instance_class)
                break
        return tuple(instances)

    @staticmethod
    def get_enum_by_name(name: str, enum_type: Any, default_value: Any=None) -> Any:
        """get_enum_by_name(name, enum_type, default_value=None)

        Retrieve an enum value by its a name.

        :param name: The name of an outfit category.
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
        if name in enum_type:
            return enum_type[name]
        if hasattr(enum_type, 'name_to_value') and name in enum_type.name_to_value:
            return enum_type.name_to_value.get(name)
        return default_value

    @staticmethod
    def convert_str_to_fnv32(text: str, seed: int=2166136261, high_bit: bool=True) -> int:
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
    def convert_str_to_fnv64(text: str, seed: int=14695981039346656037, high_bit: bool=True) -> int:
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
    def _str_to_fnv(text: str, seed: int, prime: int, size: int) -> int:
        string_bytes = text.lower().encode(encoding='utf-8')
        hash_value = seed
        for byte in string_bytes:
            hash_value = hash_value * prime % size
            hash_value = hash_value ^ byte
        return hash_value

    @staticmethod
    def load_resource_bytes(resource_key: CommonResourceKey, silent_fail: bool=True) -> BytesIO:
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
    def load_resource_bytes_by_name(resource_type: Types, resource_name: str, has_fnv64_identifier: bool=True, has_high_bit_identifier: bool=False) -> Union[BytesIO, None]:
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
