"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from business.business_manager import BusinessManager
from business.business_service import BusinessService


class CommonBusinessUtils:
    """Utilities for manipulating Businesses."""
    @classmethod
    def get_business_manager_for_current_zone(cls) -> BusinessManager:
        """get_business_manager_for_current_zone()

        Retrieve a Business Manager for the current Zone.

        :return: A Business Manager for the current zone.
        :rtype: BusinessManager
        """
        from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
        return cls.get_business_manager_by_zone_id(CommonLocationUtils.get_current_zone_id())

    @classmethod
    def get_business_manager_by_zone_id(cls, zone_id: int) -> BusinessManager:
        """get_business_manager_by_zone_id(zone_id)

        Retrieve a Business Manager for a Zone.

        :param zone_id: The identifier of the Zone to retrieve a Business Manager from.
        :type zone_id: int
        :return: A Business Manager for the specified zone.
        :rtype: BusinessManager
        """
        return cls.get_business_service().get_business_manager_for_zone(zone_id=zone_id)

    @classmethod
    def get_business_service(cls) -> BusinessService:
        """get_business_service()

        Retrieve an instance of the Business Service.

        :return: An instance of the Business Service.
        :rtype: BusinessService
        """
        import services
        return services.business_service()
