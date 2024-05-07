"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Tuple, FrozenSet, Dict, List, Union

from cas.cas import OutfitData
from protocolbuffers import S4Common_pb2, Outfits_pb2
from sims.outfits.outfit_enums import OutfitCategory, BodyType
from sims.sim_info import SimInfo
from sims.sim_info_base_wrapper import SimInfoBaseWrapper
from sims4communitylib.enums.common_body_slot import CommonBodySlot
from sims4communitylib.logging.has_log import HasLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils


class CommonSimOutfitIO(HasLog):
    """CommonSimOutfitIO(sim_info, outfit_category_and_index=None, override_outfit_parts=None)

    Make changes to an outfit of a Sim.

    :param sim_info: An instance of a Sim.
    :type sim_info: Union[SimInfo, SimInfoBaseWrapper]
    :param outfit_category_and_index: The OutfitCategory and Index of the Outfit being written to or read from. Default is the current outfit of the Sim.
    :type outfit_category_and_index: Tuple[OutfitCategory, int], optional
    :param initial_outfit_parts: A library of body types and cas parts to use in place of the normal parts of their outfit. If set to None, OutfitParts will be loaded from the specified OutfitCategory and Index. Default is None.
    :type initial_outfit_parts: Dict[BodyType, int], optional
    :param mod_identity: The identity of the mod making changes. Default is None. Optional, but highly recommended!
    :type mod_identity: CommonModIdentity, optional
    """
    # noinspection PyMissingOrEmptyDocstring
    @property
    def mod_identity(self) -> CommonModIdentity:
        return self._mod_identity

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'common_sim_outfit_io'

    def __init__(self, sim_info: Union[SimInfo, SimInfoBaseWrapper], outfit_category_and_index: Tuple[OutfitCategory, int]=None, initial_outfit_parts: Dict[BodyType, int]=None, mod_identity: CommonModIdentity=None):
        super().__init__()
        self._mod_identity = mod_identity
        self.log.enable_logging_extra_sim_details()
        self._sim_info = sim_info
        self._current_outfit_category_and_index = CommonOutfitUtils.get_current_outfit(sim_info)
        self._outfit_category_and_index: Tuple[OutfitCategory, int] = (CommonOutfitUtils.convert_value_to_outfit_category(outfit_category_and_index[0]), outfit_category_and_index[1]) if outfit_category_and_index is not None else self._current_outfit_category_and_index
        self._outfit_data: OutfitData = None
        self._outfit_parts: Dict[BodyType, int] = None
        self._original_outfit_data: FrozenSet[int] = None
        self._outfit_body_types: List[Union[BodyType, int]] = list()
        self._outfit_part_ids: List[int] = list()
        if not CommonOutfitUtils.has_outfit(self._sim_info, self._outfit_category_and_index):
            self.log.format_warn_with_message('Sim did not have the specified outfit category and index!', sim=self._sim_info, outfit_category_and_index=self._outfit_category_and_index)
        self._load(initial_outfit_parts=initial_outfit_parts)

    @property
    def sim_info(self) -> Union[SimInfo, SimInfoBaseWrapper]:
        """ The Sim to apply Outfit changes to.

        :return: An instance of a Sim.
        :rtype: Union[SimInfo, SimInfoBaseWrapper]
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
    def outfit_parts(self) -> Dict[Union[BodyType, int], int]:
        """A library of Body Types to CAS Part Ids"""
        return self._to_outfit_dictionary(self.body_types, self.cas_part_ids)

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
        return self.is_any_body_type_attached((body_type,))

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

    def get_body_type_cas_part_is_attached_to(self, cas_part_id: int) -> int:
        """get_body_type_cas_part_is_attached_to(cas_part_id)

        Retrieve the Body Type the specified CAS Part is attached to.

        :param cas_part_id: The decimal identifier of a CAS Part.
        :type cas_part_id: int
        :return: The Body Type the specified CAS Part was located at or -1 if the Outfit does not have the CAS Part or the CAS Part is empty.
        :rtype: Union[int, BodyType]
        """
        for (_body_type, _cas_part_id) in zip(self.body_types, self.cas_part_ids):
            if int(_cas_part_id) == int(cas_part_id):
                return _body_type
        self.log.format_with_message('CAS Part not found.', cas_part_id=cas_part_id)
        return -1

    def get_cas_part_at_body_type(self, body_type: Union[CommonBodySlot, BodyType, int]) -> int:
        """get_cas_part_at_body_type(body_type)

        Retrieve the CAS Part located at the specified body type.

        :param body_type: The BodyType to look at.
        :type body_type: Union[CommonBodySlot, BodyType, int]
        :return: The decimal identifier of the CAS Part located at the specified body part or -1 if the Outfit does not have the body type or the body type is empty.
        :rtype: int
        """
        for (_body_type, _cas_part_id) in zip(self.body_types, self.cas_part_ids):
            if int(_body_type) == int(body_type):
                return _cas_part_id
        self.log.format_with_message('Body type not found.', body_type=body_type)
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
        if cas_part_id == -1 or cas_part_id is None:
            self.log.format_error_with_message('Attempted to attach a negative or None CAS Part to the outfit of a Sim!', sim=self.sim_info, body_type=body_type, cas_part_id=cas_part_id, outfit_category_and_index=self._outfit_category_and_index)
            return False
        if body_type == BodyType.NONE:
            body_type = CommonCASUtils.get_body_type_of_cas_part(cas_part_id)
        self.log.format_with_message('Attempting to attach cas part to body type.', cas_part=cas_part_id, body_type=body_type)
        if self.is_body_type_attached(body_type):
            self.detach_body_type(body_type)
        self.log.format_with_message('Attaching CAS Part.', cas_part=cas_part_id, body_type=body_type)
        self._outfit_body_types.append(body_type)
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
        self.log.format_with_message('Attempting to detach cas part', cas_part=cas_part_id, current_body_types=self._outfit_body_types, current_cas_parts=self._outfit_body_types)
        new_body_types = list()
        new_part_ids = list()
        for (_body_type, _cas_part_id) in zip(self.body_types, self.cas_part_ids):
            if int(_cas_part_id) == int(cas_part_id):
                self.log.format_with_message('Detaching CAS Part.', cas_part=cas_part_id)
                continue
            self.log.format_with_message('Keeping CAS Part.', cas_part=cas_part_id, other_cas_part=_cas_part_id)
            new_body_types.append(_body_type)
            new_part_ids.append(_cas_part_id)
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
        self.log.format_with_message('Attempting to detach body type', body_type=body_type)
        self.log.format(current_body_types=self._outfit_body_types)
        new_body_types = list()
        new_part_ids = list()
        for (_body_type, _cas_part_id) in zip(self.body_types, self.cas_part_ids):
            if int(_body_type) == int(body_type):
                self.log.format_with_message('Detaching body type', body_type=body_type)
                continue
            self.log.format_with_message('Keeping body type.', body_type=body_type, other_body_type=_body_type)
            new_body_types.append(_body_type)
            new_part_ids.append(_cas_part_id)
        self._outfit_body_types = new_body_types
        self._outfit_part_ids = new_part_ids
        return True

    def apply(
        self,
        resend_outfits_after_apply: bool=True,
        change_sim_to_outfit_after_apply: bool=True,
        apply_to_all_outfits_in_same_category: bool=False,
        apply_to_outfit_category_and_index: Tuple[OutfitCategory, int]=None
    ) -> bool:
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
            initial_outfit_category_and_index=self.outfit_category_and_index,
            apply_to_all_outfits_in_same_category=apply_to_all_outfits_in_same_category,
            apply_to_outfit_category_and_index=apply_to_outfit_category_and_index
        )
        apply_to_outfit_category_and_index = apply_to_outfit_category_and_index or self.outfit_category_and_index
        outfit_to_apply_to_data = CommonOutfitUtils.get_outfit_data(self.sim_info, outfit_category_and_index=apply_to_outfit_category_and_index)
        outfit_to_apply_to_parts = CommonOutfitUtils.get_outfit_parts(self.sim_info, outfit_category_and_index=apply_to_outfit_category_and_index)
        outfit_to_apply_to_original_data: FrozenSet[int] = frozenset(outfit_to_apply_to_parts.items())
        saved_outfits = self.sim_info.save_outfits()
        self.log.format_with_message('Applying Outfit IO Changes to outfits', sim=self.sim_info, outfits=saved_outfits.outfits, outfit_part_ids=self._outfit_part_ids, outfit_body_types=self._outfit_body_types)
        for saved_outfit in saved_outfits.outfits:
            if int(saved_outfit.category) != int(apply_to_outfit_category_and_index[0]):
                self.log.format_with_message('Ignoring saved outfit due to wrong category.', sim=self.sim_info, outfit_category=saved_outfit.category, expected_category=apply_to_outfit_category_and_index[0])
                continue

            if not apply_to_all_outfits_in_same_category:
                self.log.format_with_message('Changes are not being applied to all outfits in the same category.', sim=self.sim_info, outfit_category_and_index=apply_to_outfit_category_and_index)
                # noinspection PyUnresolvedReferences
                saved_outfit_data = self._to_outfit_data(saved_outfit.body_types_list.body_types, saved_outfit.parts.ids)
                self.log.format_with_message('Checking if sub outfit data matches', saved_outfit_data=saved_outfit_data)
                if int(saved_outfit.outfit_id) != int(outfit_to_apply_to_data.outfit_id) or saved_outfit_data != outfit_to_apply_to_original_data:
                    self.log.format_with_message('Sub outfit data did not match!', saved_outfit_id=saved_outfit.outfit_id, self_outfit_id=outfit_to_apply_to_data.outfit_id, saved_outfit_data=saved_outfit_data, original_outfit_data=outfit_to_apply_to_original_data)
                    continue
                else:
                    self.log.format_with_message('Sub outfit matches.', saved_outfit_id=saved_outfit.outfit_id, self_outfit_id=outfit_to_apply_to_data.outfit_id, saved_outfit_data=saved_outfit_data, original_outfit_data=outfit_to_apply_to_original_data)

            saved_outfit.parts = S4Common_pb2.IdList()
            # noinspection PyUnresolvedReferences
            saved_outfit.parts.ids.extend(self._outfit_part_ids)
            saved_outfit.body_types_list = Outfits_pb2.BodyTypesList()
            # noinspection PyUnresolvedReferences
            saved_outfit.body_types_list.body_types.extend([int(body_type) for body_type in self._outfit_body_types])
            # noinspection PyUnresolvedReferences
            saved_outfit_data = self._to_outfit_data(saved_outfit.body_types_list.body_types, saved_outfit.parts.ids)
            self.log.format_with_message('Changes made.', saved_outfit_data=saved_outfit_data)
            if not apply_to_all_outfits_in_same_category:
                self.log.format_with_message('Skipping the other outfit indexes, since we do not want to apply to all outfits in the same category.', sim=self.sim_info, outfit_category_and_index_applied_to=apply_to_outfit_category_and_index)
                break

        self.sim_info._base.outfits = saved_outfits.SerializeToString()
        if change_sim_to_outfit_after_apply:
            self.sim_info._base.outfit_type_and_index = apply_to_outfit_category_and_index
        else:
            self.sim_info._base.outfit_type_and_index = self._current_outfit_category_and_index
        self.log.format_with_message('Finished applying outfit changes.', sim=self.sim_info, outfit_category_and_index_applid_to=apply_to_outfit_category_and_index)
        if resend_outfits_after_apply:
            CommonOutfitUtils.refresh_outfit(self.sim_info, outfit_category_and_index=self._current_outfit_category_and_index)
            return CommonOutfitUtils.resend_outfits(self.sim_info)
        return True

    def _load(self, initial_outfit_parts: Dict[BodyType, int]=None) -> bool:
        target_sim_name = CommonSimNameUtils.get_full_name(self.sim_info)
        self._outfit_parts = CommonOutfitUtils.get_outfit_parts(self.sim_info, outfit_category_and_index=self._outfit_category_and_index) or dict()
        self._original_outfit_data: FrozenSet[int] = frozenset(self._outfit_parts.items())
        if initial_outfit_parts is not None:
            cleaned_initial_outfit_parts = self._clean_outfit_parts(initial_outfit_parts)

            self._outfit_body_types = list(cleaned_initial_outfit_parts.keys())
            self._outfit_part_ids = list(initial_outfit_parts.values())
        else:
            if self._outfit_parts is None:
                self.log.format_error_with_message('No outfit parts for available Sim \'{}\' and Outfit Category and Index {}'.format(target_sim_name, self._outfit_category_and_index), initial_outfit_parts=initial_outfit_parts, throw=True)
                return False
            self._outfit_parts = self._clean_outfit_parts(self._outfit_parts)

            self._outfit_body_types: List[Union[BodyType, int]] = list(self._outfit_parts.keys())
            self._outfit_part_ids: List[int] = list(self._outfit_parts.values())
            if len(self._outfit_body_types) != len(self._outfit_part_ids):
                self.log.format_error_with_message('\'{}\': The number of cas parts did not match the number of body types for Outfit Category and Index {}.'.format(target_sim_name, self._outfit_category_and_index), outfit_category_and_index=self.outfit_category_and_index, outfit_parts=self._outfit_parts, throw=True)
                return False
        return True

    def _clean_outfit_parts(self, outfit_parts: Dict[Union[BodyType, int], int]) -> Dict[Union[BodyType, int], int]:
        cleaned_outfit_parts = dict()
        for (body_type, cas_part_id) in outfit_parts.items():
            if (not isinstance(body_type, int) and not isinstance(body_type, BodyType)) or not isinstance(cas_part_id, int):
                self.log.format_error_with_message('outfit_body_parts contains non-integer variables body_type: {} cas_part_id: {}.'.format(body_type, cas_part_id), sim=self.sim_info, body_type=body_type, cas_part_id=cas_part_id, outfit_parts=outfit_parts)
                continue
            if cas_part_id == -1 or cas_part_id is None:
                self.log.format_with_message('Ignoring body_type with negative or None cas_part_id.', sim=self.sim_info, outfit_category_and_index=self.outfit_category_and_index, body_type=body_type, cas_part_id=cas_part_id)
                continue
            # noinspection PyUnresolvedReferences
            if isinstance(body_type, int) and body_type in BodyType.value_to_name:
                # noinspection PyUnresolvedReferences
                new_body_type = CommonResourceUtils.get_enum_by_name(BodyType.value_to_name[body_type], BodyType, default_value=-1)
                if new_body_type == -1:
                    new_body_type = body_type
            else:
                new_body_type = body_type
            cleaned_outfit_parts[new_body_type] = cas_part_id
        return cleaned_outfit_parts

    def _to_outfit_dictionary(self, body_types: Tuple[Union[BodyType, int]], part_ids: Tuple[int]) -> Dict[Union[BodyType, int], int]:
        return dict(zip(list(body_types), list(part_ids)))

    def _to_outfit_data(self, body_types: Tuple[Union[BodyType, int]], part_ids: Tuple[int]) -> FrozenSet[Union[BodyType, int]]:
        return frozenset(dict(zip(list(body_types), list(part_ids))).items())

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f'<{self.__class__.__name__}: OCI: {self.outfit_category_and_index}, Parts: {self._outfit_parts}>'
