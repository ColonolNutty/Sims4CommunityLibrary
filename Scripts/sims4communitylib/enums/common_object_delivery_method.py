"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonObjectDeliveryMethod(CommonInt):
    """A method of delivery for objects."""
    NONE: 'CommonObjectDeliveryMethod' = ...
    INVENTORY: 'CommonObjectDeliveryMethod' = ...
    # Sims 4 removed the ability to deliver items via the mail, so we'll fall back to inventory for now.
    MAIL: 'CommonObjectDeliveryMethod' = INVENTORY
