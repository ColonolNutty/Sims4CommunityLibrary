"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from event_testing.resolver import DoubleSimResolver
from interactions import ParticipantType, ParticipantTypeSituationSims
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonDoubleSimResolver(DoubleSimResolver):
    """A double Sim resolver that is able to handle many more participant types."""

    # noinspection PyMissingOrEmptyDocstring
    def get_participants(self, participant_type, **kwargs) -> Any:
        from event_testing.test_constants import SIM_INSTANCE, FROM_DATA_OBJECT, OBJECTIVE_GUID64, FROM_EVENT_DATA
        if participant_type == SIM_INSTANCE:
            participant_type = ParticipantType.Actor

        if participant_type in (
            # Participants Shared
            ParticipantType.Lot,
            ParticipantType.LotOwners,
            ParticipantType.LotOwnersOrRenters,
            ParticipantType.LotOwnerSingleAndInstanced,
            ParticipantType.ActiveHousehold,
            ParticipantType.AllInstancedActiveHouseholdSims,
            ParticipantType.CareerEventSim,
            ParticipantType.AllInstancedSims,
            ParticipantType.Street,
            ParticipantType.VenuePolicyProvider,
            ParticipantType.CurrentRegion,
            # Single Sim Resolver
            ParticipantType.Actor,
            ParticipantType.CustomSim,
            ParticipantType.SignificantOtherActor,
            ParticipantType.PregnancyPartnerActor,
            ParticipantType.AllRelationships,
            ParticipantType.ActorFeudTarget,
            ParticipantType.InteractionContext,
            ParticipantType.Affordance,
            ParticipantType.Familiar,
            ParticipantType.PickedZoneId,
            ParticipantType.ActorLot,
            ParticipantType.RoutingSlaves,
            ParticipantType.StoredCASPartsOnObject,
            ParticipantType.ActorLotLevel,
            # Double Sim Resolver
            ParticipantType.TargetSim,
            ParticipantType.TargetHouseholdMembers,
            ParticipantType.SignificantOtherTargetSim,
            ParticipantType.FamiliarOfTarget
        ):
            return super().get_participants(participant_type, **kwargs)

        sim = CommonSimUtils.get_sim_instance(self.sim_info_to_test)
        target_sim = CommonSimUtils.get_sim_instance(self.target_sim_info)
        if participant_type == ParticipantType.Object:
            return (self.target_sim_info,)
        elif participant_type == ParticipantType.ObjectIngredients:
            if target_sim is not None and hasattr(target_sim, 'crafting_component') and target_sim.crafting_component and hasattr(target_sim, 'get_crafting_process'):
                target_crafting_process = target_sim.get_crafting_process()
                if target_crafting_process is not None:
                    return tuple(target_crafting_process.get_ingredients_object_definitions())
            return ()

        if participant_type == ParticipantType.ActorPostureTarget:
            return (self.target_sim_info, )
        elif participant_type == ParticipantType.AssociatedClub or participant_type == ParticipantType.AssociatedClubLeader or participant_type == ParticipantType.AssociatedClubMembers:
            return ()
        if participant_type == ParticipantType.ObjectCrafter:
            return (self.sim_info_to_test, )
        if participant_type in ParticipantTypeSituationSims:
            return self.sim_info_to_test, self.target_sim_info
        else:
            if participant_type == ParticipantType.ObjectLotLevel:
                return self._get_lot_level_from_object(target_sim)
            if participant_type == ParticipantType.ActorLotLevel:
                return self._get_lot_level_from_object(sim)
        if participant_type == 0:
            return ()
        result = self._get_participants_base(participant_type, **kwargs)
        if result is not None:
            return result
        if participant_type == FROM_DATA_OBJECT:
            return ()
        if participant_type == OBJECTIVE_GUID64:
            return ()
        if participant_type == FROM_EVENT_DATA:
            return ()
        if participant_type == ParticipantType.PickedItemId:
            return (self.target_sim_info, )
        if participant_type == ParticipantType.Listeners:
            return (self.target_sim_info, )
        return self.sim_info_to_test, self.target_sim_info
