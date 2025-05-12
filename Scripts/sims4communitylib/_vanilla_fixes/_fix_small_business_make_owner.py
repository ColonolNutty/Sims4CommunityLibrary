"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from business.business_enums import BusinessType
from business.business_tracker import BusinessTracker
from protocolbuffers import Business_pb2
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils

# This fix resolves the error that EA fails to check for business_data when creating a small business class. So it throws a "sim_id does not exist on NoneType" error inside SmallBusinessManager.__init__.


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), BusinessTracker, BusinessTracker.make_owner.__name__, handle_exceptions=False)
def _common_fix_small_business_make_owner(original, self: BusinessTracker, owner_household_id: int, business_zone_id: int, *_, from_load: bool = False, business_data=None, **__) -> Any:
    if hasattr(self, 'business_type') and self.business_type == BusinessType.SMALL_BUSINESS and business_data is None:
        business_data = Business_pb2.SetBusinessData()
    return original(self, owner_household_id, business_zone_id, *_, from_load=from_load, business_data=business_data, **__)
