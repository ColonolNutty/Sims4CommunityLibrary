"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, Any

from sims4.resources import Types
from sims4.tuning.instance_manager import InstanceManager


class CommonInstanceManagerModificationHandler:
    """A modification handler that will modify an instance manager.

    """
    @classmethod
    def instance_manager_type(cls) -> Types:
        """The type of instances this handler modifies."""
        raise NotImplementedError()

    def should_apply_modifications(self, instance_manager: InstanceManager) -> bool:
        """should_apply_modifications(instance_manager)

        Whether or not this handler should apply its modifications to an Instance Manager.

        :param instance_manager: The instance manager to check.
        :type instance_manager: InstanceManager
        :return: True, if this handler should apply its modifications. False, if not.
        :rtype: bool
        """
        return self.__class__.instance_manager_type() == instance_manager.TYPE

    def apply_modifications(self, instance_manager: InstanceManager):
        """apply_modifications(instance_manager)

        Apply modifications to an Instance Manager.

        :param instance_manager: The instance manager to modify.
        :type instance_manager: InstanceManager
        """
        raise NotImplementedError()

    def _load_instances_from_manager(self, instance_manager: InstanceManager, instance_ids: Tuple[int]) -> Tuple[Any]:
        instances = list()
        for (key, cls) in tuple(instance_manager._tuned_classes.items()):
            if key.instance in instance_ids:
                instances.append(cls)
        return tuple(instances)
