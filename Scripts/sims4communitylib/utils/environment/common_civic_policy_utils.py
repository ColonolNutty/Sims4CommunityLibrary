"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Tuple

from civic_policies.base_civic_policy import BaseCivicPolicy
from civic_policies.street_civic_policy import StreetCivicPolicy
from civic_policies.street_civic_policy_provider import StreetProvider
from sims4communitylib.enums.common_civic_policy_status_type import CommonCivicPolicyStatusType
from sims4communitylib.enums.common_street_civic_policy_ids import CommonStreetCivicPolicyId
from sims4communitylib.enums.common_venue_civic_policy_ids import CommonVenueCivicPolicyId
from sims4communitylib.logging._has_s4cl_class_log import _HasS4CLClassLog
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
from venues.civic_policies.venue_civic_policy import VenueCivicPolicy
from venues.civic_policies.venue_civic_policy_provider import VenueCivicPolicyProvider


class CommonCivicPolicyUtils(_HasS4CLClassLog):
    """Utilities for manipulating civic policies."""

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_civic_policy_utils'

    @classmethod
    def is_free_love_enacted(cls) -> bool:
        """is_free_love_enacted()

        Determine if the Free Love civic policy has been enacted in the current zone.

        :return: True, if the policy is enacted. False, if not.
        :rtype: bool
        """
        return cls.is_policy_enacted_in_current_zone(CommonStreetCivicPolicyId.SKILL_BASED_FREE_LOVE)

    @classmethod
    def is_policy_enacted_in_zone(cls, zone_id: int, policy: Union[int, CommonVenueCivicPolicyId, CommonStreetCivicPolicyId, BaseCivicPolicy]) -> bool:
        """is_policy_enacted_in_zone(zone_id, policy)

        Determine if a Policy is currently enacted in a Zone.

        :param zone_id: The identifier of the Zone to check.
        :type zone_id: int
        :param policy: The policy to look for.
        :type policy: Union[int, CommonVenueCivicPolicyId, CommonStreetCivicPolicyId, BaseCivicPolicy]
        :return: True, if the specified policy is currently enacted in a Zone. False, if not.
        :rtype: bool
        """
        return cls.is_policy_in_zone(zone_id, policy, CommonCivicPolicyStatusType.ENACTED)

    @classmethod
    def is_policy_balloted_in_zone(cls, zone_id: int, policy: Union[int, CommonVenueCivicPolicyId, CommonStreetCivicPolicyId, BaseCivicPolicy]) -> bool:
        """is_policy_balloted_in_zone(zone_id, policy)

        Determine if a Policy is currently balloted in a Zone.

        :param zone_id: The identifier of the Zone to check.
        :type zone_id: int
        :param policy: The policy to look for.
        :type policy: Union[int, CommonVenueCivicPolicyId, CommonStreetCivicPolicyId, BaseCivicPolicy]
        :return: True, if the specified policy is currently balloted in a Zone. False, if not.
        :rtype: bool
        """
        return cls.is_policy_in_zone(zone_id, policy, CommonCivicPolicyStatusType.BALLOTED)

    @classmethod
    def is_policy_up_for_repeal_in_zone(cls, zone_id: int, policy: Union[int, CommonVenueCivicPolicyId, CommonStreetCivicPolicyId, BaseCivicPolicy]) -> bool:
        """is_up_for_repeal_in_zone(zone_id, policy)

        Determine if a Policy is currently up for repeal in a Zone.

        :param zone_id: The identifier of the Zone to check.
        :type zone_id: int
        :param policy: The policy to look for.
        :type policy: Union[int, CommonVenueCivicPolicyId, CommonStreetCivicPolicyId, BaseCivicPolicy]
        :return: True, if the specified policy is currently up for repeal in a Zone. False, if not.
        :rtype: bool
        """
        return cls.is_policy_in_zone(zone_id, policy, CommonCivicPolicyStatusType.UP_FOR_REPEAL)

    @classmethod
    def is_dormant_in_zone(cls, zone_id: int, policy: Union[int, CommonVenueCivicPolicyId, CommonStreetCivicPolicyId, BaseCivicPolicy]) -> bool:
        """is_dormant_in_zone(zone_id, policy)

        Determine if a Policy is currently up for repeal in a Zone.

        :param zone_id: The identifier of the Zone to check.
        :type zone_id: int
        :param policy: The policy to look for.
        :type policy: Union[int, CommonVenueCivicPolicyId, CommonStreetCivicPolicyId, BaseCivicPolicy]
        :return: True, if the specified policy is currently up for repeal in a Zone. False, if not.
        :rtype: bool
        """
        return cls.is_policy_in_zone(zone_id, policy, CommonCivicPolicyStatusType.DORMANT)

    @classmethod
    def is_policy_enacted_in_current_zone(cls, policy: Union[int, CommonVenueCivicPolicyId, CommonStreetCivicPolicyId, BaseCivicPolicy]) -> bool:
        """is_policy_enacted_in_current_zone(policy)

        Determine if a Policy is currently enacted in the current Zone.

        :param policy: The policy to look for.
        :type policy: Union[int, CommonVenueCivicPolicyId, CommonStreetCivicPolicyId, BaseCivicPolicy]
        :return: True, if the specified policy is currently enacted in the current Zone. False, if not.
        :rtype: bool
        """
        return cls.is_policy_in_zone(CommonLocationUtils.get_current_zone_id(), policy, CommonCivicPolicyStatusType.ENACTED)

    @classmethod
    def is_policy_balloted_in_current_zone(cls, policy: Union[int, CommonVenueCivicPolicyId, CommonStreetCivicPolicyId, BaseCivicPolicy]) -> bool:
        """is_policy_balloted_in_current_zone(policy)

        Determine if a Policy is currently balloted in the current Zone.

        :param policy: The policy to look for.
        :type policy: Union[int, CommonVenueCivicPolicyId, CommonStreetCivicPolicyId, BaseCivicPolicy]
        :return: True, if the specified policy is currently balloted in the current Zone. False, if not.
        :rtype: bool
        """
        return cls.is_policy_in_zone(CommonLocationUtils.get_current_zone_id(), policy, CommonCivicPolicyStatusType.BALLOTED)

    @classmethod
    def is_policy_up_for_repeal_in_current_zone(cls, policy: Union[int, CommonVenueCivicPolicyId, CommonStreetCivicPolicyId, BaseCivicPolicy]) -> bool:
        """is_up_for_repeal_in_current_zone(policy)

        Determine if a Policy is currently up for repeal in the current Zone.

        :param policy: The policy to look for.
        :type policy: Union[int, CommonVenueCivicPolicyId, CommonStreetCivicPolicyId, BaseCivicPolicy]
        :return: True, if the specified policy is currently up for repeal in the current Zone. False, if not.
        :rtype: bool
        """
        return cls.is_policy_in_zone(CommonLocationUtils.get_current_zone_id(), policy, CommonCivicPolicyStatusType.UP_FOR_REPEAL)

    @classmethod
    def is_dormant_in_current_zone(cls, policy: Union[int, CommonVenueCivicPolicyId, CommonStreetCivicPolicyId, BaseCivicPolicy]) -> bool:
        """is_dormant_in_current_zone(policy)

        Determine if a Policy is currently up for repeal in the current Zone.

        :param policy: The policy to look for.
        :type policy: Union[int, CommonVenueCivicPolicyId, CommonStreetCivicPolicyId, BaseCivicPolicy]
        :return: True, if the specified policy is currently up for repeal in the current Zone. False, if not.
        :rtype: bool
        """
        return cls.is_policy_in_zone(CommonLocationUtils.get_current_zone_id(), policy, CommonCivicPolicyStatusType.DORMANT)

    @classmethod
    def is_policy_in_zone(cls, zone_id: int, policy: Union[int, CommonVenueCivicPolicyId, CommonStreetCivicPolicyId, BaseCivicPolicy], policy_status: CommonCivicPolicyStatusType) -> bool:
        """is_policy_in_current_zone(zone_id, policy, policy_status)

        Determine if a Policy has a specific Status in a Zone.

        :param zone_id: The identifier of the Zone to check.
        :type zone_id: int
        :param policy: The policy to look for.
        :type policy: Union[int, CommonVenueCivicPolicyId, CommonStreetCivicPolicyId, BaseCivicPolicy]
        :param policy_status: The status of the policies to check.
        :type policy_status: CommonCivicPolicyStatusType
        :return: True, if the specified policy has the specified status in a Zone. False, if not.
        :rtype: bool
        """
        policy = cls.load_civic_policy_by_id(policy)
        if policy is None:
            return False
        if isinstance(policy, StreetCivicPolicy):
            policies = cls.get_street_civic_policies_by_zone_id(zone_id, policy_status)
        elif isinstance(policy, VenueCivicPolicy):
            policies = cls.get_venue_civic_policies_by_zone_id(zone_id, policy_status)
        else:
            return False
        return policy in policies

    @classmethod
    def is_policy_in_current_zone(cls, policy: Union[int, CommonVenueCivicPolicyId, CommonStreetCivicPolicyId, BaseCivicPolicy], policy_status: CommonCivicPolicyStatusType) -> bool:
        """is_policy_in_current_zone(policy, policy_status)

        Determine if a Policy has a specific Status in the current Zone.

        :param policy: The policy to look for.
        :type policy: Union[int, CommonVenueCivicPolicyId, CommonStreetCivicPolicyId, BaseCivicPolicy]
        :param policy_status: The status of the policies to check.
        :type policy_status: CommonCivicPolicyStatusType
        :return: True, if the specified policy has the specified status in the current Zone. False, if not.
        :rtype: bool
        """
        return cls.is_policy_in_zone(CommonLocationUtils.get_current_zone_id(), policy, policy_status)

    @classmethod
    def get_street_civic_policies_by_zone_id(cls, zone_id: int, policy_status: CommonCivicPolicyStatusType) -> Tuple[StreetCivicPolicy]:
        """get_street_civic_policies_by_zone_id(zone_id, policy_status)

        Retrieve Street Civic Policies with the specifies status from the specified zone.

        :param zone_id: The identifier of the Zone to retrieve the civic policies from.
        :type zone_id: int
        :param policy_status: The status of the policies to look for.
        :type policy_status: CommonCivicPolicyStatusType
        :return: A collection of Street Civic Policies with the specified status from the specified zone.
        :rtype: Tuple[StreetCivicPolicy]
        """
        provider = CommonCivicPolicyUtils.get_street_civic_policy_provider_by_zone_id(zone_id)
        if provider is None:
            return tuple()
        if policy_status == CommonCivicPolicyStatusType.ENACTED:
            return provider.get_enacted_policies()
        if policy_status == CommonCivicPolicyStatusType.BALLOTED:
            return provider.get_balloted_policies()
        if policy_status == CommonCivicPolicyStatusType.UP_FOR_REPEAL:
            return provider.get_up_for_repeal_policies()
        if policy_status == CommonCivicPolicyStatusType.DORMANT:
            return provider.get_dormant_policies()
        return tuple()

    @classmethod
    def get_street_civic_policies_in_current_zone(cls, policy_status: CommonCivicPolicyStatusType) -> Tuple[StreetCivicPolicy]:
        """get_street_civic_policies_in_current_zone(policy_status)

        Retrieve Street Civic Policies with the specifies status from the current zone.

        :param policy_status: The status of the policies to look for.
        :type policy_status: CommonCivicPolicyStatusType
        :return: A collection of Street Civic Policies with the specified status from the current zone.
        :rtype: Tuple[StreetCivicPolicy]
        """
        return cls.get_street_civic_policies_by_zone_id(CommonLocationUtils.get_current_zone_id(), policy_status)

    @classmethod
    def get_street_civic_policy_provider_for_current_zone(cls) -> Union[StreetProvider, None]:
        """get_street_civic_policy_provider_for_current_zone(zone_id)

        Retrieve the Street Civic Policy Provider for the current Zone.

        :return: The Street Civic Policy Provider for the current Zone or None if the street service is unavailable or there is no street for the current Zone.
        :rtype: Union[StreetProvider, None]
        """
        return cls.get_street_civic_policy_provider_by_zone_id(CommonLocationUtils.get_current_zone_id())

    @classmethod
    def get_street_civic_policy_provider_by_world_id(cls, world_id: int) -> Union[StreetProvider, None]:
        """get_street_civic_policy_provider_by_world_id(zone_id)

        Retrieve the Street Civic Policy Provider for a World.

        :param world_id: The identifier of the World to retrieve the civic policy provider from.
        :type world_id: int
        :return: The Street Civic Policy Provider for the specified World or None if the street service is unavailable or there is no street for the specified World.
        :rtype: Union[StreetProvider, None]
        """
        street_service = CommonLocationUtils.get_street_service()
        if street_service is None:
            return None
        street = CommonLocationUtils.get_street_by_world_id(world_id)
        if street is None:
            return None
        return street_service.get_provider(street)

    @classmethod
    def get_street_civic_policy_provider_by_zone_id(cls, zone_id: int) -> Union[StreetProvider, None]:
        """get_street_civic_policy_provider_by_zone_id(zone_id)

        Retrieve the Street Civic Policy Provider for a Zone.

        :param zone_id: The identifier of the Zone to retrieve the civic policy provider from.
        :type zone_id: int
        :return: The Street Civic Policy Provider for the specified Zone or None if the street service is unavailable or there is no street for the specified Zone.
        :rtype: Union[StreetProvider, None]
        """
        street_service = CommonLocationUtils.get_street_service()
        if street_service is None:
            return None
        street = CommonLocationUtils.get_street_by_zone_id(zone_id)
        if street is None:
            return None
        return street_service.get_provider(street)

    @classmethod
    def get_venue_civic_policies_by_zone_id(cls, zone_id: int, policy_status: CommonCivicPolicyStatusType) -> Tuple[VenueCivicPolicy]:
        """get_venue_civic_policies_by_zone_id(zone_id, policy_status)

        Retrieve Venue Civic Policies with the specifies status from the specified zone.

        :param zone_id: The identifier of the Zone to retrieve the civic policies from.
        :type zone_id: int
        :param policy_status: The status of the policies to look for.
        :type policy_status: CommonCivicPolicyStatusType
        :return: A collection of Venue Civic Policies with the specified status from the specified zone.
        :rtype: Tuple[VenueCivicPolicy]
        """
        provider = CommonCivicPolicyUtils.get_venue_civic_policy_provider_by_zone_id(zone_id)
        if provider is None:
            return tuple()
        if policy_status == CommonCivicPolicyStatusType.ENACTED:
            return provider.get_enacted_policies()
        if policy_status == CommonCivicPolicyStatusType.BALLOTED:
            return provider.get_balloted_policies()
        if policy_status == CommonCivicPolicyStatusType.UP_FOR_REPEAL:
            return provider.get_up_for_repeal_policies()
        if policy_status == CommonCivicPolicyStatusType.DORMANT:
            return provider.get_dormant_policies()
        return tuple()

    @classmethod
    def get_venue_civic_policies_in_current_zone(cls, policy_status: CommonCivicPolicyStatusType) -> Tuple[VenueCivicPolicy]:
        """get_venue_civic_policies_in_current_zone(policy_status)

        Retrieve Venue Civic Policies with the specifies status from the current zone.

        :param policy_status: The status of the policies to look for.
        :type policy_status: CommonCivicPolicyStatusType
        :return: A collection of Venue Civic Policies with the specified status from the current zone.
        :rtype: Tuple[VenueCivicPolicy]
        """
        return cls.get_venue_civic_policies_by_zone_id(CommonLocationUtils.get_current_zone_id(), policy_status)

    @classmethod
    def get_venue_civic_policy_provider_for_current_zone(cls) -> Union[VenueCivicPolicyProvider, None]:
        """get_venue_civic_policy_provider_for_current_zone()

        Retrieve the Venue Civic Policy Provider for a Zone.

        :return: The Venue Civic Policy Provider for the current Zone or None if the current Zone does not have a venue.
        :rtype: Union[VenueCivicPolicyProvider, None]
        """
        return cls.get_venue_civic_policy_provider_by_zone_id(CommonLocationUtils.get_current_zone_id())

    @classmethod
    def get_venue_civic_policy_provider_by_zone_id(cls, zone_id: int) -> Union[VenueCivicPolicyProvider, None]:
        """get_venue_civic_policy_provider_by_zone_id(zone_id)

        Retrieve the Venue Civic Policy Provider for a Zone.

        :param zone_id: The identifier of the Zone to retrieve the civic policy provider from.
        :type zone_id: int
        :return: The Venue Civic Policy Provider for the specified Zone or None if the specified Zone does not have a venue.
        :rtype: Union[VenueCivicPolicyProvider, None]
        """
        venue = CommonLocationUtils.get_venue_by_zone_id(zone_id)
        if venue is None:
            return None
        return venue.civic_policy_provider

    @classmethod
    def load_civic_policy_by_id(cls, policy: Union[int, CommonVenueCivicPolicyId, CommonStreetCivicPolicyId, BaseCivicPolicy]) -> Union[BaseCivicPolicy, None]:
        """load_civic_policy_by_id(policy)

        Load an instance of a Civic Policy by its identifier.

        :param policy: The identifier of a Civic Policy.
        :type policy: Union[int, CommonVenueCivicPolicyId, CommonStreetCivicPolicyId, BaseCivicPolicy]
        :return: An instance of a Civic Policy matching the decimal identifier or None if not found.
        :rtype: Union[BaseCivicPolicy, None]
        """
        if isinstance(policy, BaseCivicPolicy):
            return policy
        # noinspection PyBroadException
        try:
            # noinspection PyCallingNonCallable
            policy_instance = policy()
            if isinstance(policy_instance, BaseCivicPolicy):
                # noinspection PyTypeChecker
                return policy
        except:
            pass
        # noinspection PyBroadException
        try:
            policy: int = int(policy)
        except:
            # noinspection PyTypeChecker
            policy: BaseCivicPolicy = policy
            return policy

        from sims4.resources import Types
        from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
        return CommonResourceUtils.load_instance(Types.SNIPPET, policy)


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.print_enacted_street_policies', 'Print a list of enacted policies.')
def _common_print_street_civic_policies(output: CommonConsoleCommandOutput, policy_status: CommonCivicPolicyStatusType):
    log = CommonCivicPolicyUtils.get_log()
    try:
        log.enable()
        provider = CommonCivicPolicyUtils.get_street_civic_policy_provider_for_current_zone()
        policies = provider.get_enacted_policies(tuning=True)
        output(f'------------{policy_status.name} Street Civic Policies------------')
        log.debug(f'------------{policy_status.name} Street Civic Policies------------')
        for policy in policies:
            output(f'Policy: {policy}')
            log.format_with_message(f'Policy: {policy}')
        output('------------------------------------------------------')
        log.debug('------------------------------------------------------')
    finally:
        log.disable()


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.print_enacted_street_policies', 'Print a list of enacted policies.')
def _common_print_enacted_street_policies(output: CommonConsoleCommandOutput):
    log = CommonCivicPolicyUtils.get_log()
    try:
        log.enable()
        provider = CommonCivicPolicyUtils.get_street_civic_policy_provider_for_current_zone()
        policies = provider.get_enacted_policies(tuning=True)
        output('------------Enacted Street Civic Policies------------')
        log.debug('------------Enacted Street Civic Policies------------')
        for policy in policies:
            output(f'Policy: {policy}')
            log.format_with_message(f'Policy: {policy}')
        output('------------------------------------------------------')
        log.debug('------------------------------------------------------')
    finally:
        log.disable()


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.print_balloted_street_policies', 'Print a list of balloted policies.')
def _common_print_balloted_street_policies(output: CommonConsoleCommandOutput):
    log = CommonCivicPolicyUtils.get_log()
    try:
        log.enable()
        provider = CommonCivicPolicyUtils.get_street_civic_policy_provider_for_current_zone()
        policies = provider.get_balloted_policies(tuning=True)
        output('------------Balloted Street Civic Policies------------')
        log.debug('------------Balloted Street Civic Policies------------')
        for policy in policies:
            output(f'Policy: {policy}')
            log.format_with_message(f'Policy: {policy}')
        output('------------------------------------------------------')
        log.debug('------------------------------------------------------')
    finally:
        log.disable()


@CommonConsoleCommand(ModInfo.get_identity(), 's4clib.print_dormant_street_policies', 'Print a list of dormant policies.')
def _common_print_dormant_street_policies(output: CommonConsoleCommandOutput):
    log = CommonCivicPolicyUtils.get_log()
    try:
        log.enable()
        provider = CommonCivicPolicyUtils.get_street_civic_policy_provider_for_current_zone()
        policies = provider.get_dormant_policies(tuning=True)
        output('------------Dormant Street Civic Policies------------')
        log.debug('------------Dormant Street Civic Policies------------')
        for policy in policies:
            output(f'Policy: {policy}')
            log.format_with_message(f'Policy: {policy}')
        output('------------------------------------------------------')
        log.debug('------------------------------------------------------')
    finally:
        log.disable()
