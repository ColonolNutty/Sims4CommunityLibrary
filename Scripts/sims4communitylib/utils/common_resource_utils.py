"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

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
    """ Utilities for retrieving the Tuning files and instances of various resources. (Objects, Snippets, Statistics, etc.) """
    @staticmethod
    def load_instance(instance_type: Types, instance_id: int) -> Any:
        """
            Load an instance of the specified type.

            Example Usage 1:
                mood_instance = CommonResourceUtils.load_instance(Types.MOOD, CommonMoodId.CONFIDENT)
                # This will retrieve an instance for the Confident mood and will be of type statistics.mood.Mood
            Example Usage 2:
                buff_instance = CommonResourceUtils.load_instance(Types.BUFF, CommonBuffId.WALK_STYLE_ANGRY)
                # This will retrieve an instance for the Walk Style Angry buff and will be of type buffs.buff.Buff
        :param instance_type: The type of instance being loaded.
        :param instance_id: The decimal identifier of an instance.
        :return: An instance of the specified type or None if no instance was found.
        """
        instance_manager = CommonResourceUtils.get_instance_manager(instance_type)
        return CommonResourceUtils.load_instance_from_manager(instance_manager, instance_id)

    @staticmethod
    def load_instance_from_manager(instance_manager: InstanceManager, instance_id: int) -> Any:
        """
            Load an instance from the specified InstanceManager.
        :param instance_manager: The InstanceManager an instance will be loaded from.
        :param instance_id: The decimal identifier of an instance.
        :return: An instance of the specified type or None if no instance was found.
        """
        return instance_manager.get(instance_id)

    @staticmethod
    def load_all_instances(instance_type: Types) -> ItemsView[Any, Any]:
        """
            Load all instances of the specified type.
        :param instance_type: The type of instance being loaded.
        :return: All instances of the specified type.
        """
        return CommonResourceUtils.get_instance_manager(instance_type).types.items()

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.MOD_NAME, fallback_return=None)
    def get_instance_manager(instance_manager_type: Types) -> Union[InstanceManager, None]:
        """
            Get an InstanceManager for the specified type.
        :param instance_manager_type: The type of InstanceManager to get.
        :return: An InstanceManager for the specified type, or None if no InstanceManager is found.
        """
        return services.get_instance_manager(instance_manager_type)

    @staticmethod
    def get_resource_key(resource_type: Types, instance_id: int) -> _resourceman.Key:
        """
            Retrieve the resource key of a resource in the format: 00000000:00000000:00000000000000000

            Possible Usages:
            - Retrieve the identifier of an Icon to display next to an Interaction in the Pie Menu.
            - Retrieve the identifier of an Image for display in Dialogs or Notifications.

            Example Usage:
            icon_key = CommonResourceUtils.get_resource_key(Types.PNG, 1234)
        :param resource_type: The type of resource being loaded.
        :param instance_id: The decimal identifier of the resource.
        :return: The resource key of an instance (format: 00000000(Type):00000000(Group):00000000000000000(Instance Guid)) or None if no instance was found.
        """
        return get_resource_key(instance_id, resource_type)

    @staticmethod
    def load_instances_with_any_tags(resource_type: Types, tags: Tuple[str]) -> Tuple[Any]:
        """
            Retrieve all resources that contain the specified tag names within their tuning file.

            Possible Usages:
            - Load all Snippet files containing properties with any of the specified tags.

        :param resource_type: The type of resource being loaded.
        :param tags: A collection of tag names to locate within a tuning file.
        :return: A collection of resources that contain any of the specified tags.
        """
        instances = []
        for (_, instance_class) in CommonResourceUtils.load_all_instances(resource_type):
            for tag in tags:
                if not hasattr(instance_class, tag):
                    continue
                instances.append(instance_class)
                break
        return tuple(instances)
