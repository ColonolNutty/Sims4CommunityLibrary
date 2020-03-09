"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
# noinspection PyUnresolvedReferences
import _resourceman
import services
from typing import ItemsView, Any, Union, Tuple
from sims4.resources import get_resource_key, Types
from sims4.tuning.instance_manager import InstanceManager
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo


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
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity(), fallback_return=None)
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
    def get_resource_key(resource_type: Types, instance_id: int) -> _resourceman.Key:
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
        :rtype: _resourceman.Key
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
