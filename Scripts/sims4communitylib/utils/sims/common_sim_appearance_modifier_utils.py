"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Type, Iterator, Any, Callable

from buffs.appearance_modifier.appearance_modifier import AppearanceModifier
from buffs.appearance_modifier.appearance_tracker import AppearanceTracker, ModifierInfo
from cas.cas import OutfitOverrideOptionFlags
from sims.sim_info import SimInfo
from sims4communitylib.enums.common_appearance_modifier_priority import CommonAppearanceModifierPriority
from sims4communitylib.enums.common_appearance_modifier_type import CommonAppearanceModifierType


class CommonSimAppearanceModifierUtils:
    """Utilities for manipulating the appearance modifiers of Sims.

    """
    @staticmethod
    def get_appearance_tracker(sim_info: SimInfo) -> Union[AppearanceTracker, None]:
        """get_appearance_tracker(sim_info)

        Retrieve the appearance tracker of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The appearance tracker for the Sim or None if not found.
        :rtype: Union[AppearanceTracker, None]
        """
        if sim_info is None:
            return None
        if sim_info.appearance_tracker is None:
            return None
        return sim_info.appearance_tracker

    @staticmethod
    def has_any_appearance_modifiers(sim_info: SimInfo) -> bool:
        """has_any_appearance_modifiers(sim_info)

        Determine if a Sim has any appearance modifiers applied to them.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has any appearance modifiers applied to them. False, if not.
        :rtype: bool
        """
        return any(CommonSimAppearanceModifierUtils.get_appearance_modifiers_gen(sim_info))

    @staticmethod
    def has_any_appearance_modifiers_with_guid(sim_info: SimInfo, modifier_guid: int) -> bool:
        """has_any_appearance_modifiers_with_guid(sim_info, modifier_guid)

        Determine if a Sim has any appearance modifiers applied to them with a specified GUID.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param modifier_guid: The GUID of the modifier to search for.
        :type modifier_guid: int
        :return: True, if the Sim has any appearance modifiers applied to them with the specified GUID. False, if not.
        :rtype: bool
        """
        return any(CommonSimAppearanceModifierUtils.get_appearance_modifiers_by_guid_gen(sim_info, modifier_guid))

    @staticmethod
    def has_any_appearance_modifiers_of_type(sim_info: SimInfo, modifier_type: Type[AppearanceModifier.BaseAppearanceModification]) -> bool:
        """has_any_appearance_modifiers_of_type(sim_info, modifier_type)

        Determine if a Sim has any appearance modifiers applied to them of a specified type.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param modifier_type: The type of modifier to search for.
        :type modifier_type: Type[AppearanceModifier.BaseAppearanceModification]
        :return: True, if the Sim has any appearance modifiers applied to them of the specified type. False, if not.
        :rtype: bool
        """
        return any(CommonSimAppearanceModifierUtils.get_appearance_modifiers_by_type_gen(sim_info, modifier_type))

    @staticmethod
    def get_appearance_modifiers_by_guid_gen(sim_info: SimInfo, modifier_guid: int) -> Iterator[ModifierInfo]:
        """get_appearance_modifiers_by_guid_gen(sim_info, modifier_guid)

        Retrieve the appearance modifiers applied to a Sim that have the specified GUID.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param modifier_guid: The GUID of the modifiers to search for.
        :type modifier_guid: int
        :return: An iterator of Appearance Modifiers that have the specified GUID.
        :rtype: Iterator[ModifierInfo]
        """
        def _matches(_modifier_type: Any, _appearance_modifier: ModifierInfo) -> bool:
            return _appearance_modifier.guid == modifier_guid

        yield from CommonSimAppearanceModifierUtils.get_appearance_modifiers_gen(sim_info, include_appearance_modifier=_matches)

    @staticmethod
    def get_appearance_modifiers_by_type_gen(sim_info: SimInfo, modifier_type: Type[AppearanceModifier.BaseAppearanceModification]) -> Iterator[ModifierInfo]:
        """get_appearance_modifiers_by_type_gen(sim_info, modifier_type)

        Retrieve the appearance modifiers applied to a Sim that match a specified type.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param modifier_type: The type of the modifiers to search for.
        :type modifier_type: Type[AppearanceModifier.BaseAppearanceModification]
        :return: An iterator of Appearance Modifiers that match the specified type.
        :rtype: Iterator[ModifierInfo]
        """
        def _matches(_modifier_type: Any, _appearance_modifier: ModifierInfo) -> bool:
            return isinstance(_appearance_modifier.modifier, modifier_type)

        yield from CommonSimAppearanceModifierUtils.get_appearance_modifiers_gen(sim_info, include_appearance_modifier=_matches)

    @staticmethod
    def get_appearance_modifiers_gen(sim_info: SimInfo, include_appearance_modifier: Callable[[CommonAppearanceModifierType, ModifierInfo], bool] = None) -> Iterator[ModifierInfo]:
        """get_appearance_modifiers_gen(sim_info, include_appearance_modifier=None)

        Retrieve the appearance modifiers applied to a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param include_appearance_modifier: If the result of this callback is True, the Appearance Modifier will be included in the results. If set to None, All Appearance Modifiers will be included. Default is None.
        :type include_appearance_modifier: Callable[[CommonAppearanceModifierType, ModifierInfo], bool], optional
        :return: An iterator of all Appearance Modifiers applied to the Sim that match the `include_appearance_modifier` filter.
        :rtype: Iterator[ModifierInfo]
        """
        appearance_tracker = CommonSimAppearanceModifierUtils.get_appearance_tracker(sim_info)
        if appearance_tracker is None:
            return tuple()
        if appearance_tracker._active_appearance_modifier_infos is None:
            return tuple()
        for (modifier_type, appearance_modifiers) in appearance_tracker._active_appearance_modifier_infos.items():
            for appearance_modifier in appearance_modifiers:
                if include_appearance_modifier is not None and not include_appearance_modifier(modifier_type, appearance_modifier):
                    continue
                yield appearance_modifier
        return tuple()

    @staticmethod
    def add_appearance_modifier(
        sim_info: SimInfo,
        modifier: AppearanceModifier.BaseAppearanceModification,
        modifier_guid: int,
        priority: CommonAppearanceModifierPriority = CommonAppearanceModifierPriority.TRANSFORMED,
        apply_to_all_outfits: bool = True,
        additional_flags: OutfitOverrideOptionFlags = OutfitOverrideOptionFlags.DEFAULT,
        source: Any = None
    ) -> None:
        """add_appearance_modifier(\
            sim_info,\
            modifier,\
            modifier_guid,\
            priority=CommonAppearanceModifierPriority.TRANSFORMED,\
            apply_to_all_outfits=True,\
            additional_flags=OutfitOverrideOptionFlags.DEFAULT,\
            source=None\
        )

        Determine if a Sim has any appearance modifiers applied to them of a specified type.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param modifier: The Appearance Modifier to apply.
        :type modifier: AppearanceModifier.BaseAppearanceModification
        :param modifier_guid: The GUID of the appearance modifier being applied.
        :type modifier_guid: int
        :param priority: The priority of the appearance modifier. This determines which types of appearance modifiers can override this modifier and which ones this modifier overrides. Default is CommonAppearanceModifierPriority.TRANSFORMED.
        :type priority: CommonAppearanceModifierPriority, optional
        :param apply_to_all_outfits: If True, the appearance modifier will apply to all outfits. If False, the appearance modifier will only apply the current outfit of the Sim. Default is True.
        :type apply_to_all_outfits: bool, optional
        :param additional_flags: Additional flags for overriding outfit parts. Default is OutfitOverrideOptionFlags.DEFAULT.
        :type additional_flags: OutfitOverrideOptionFlags, optional
        :param source: The source of the appearance modifier. Default is None.
        :type source: Any, optional
        """
        appearance_tracker = sim_info.appearance_tracker
        if isinstance(modifier, tuple):
            if len(modifier) > 1:
                modifier = appearance_tracker._choose_modifier(modifier)
            else:
                modifier = modifier[0].modifier
        vanilla_priority = CommonAppearanceModifierPriority.convert_to_vanilla(priority)
        appearance_tracker.add_appearance_modifier(modifier, modifier_guid, vanilla_priority, apply_to_all_outfits, source=source, additional_flags=additional_flags)

    @staticmethod
    def remove_appearance_modifiers_by_guid(sim_info: SimInfo, modifier_guid: int, source: str = 'S4CL Removal') -> None:
        """remove_appearance_modifiers_by_guid(sim_info, modifier_guid, source='S4CL Removal')

        Remove appearance modifiers from a Sim by their GUID.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param modifier_guid: The GUID of the modifiers to remove.
        :type modifier_guid: int
        :param source: The source of the removal. Default is "S4CL Removal".
        :type source: str, optional
        """
        appearance_tracker = CommonSimAppearanceModifierUtils.get_appearance_tracker(sim_info)
        if appearance_tracker is None:
            return
        appearance_tracker.remove_appearance_modifiers(modifier_guid, source=source)

    @staticmethod
    def evaluate_appearance_modifiers(sim_info: SimInfo) -> None:
        """evaluate_appearance_modifiers(sim_info)

        Force evaluate the appearance modifiers of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        """
        appearance_tracker = CommonSimAppearanceModifierUtils.get_appearance_tracker(sim_info)
        if appearance_tracker is None:
            return
        appearance_tracker.evaluate_appearance_modifiers()
