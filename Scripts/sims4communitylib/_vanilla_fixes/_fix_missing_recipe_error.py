"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any
from objects.components.crafting_component import CraftingComponent
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils


# This error can happen when an object has been created that has multiple servings, is placed on the lot, and has its package file removed (The one that contains its recipe)
@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), CraftingComponent, CraftingComponent.component_super_affordances_gen.__name__)
def _common_fix_missing_recipe_error(original, self, **kwargs) -> Any:
    if self.get_recipe() is None:
        return
    result = original(self, **kwargs)
    if not result:
        return result
    yield from result
