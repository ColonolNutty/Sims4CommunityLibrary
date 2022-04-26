"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4.resources import Types
from sims4.tuning.instance_manager import InstanceManager
from typing import Tuple

from sims4communitylib.classes.mixins.common_affordance_lists_mixin import \
    CommonAffordanceListsMixin
from sims4communitylib.classes.mixins.common_interactions_mixin import \
    CommonInteractionsMixin
from sims4communitylib.services.resources.modification_handlers.common_instance_manager_modification_handler import \
    CommonInstanceManagerModificationHandler


class CommonAddInteractionsToAffordanceListsModificationHandler(CommonInstanceManagerModificationHandler, CommonInteractionsMixin, CommonAffordanceListsMixin):
    """A handler that will add interactions to affordance lists."""

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def instance_manager_type(cls) -> Types:
        return Types.SNIPPET

    # noinspection PyMissingOrEmptyDocstring
    @property
    def interaction_ids(self) -> Tuple[int]:
        raise NotImplementedError()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def affordance_list_ids(self) -> Tuple[int]:
        raise NotImplementedError()

    def __init__(self, *_, **__) -> None:
        super().__init__(*_, **__)
        CommonInteractionsMixin.__init__(self)
        CommonAffordanceListsMixin.__init__(self)

    # noinspection PyMissingOrEmptyDocstring
    def apply_modifications(self, instance_manager: InstanceManager):
        instances = self._load_instances_from_manager(instance_manager, self.affordance_list_ids)
        for instance in instances:
            new_interactions = list()
            for interaction_instance_to_add in self._interaction_instances_gen():
                if interaction_instance_to_add in instance.value:
                    continue
                new_interactions.append(interaction_instance_to_add)
            if not new_interactions:
                continue
            instance.value += tuple(new_interactions)
