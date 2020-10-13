"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from pprint import pformat
from typing import Tuple, FrozenSet, Dict, List, Union

from cas.cas import OutfitData
from protocolbuffers import S4Common_pb2, Outfits_pb2
from sims.outfits.outfit_enums import OutfitCategory, BodyType
from sims.sim_info import SimInfo
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils


class CommonSimOutfitIO(HasLog):
    """CommonSimOutfitIO(sim_info, outfit_category_and_index=None, override_outfit_parts=None)

    Make changes to an outfit of a Sim.

    :param sim_info: An instance of a Sim.
    :type sim_info: SimInfo
    :param outfit_category_and_index: The OutfitCategory and Index of the Outfit being written to or read from. Default is the current outfit of the Sim.
    :type outfit_category_and_index: Tuple[OutfitCategory, int], optional
    :param initial_outfit_parts: A library of body types and cas parts to use in place of the normal parts of their outfit. If set to None, OutfitParts will be loaded from the specified OutfitCategory and Index. Default is None.
    :type initial_outfit_parts: Dict[BodyType, int], optional
    """
    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'common_sim_outfit_io'

    def __init__(self, sim_info: SimInfo, outfit_category_and_index: Tuple[OutfitCategory, int]=None, initial_outfit_parts: Dict[BodyType, int]=None):
        super().__init__()
        self._sim_info: SimInfo = sim_info
        self._current_outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)
        self._outfit_category_and_index: Tuple[OutfitCategory, int] = outfit_category_and_index or self._current_outfit_category_and_index
        self._outfit_data: OutfitData = None
        self._outfit_parts: Dict[BodyType, int] = None
        self._original_outfit_data: FrozenSet[int] = None
        self._outfit_body_types: List[Union[BodyType, int]] = None
        self._outfit_part_ids: List[int] = None
        self._load(initial_outfit_parts=initial_outfit_parts)

    @property
    def sim_info(self) -> SimInfo:
        """ The Sim to apply Outfit changes to.

        :return: An instance of a Sim.
        :rtype: SimInfo
        """
        return self._sim_info

    @property
    def outfit_category_and_index(self) -> Tuple[OutfitCategory, int]:
        """ The OutfitCategory and Index of the Outfit being written to.

        :return: The OutfitCategory and Index of the Outfit being written to.
        :rtype: Tuple[OutfitCategory, int]
        """
        return self._outfit_category_and_index

    @property
    def cas_part_ids(self) -> Tuple[int]:
        """The decimal identifiers of CAS Parts attached to the outfit.

        :return: A collection of decimal identifiers of CAS Parts attached to the outfit.
        :rtype: Tuple[int]
        """
        return tuple(self._outfit_part_ids)

    @property
    def body_types(self) -> Tuple[Union[BodyType, int]]:
        """The body types attached to the outfit.

        :return: A collection of body types attached to the outfit.
        :rtype: Tuple[Union[BodyType, int]]
        """
        return tuple(self._outfit_body_types)

    def is_body_type_attached(self, body_type: Union[BodyType, int]) -> bool:
        """is_body_type_attached(body_type)

        Determine if the specified BodyType is attached to the outfit.

        :param body_type: The BodyType to look for.
        :type body_type: Union[BodyType, int]
        :return: True, if the specified BodyType is attached to the outfit. False, if not.
        :rtype: bool
        """
        return self.is_any_cas_part_attached((body_type,))

    def is_any_body_type_attached(self, body_types: Tuple[Union[BodyType, int]]) -> bool:
        """is_any_body_type_attached(body_types)

        Determine if any of the specified BodyTypes are attached to the outfit.

        :param body_types: The BodyType to look for.
        :type body_types: Union[BodyType, int]
        :return: True, if any of the specified BodyTypes are attached to the outfit. False, if not.
        :rtype: bool
        """
        for body_type in body_types:
            for outfit_body_type in self._outfit_body_types:
                if int(body_type) == int(outfit_body_type):
                    return True
        return False

    def is_cas_part_attached(self, cas_part_id: int) -> bool:
        """is_cas_part_attached(cas_part_id)

        Determine if the specified CAS Part is attached to the outfit.

        :param cas_part_id: The decimal identifier of a CAS Part.
        :type cas_part_id: int
        :return: True, if the specified CAS Part is attached to the outfit. False, if not.
        :rtype: bool
        """
        return self.is_any_cas_part_attached((cas_part_id,))

    def is_any_cas_part_attached(self, cas_part_ids: Tuple[int]) -> bool:
        """is_any_cas_part_attached(cas_part_ids)

        Determine if any of the specified CAS Parts are attached to the outfit.

        :param cas_part_ids: A collection of decimal identifiers of CAS Parts.
        :type cas_part_ids: Tuple[int]
        :return: True, if any of the specified CAS Parts are attached to the outfit. False, if not.
        :rtype: bool
        """
        return any((int(cas_part_id) in self._outfit_part_ids for cas_part_id in cas_part_ids))

    def get_cas_part_at_body_type(self, body_type: Union[BodyType, int]) -> int:
        """get_cas_part_at_body_type(body_type)

        Retrieve the CAS Part located at the specified body type.

        :param body_type: The BodyType to look at.
        :type body_type: Union[BodyType, int]
        :return: The decimal identifier of the CAS Part located at the specified body part or -1 if the Outfit does not have the body type or the body type is empty.
        :rtype: int
        """
        for body_type_index in range(len(self._outfit_body_types)):
            if body_type_index not in self._outfit_body_types or int(self._outfit_body_types[body_type_index]) != int(body_type):
                self.log.format_with_message('Body type not found or already removed.', body_type=body_type)
                continue

            return self._outfit_part_ids[body_type_index]
        return -1

    def attach_cas_part(self, cas_part_id: int, body_type: Union[BodyType, int]=BodyType.NONE) -> bool:
        """attach_cas_part(cas_part_id, body_type=BodyType.NONE)

        Attach a CAS Part to the specified body type.

        ..note:: This will override the CAS Part located at the body type, if there is one.

        :param cas_part_id: The decimal identifier of a CAS Part.
        :type cas_part_id: int
        :param body_type: The BodyType the CAS Part will be attached to. Default is the BodyType of the CAS Part
        :type body_type: Union[BodyType, int], optional
        :return: True, if the CAS Part was attached successfully. False, if not.
        :rtype: bool
        """
        from sims4communitylib.utils.cas.common_cas_utils import CommonCASUtils
        if body_type == BodyType.NONE:
            body_type = CommonCASUtils.get_body_type_of_cas_part(cas_part_id)
        self.log.format_with_message('Attempting to add cas part to body type.', cas_part=cas_part_id, body_type=body_type)
        if self.is_body_type_attached(body_type):
            self.detach_body_type(body_type)
        self._outfit_body_types.append(int(body_type))
        self._outfit_part_ids.append(cas_part_id)
        self.log.format_with_message('Finished adding cas part to body type.', cas_part=cas_part_id, body_type=body_type)
        return True

    def detach_cas_part(self, cas_part_id: int) -> bool:
        """detach_cas_part(cas_part_id)

        Detach a CAS Part from all body types of the Outfit.

        :param cas_part_id: The decimal identifier of a CAS Part.
        :type cas_part_id: int
        :return: True, if the CAS Part was erased from all body types successfully. False, if not.
        :rtype: bool
        """
        self.log.format_with_message('Attempting to remove cas part', cas_part=cas_part_id, current_body_types=pformat(self._outfit_body_types), current_cas_parts=pformat(self._outfit_body_types))
        new_body_types = list()
        new_part_ids = list()
        for body_type_index in range(len(self._outfit_body_types)):
            if int(self._outfit_part_ids[body_type_index]) == int(cas_part_id):
                self.log.format_with_message('Detaching CAS Part.', cas_part=cas_part_id)
                continue
            self.log.format_with_message('Keeping CAS Part.', cas_part=int(cas_part_id), other_cas_part=int(self._outfit_part_ids[body_type_index]))
            new_body_types.append(self._outfit_body_types[body_type_index])
            new_part_ids.append(self._outfit_part_ids[body_type_index])
        self._outfit_body_types = new_body_types
        self._outfit_part_ids = new_part_ids
        return True

    def detach_body_type(self, body_type: Union[BodyType, int]) -> bool:
        """detach_body_type(body_type)

        Detach the BodyType including the CAS Part attached to it from the outfit.

        :param body_type: The BodyType being detached.
        :type body_type: Union[BodyType, int]
        :return: True, if the Body Type was detached from the outfit successfully. False, if not.
        :rtype: bool
        """
        self.log.format_with_message('Attempting to remove body type', body_type=body_type)
        self.log.format(current_body_types=pformat(self._outfit_body_types))
        new_body_types = list()
        new_part_ids = list()
        for body_type_index in range(len(self._outfit_body_types)):
            if int(self._outfit_body_types[body_type_index]) == int(body_type):
                self.log.format_with_message('Detaching body type', body_type=body_type)
                continue
            self.log.format_with_message('Keeping body type.', body_type=int(body_type), other_body_type=int(self._outfit_body_types[body_type_index]))
            new_body_types.append(self._outfit_body_types[body_type_index])
            new_part_ids.append(self._outfit_part_ids[body_type_index])
        self._outfit_body_types = new_body_types
        self._outfit_part_ids = new_part_ids
        return True

    def apply(self, resend_outfits_after_apply: bool=True, change_sim_to_outfit_after_apply: bool=True, apply_to_all_outfits_in_same_category: bool=False, apply_to_outfit_category_and_index: Tuple[OutfitCategory, int]=None) -> bool:
        """apply(resend_outfits_after_apply=True, change_sim_to_outfit_after_apply=True, apply_to_all_outfits_in_same_category=False, apply_to_outfit_category_and_index=None)

        Apply all changes made to the Outfit.

        :param resend_outfits_after_apply: If set to True, the outfits of the Sim will be re-sent after changes have been applied. Default is True.
        :type resend_outfits_after_apply: bool, optional
        :param change_sim_to_outfit_after_apply: If set to True, the Sim will change to the outfit after the outfit is updated. Default is True.
        :type change_sim_to_outfit_after_apply: bool, optional
        :param apply_to_all_outfits_in_same_category: If set to True, changes will be applied to all Outfits in the same category. If set to False, changes will only be applied to the outfit provided at initialization. Default is False.
        :type apply_to_all_outfits_in_same_category: bool, optional
        :param apply_to_outfit_category_and_index: The OutfitCategory and Index to apply changes to. If set to None, it will be the OutfitCategory and Index provided at initialization. Default is None.
        :type apply_to_outfit_category_and_index: Tuple[OutfitCategory, int], optional
        :return: True, if changes were applied successfully. False, if not.
        :rtype: bool
        """
        sim_name = CommonSimNameUtils.get_full_name(self.sim_info)
        self.log.format_with_message(
            'Applying changes to outfit',
            sim=sim_name,
            resend_outfits=resend_outfits_after_apply,
            change_to_outfit=change_sim_to_outfit_after_apply,
            apply_to_all_outfits_in_same_category=apply_to_all_outfits_in_same_category,
            apply_to_outfit_category_and_index=apply_to_outfit_category_and_index
        )
        apply_to_outfit_category_and_index = apply_to_outfit_category_and_index or self.outfit_category_and_index
        saved_outfits = self.sim_info.save_outfits()
        for saved_outfit in saved_outfits.outfits:
            if int(saved_outfit.category) != int(apply_to_outfit_category_and_index[0]):
                continue

            if apply_to_all_outfits_in_same_category:
                pass
            else:
                # noinspection PyUnresolvedReferences
                sub_outfit_data = self._to_outfit_data(saved_outfit.body_types_list.body_types, saved_outfit.parts.ids)
                if int(saved_outfit.outfit_id) != int(self._outfit_data.outfit_id) or sub_outfit_data != self._original_outfit_data:
                    continue

            saved_outfit.parts = S4Common_pb2.IdList()
            # noinspection PyUnresolvedReferences
            saved_outfit.parts.ids.extend(self._outfit_part_ids)
            saved_outfit.body_types_list = Outfits_pb2.BodyTypesList()
            # noinspection PyUnresolvedReferences
            saved_outfit.body_types_list.body_types.extend(self._outfit_body_types)
            if not apply_to_all_outfits_in_same_category:
                break

        self.sim_info._base.outfits = saved_outfits.SerializeToString()
        if change_sim_to_outfit_after_apply:
            self.sim_info._base.outfit_type_and_index = apply_to_outfit_category_and_index
        else:
            self.sim_info._base.outfit_type_and_index = self._current_outfit_category_and_index
        self.log.format_with_message('Finished flushing outfit changes.', sim=sim_name)
        if resend_outfits_after_apply:
            return CommonOutfitUtils.resend_outfits(self.sim_info)
        return True

    def _load(self, initial_outfit_parts: Dict[BodyType, int]=None) -> bool:
        target_sim_name = CommonSimNameUtils.get_full_name(self.sim_info)
        self._outfit_data: OutfitData = CommonOutfitUtils.get_outfit_data(self.sim_info, outfit_category_and_index=self._outfit_category_and_index)
        if self._outfit_data is None:
            self.log.error('Missing outfit data for Sim \'{}\' and Outfit Category and Index {}'.format(target_sim_name, self._outfit_category_and_index), throw=True)
            return False
        self._outfit_parts = CommonOutfitUtils.get_outfit_parts(self.sim_info, outfit_category_and_index=self._outfit_category_and_index)
        self._original_outfit_data: FrozenSet[int] = frozenset(self._outfit_parts.items())
        if initial_outfit_parts is not None:
            for (key, value) in initial_outfit_parts.items():
                if not isinstance(key, int) or not isinstance(value, int):
                    self.log.error('\'{}\': outfit_body_parts contains non-integer variables key: {} value: {}.'.format(target_sim_name, key, value))
                    return False

            self._outfit_body_types = list(initial_outfit_parts.keys())
            self._outfit_part_ids = list(initial_outfit_parts.values())
        else:
            if not self._outfit_data.part_ids or not self._outfit_data.body_types:
                self.log.error('\'{}\' is missing outfit parts or body types for Outfit Category and Index {}.'.format(target_sim_name, self._outfit_category_and_index))
                return False
            self._outfit_body_types: List[Union[BodyType, int]] = list(self._outfit_data.body_types)
            self._outfit_part_ids: List[int] = list(self._outfit_data.part_ids)
            if len(self._outfit_body_types) != len(self._outfit_part_ids):
                self.log.error('\'{}\': The number of outfit parts did not match the number of body types for Outfit Category and Index {}.'.format(target_sim_name, self._outfit_category_and_index))
                return False
        return True

    def _to_outfit_data(self, body_types: Tuple[BodyType], part_ids: Tuple[int]) -> FrozenSet[int]:
        return frozenset(dict(zip(list(body_types), list(part_ids))).items())
