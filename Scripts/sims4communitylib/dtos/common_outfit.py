"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Dict, Any, List, Tuple

from sims.outfits.outfit_enums import BodyType, OutfitCategory
from sims.sim_info import SimInfo
from sims4communitylib.classes.serialization.common_serializable import CommonSerializable
from sims4communitylib.enums.common_body_slot import CommonBodySlot
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.services.sim.cas.common_sim_outfit_io import CommonSimOutfitIO
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils


class CommonOutfit(CommonSerializable):
    """CommonOutfit(outfit_parts)

    Contains information on the CAS Parts that make up an outfit.

    :param outfit_parts: A mapping of CAS Parts organized by Body Slot.
    :type outfit_parts: Dict[Union[CommonBodySlot, BodyType, int], int]
    """

    def __init__(self, outfit_parts: Dict[Union[CommonBodySlot, BodyType, int], int]):
        self._outfit_parts = outfit_parts

    @property
    def outfit_parts(self) -> Dict[Union[CommonBodySlot, BodyType, int], int]:
        """A library of Body Slots to CAS Part Ids"""
        return self._outfit_parts

    def has_body_slot(self, body_slot: Union[CommonBodySlot, BodyType, int]) -> bool:
        """has_body_slot(body_slot)

        Determine if the Outfit has a Body Slot.

        :param body_slot: A body slot.
        :type body_slot: Union[CommonBodySlot, BodyType, int]
        :return: True, if the outfit has the specified body slot. False, if not.
        :rtype: bool
        """
        return body_slot in self.outfit_parts

    def has_cas_part(self, cas_part: int) -> bool:
        """has_cas_part(cas_part)

        Determine if the Outfit has a CAS Part.

        :param cas_part: The decimal identifier of a CAS Part.
        :type cas_part: int
        :return: True, if the outfit contains the specified CAS Part. False, if not.
        :rtype: bool
        """
        return any(self.get_all_by_cas_part(cas_part))

    def set_outfit_part(self, body_slot: Union[CommonBodySlot, BodyType, int], cas_part: int):
        """set_outfit_part(body_slot, cas_part)

        Set the CAS Part id at a Body Slot.

        :param body_slot: A body slot.
        :type body_slot: Union[CommonBodySlot, BodyType, int]
        :param cas_part: The decimal identifier of a CAS Part.
        :type cas_part: int
        """
        self.outfit_parts[body_slot] = cas_part

    def get_by_body_slot(self, body_slot: Union[CommonBodySlot, BodyType, int]) -> int:
        """get_by_body_slot(body_slot)

        Retrieve the CAS Part ID at a Body Slot.

        :param body_slot: A body slot.
        :type body_slot: Union[CommonBodySlot, BodyType, int]
        :return: The decimal identifier of the CAS Part located at the body slot on the outfit or -1 if the body slot is not found.
        :rtype: int
        """
        return self.outfit_parts.get(body_slot, -1)

    def get_all_by_cas_part(self, cas_part: int) -> Tuple[Union[CommonBodySlot, BodyType, int]]:
        """get_all_by_cas_part(cas_part)

        Retrieve the Body Slots a CAS Part is attached to.

        :param cas_part: The CAS Part to look for.
        :type cas_part: Union[CommonBodySlot, BodyType, int]
        :return: A collection of body slots the CAS Part is attached to or an empty collection if the CAS Part is not attached to the outfit.
        :rtype: Tuple[Union[CommonBodySlot, BodyType, int]]
        """
        body_slots: List[Union[CommonBodySlot, BodyType, int]] = list()
        for (body_slot, _cas_part) in self.outfit_parts.items():
            if _cas_part == cas_part:
                body_slots.append(body_slot)
        return tuple(body_slots)

    def remove_by_body_slot(self, body_slot: Union[CommonBodySlot, BodyType, int]):
        """remove_by_body_slot(body_slot)

        Remove a CAS Part by a Body Slot.

        :param body_slot: A body slot.
        :type body_slot: Union[CommonBodySlot, BodyType, int]
        """
        if body_slot not in self.outfit_parts:
            return
        del self.outfit_parts[body_slot]

    def remove_by_cas_part(self, cas_part: int):
        """remove_by_cas_part(cas_part)

        Remove all Body Slots containing a CAS Part.

        :param cas_part: The decimal identifier of a CAS Part.
        :type cas_part: int
        """
        body_slots = self.get_all_by_cas_part(cas_part)
        for body_slot in body_slots:
            self.remove_by_body_slot(body_slot)

    def clone(self) -> 'CommonOutfit':
        """clone()

        Create a clone of the outfit.

        :return: A clone of the outfit.
        :rtype: CommonOutfit
        """
        return CommonOutfit(dict(self.outfit_parts))

    # noinspection PyMissingOrEmptyDocstring
    def serialize(self) -> Union[str, Dict[str, Any]]:
        data = dict()
        if not self.outfit_parts:
            return data
        outfit_parts_list = list()
        for (body_slot, cas_part) in self.outfit_parts.items():
            outfit_parts_list.append((body_slot.name if hasattr(body_slot, 'name') else str(int(body_slot)), cas_part))
        if outfit_parts_list:
            data['outfit_parts'] = outfit_parts_list
        return data

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def deserialize(cls, data: Union[str, Dict[str, Any]]) -> 'CommonOutfit':
        if not data:
            return CommonOutfit(dict())
        if isinstance(data, CommonOutfit):
            return data
        outfit_parts_list: List[Union[CommonBodySlot, BodyType, int], int] = data.get('outfit_parts', None)
        outfit_parts = dict()
        for (body_slot_str, cas_part) in outfit_parts_list:
            if isinstance(body_slot_str, int):
                body_slot = CommonResourceUtils.get_enum_by_int_value(int(body_slot_str), CommonBodySlot, default_value=CommonBodySlot.NONE)
                if body_slot == CommonBodySlot.NONE:
                    body_slot = CommonResourceUtils.get_enum_by_int_value(int(body_slot_str), BodyType, default_value=BodyType.NONE)
                    if body_slot == BodyType.NONE:
                        body_slot = body_slot_str
                    else:
                        body_slot = CommonBodySlot.convert_from_vanilla(body_slot)
            elif isinstance(body_slot_str, str) and body_slot_str.isnumeric():
                body_slot = CommonResourceUtils.get_enum_by_int_value(int(body_slot_str), CommonBodySlot, default_value=CommonBodySlot.NONE)
                if body_slot == CommonBodySlot.NONE:
                    body_slot = CommonResourceUtils.get_enum_by_int_value(int(body_slot_str), BodyType, default_value=BodyType.NONE)
                    if body_slot == BodyType.NONE:
                        body_slot = body_slot_str
                    else:
                        body_slot = CommonBodySlot.convert_from_vanilla(body_slot)
            else:
                body_slot = CommonResourceUtils.get_enum_by_name(body_slot_str, CommonBodySlot, default_value=CommonBodySlot.NONE)
                if body_slot == CommonBodySlot.NONE:
                    body_slot = CommonResourceUtils.get_enum_by_name(body_slot_str, BodyType, default_value=BodyType.NONE)
                    if body_slot == BodyType.NONE:
                        continue
                    body_slot = CommonBodySlot.convert_from_vanilla(body_slot)
            outfit_parts[body_slot] = cas_part
        return CommonOutfit(outfit_parts)

    @classmethod
    def from_sim(cls, mod_identity: CommonModIdentity, sim_info: SimInfo, outfit_category_and_index: Union[Tuple[OutfitCategory, int], None] = None, include_body_slots: Tuple[Union[CommonBodySlot, BodyType, int]] = None) -> 'CommonOutfit':
        """from_sim(mod_identity, sim_info, outfit_category_and_index, include_body_slots=None)

        Create an outfit from the outfit of a Sim.

        :param mod_identity: The identity of the mod making the change.
        :type mod_identity: CommonModIdentity
        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param outfit_category_and_index: The Category and Index of the outfit to copy from. Default is the current outfit of the Sim.
        :type outfit_category_and_index: Union[Tuple[OutfitCategory, int], None], optional
        :param include_body_slots: A collection of body slots to include. If set to None, all body slots will be included. Default is None.
        :type include_body_slots: Tuple[Union[CommonBodySlot, BodyType, int]], optional
        :return: An Outfit created from the Sim.
        :rtype: CommonOutfit
        """
        if include_body_slots is not None:
            include_body_slots = tuple([int(body_type) for body_type in include_body_slots])
        outfit_io = CommonSimOutfitIO(sim_info, outfit_category_and_index=outfit_category_and_index, mod_identity=mod_identity)
        return cls.from_outfit_io(outfit_io, include_body_slots=include_body_slots)

    def apply_to_sim(self, mod_identity: CommonModIdentity, sim_info: SimInfo, outfit_category_and_index: Union[Tuple[OutfitCategory, int], None] = None, override_all: bool = False) -> None:
        """apply_to_sim(mod_identity, sim_info, outfit_category_and_index=None, override_all=False)

        Apply the outfit parts to the outfit of a Sim.

        :param mod_identity: The identity of the mod making the change.
        :type mod_identity: CommonModIdentity
        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param outfit_category_and_index: The Category and Index of the outfit to copy to. Default is the current outfit of the Sim.
        :type outfit_category_and_index: Union[Tuple[OutfitCategory, int], None], optional
        :param override_all: If True, then all outfit parts on the outfit of th Sim will be removed before applying the parts from this outfit. If False, no parts will be removed. Default is True.
        :type override_all: bool, optional
        """
        outfit_io = CommonSimOutfitIO(sim_info, outfit_category_and_index=outfit_category_and_index, mod_identity=mod_identity)
        self.apply_to_outfit_io(outfit_io, override_all=override_all)
        outfit_io.apply(apply_to_outfit_category_and_index=outfit_category_and_index)

    @classmethod
    def from_outfit_io(cls, outfit_io: CommonSimOutfitIO, include_body_slots: Tuple[Union[CommonBodySlot, BodyType, int]] = None) -> 'CommonOutfit':
        """from_outfit_io(outfit_io, include_body_slots=None)

        Create an outfit from an Outfit IO.

        :param outfit_io: An instance of an Outfit IO.
        :type outfit_io: CommonSimOutfitIO
        :param include_body_slots: A collection of body slots to include. If set to None, all body slots will be included. Default is None.
        :type include_body_slots: Tuple[Union[CommonBodySlot, BodyType, int]], optional
        :return: An Outfit created from the outfit io.
        :rtype: CommonOutfit
        """
        if include_body_slots is not None:
            include_body_slots = tuple([int(body_slot) for body_slot in include_body_slots])
        outfit_parts: Dict[Union[CommonBodySlot, BodyType, int], int] = dict()
        for (body_slot_val, cas_part) in zip(outfit_io.body_types, outfit_io.cas_part_ids):
            if include_body_slots is not None and int(body_slot_val) not in include_body_slots:
                continue
            if isinstance(body_slot_val, int):
                body_slot = CommonResourceUtils.get_enum_by_int_value(body_slot_val, CommonBodySlot, default_value=CommonBodySlot.NONE)
                if body_slot == CommonBodySlot.NONE:
                    body_slot = body_slot_val
            elif isinstance(body_slot_val, BodyType) or isinstance(body_slot_val, CommonBodySlot):
                body_slot = CommonBodySlot.convert_from_vanilla(body_slot_val)
            else:
                body_slot = CommonResourceUtils.get_enum_by_name(body_slot_val, CommonBodySlot, default_value=CommonBodySlot.NONE)

            outfit_parts[body_slot] = cas_part
        return cls(outfit_parts)

    def apply_to_outfit_io(self, outfit_io: CommonSimOutfitIO, override_all: bool = False) -> None:
        """apply_to_outfit_io(outfit_io, override_all=False)

        Apply the outfit parts of this outfit to an outfit io.

        :param outfit_io: An instance of an Outfit IO.
        :type outfit_io: CommonSimOutfitIO
        :param override_all: If True, then all outfit parts on the outfit io will be removed before applying the parts from this outfit. If False, no parts will be removed. Default is True.
        :type override_all: bool, optional
        """
        if override_all:
            for body_slot in tuple(outfit_io.body_types):
                outfit_io.detach_body_type(body_slot)
        for (body_slot_val, cas_part) in self.outfit_parts.items():
            outfit_io.attach_cas_part(cas_part, body_type=CommonBodySlot.convert_to_vanilla(body_slot_val))

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        result = ', '.join(['{} ({}): {}'.format(body_slot.name if hasattr(body_slot, 'name') else body_slot, int(body_slot), cas_part) for (body_slot, cas_part) in self.outfit_parts.items()])
        return result
