"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Tuple, Iterator

from sims.genealogy_tracker import GenealogyTracker, FamilyRelationshipIndex, genealogy_caching
from sims.sim_info import SimInfo
from sims4communitylib.enums.relationship_bits_enum import CommonRelationshipBitId
from sims4communitylib.utils.sims.common_relationship_utils import CommonRelationshipUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimGenealogyUtils:
    """Utilities for managing and manipulating the Genealogy of Sims."""
    @classmethod
    def get_genealogy_tracker(cls, sim_info: SimInfo) -> Union[GenealogyTracker, None]:
        """get_genealogy_tracker(sim_info)

        Retrieve the Genealogy Tracker for a Sim.

        .. note: A Genealogy Tracker is essentially just the Family Tree Tracker of the Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The genealogy tracker of the Sim or None if not found.
        :rtype: Union[GenealogyTracker, None]
        """
        if sim_info is None:
            return None
        return sim_info._genealogy_tracker

    @classmethod
    def set_as_father_of(cls, sim_info: SimInfo, new_child_sim_info: SimInfo, propagate: bool = False) -> bool:
        """set_as_father_of(sim_info, new_child_sim_info, propagate=False)

        Set a Sim to be the Father of another Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param new_child_sim_info: The new child of Sim A.
        :type new_child_sim_info: SimInfo
        :param propagate: If set to True, the grandparent relations will also be updated. Default is False.
        :type propagate: bool, optional
        :return: True, if the relation was set successfully. False, if not.
        :rtype: bool
        """
        genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(new_child_sim_info)
        if genealogy_tracker is None:
            return False
        if propagate:
            genealogy_tracker.set_and_propagate_family_relation(FamilyRelationshipIndex.FATHER, sim_info)
        else:
            genealogy_tracker.set_family_relation(FamilyRelationshipIndex.FATHER, CommonSimUtils.get_sim_id(sim_info))
        return True

    @classmethod
    def set_as_mother_of(cls, sim_info: SimInfo, new_child_sim_info: SimInfo, propagate: bool = False) -> bool:
        """set_as_mother_of(sim_info, new_child_sim_info, propagate=False)

        Set a Sim to be the Mother of another Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param new_child_sim_info: The new child of Sim A.
        :type new_child_sim_info: SimInfo
        :param propagate: If set to True, the grandparent relations will also be updated. Default is False.
        :type propagate: bool, optional
        :return: True, if the relation was set successfully. False, if not.
        :rtype: bool
        """
        genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(new_child_sim_info)
        if genealogy_tracker is None:
            return False
        if propagate:
            genealogy_tracker.set_and_propagate_family_relation(FamilyRelationshipIndex.MOTHER, sim_info)
        else:
            genealogy_tracker.set_family_relation(FamilyRelationshipIndex.MOTHER, CommonSimUtils.get_sim_id(sim_info))
        return True

    @classmethod
    def set_as_fathers_father_of(cls, sim_info: SimInfo, new_grandchild_sim_info: SimInfo) -> bool:
        """set_as_fathers_father_of(sim_info, new_fathers_father_sim_info)

        Set a Sim to be the Fathers Father of another Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param new_grandchild_sim_info: The new grandchild of Sim A.
        :type new_grandchild_sim_info: SimInfo
        :return: True, if the relation was set successfully. False, if not.
        :rtype: bool
        """
        genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(new_grandchild_sim_info)
        if genealogy_tracker is None:
            return False
        genealogy_tracker.set_and_propagate_family_relation(FamilyRelationshipIndex.FATHERS_FATHER, sim_info)
        return True

    @classmethod
    def set_as_fathers_mother_of(cls, sim_info: SimInfo, new_grandchild_sim_info: SimInfo) -> bool:
        """set_as_fathers_mother_of(sim_info, new_grandchild_sim_info)

        Retrieve the Father of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param new_grandchild_sim_info: The new grandchild of Sim A.
        :type new_grandchild_sim_info: SimInfo
        :return: True, if the relation was set successfully. False, if not.
        :rtype: bool
        """
        genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(new_grandchild_sim_info)
        if genealogy_tracker is None:
            return False
        genealogy_tracker.set_family_relation(FamilyRelationshipIndex.FATHERS_MOM, sim_info)
        return True

    @classmethod
    def set_as_mothers_father_of(cls, sim_info: SimInfo, new_grandchild_sim_info: SimInfo) -> bool:
        """set_as_mothers_father_of(sim_info, new_grandchild_sim_info)

        Retrieve the Father of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param new_grandchild_sim_info: The new grandchild of Sim A.
        :type new_grandchild_sim_info: SimInfo
        :return: True, if the relation was set successfully. False, if not.
        :rtype: bool
        """
        genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(new_grandchild_sim_info)
        if genealogy_tracker is None:
            return False
        genealogy_tracker.set_and_propagate_family_relation(FamilyRelationshipIndex.MOTHERS_FATHER, sim_info)
        return True

    @classmethod
    def set_as_mothers_mother_of(cls, sim_info: SimInfo, new_grandchild_sim_info: SimInfo) -> bool:
        """set_as_mothers_mother_of(sim_info, new_grandchild_sim_info)

        Retrieve the Father of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param new_grandchild_sim_info: The new grandchild of Sim A.
        :type new_grandchild_sim_info: SimInfo
        :return: True, if the relation was set successfully. False, if not.
        :rtype: bool
        """
        genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(new_grandchild_sim_info)
        if genealogy_tracker is None:
            return False
        genealogy_tracker.set_and_propagate_family_relation(FamilyRelationshipIndex.MOTHERS_MOM, sim_info)
        return True

    @classmethod
    def has_father(cls, sim_info: SimInfo) -> bool:
        """has_father(sim_info)

        Determine if a Sim has a father.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has a father. False, if not.
        :rtype: bool
        """
        return cls.get_father_sim_info(sim_info) is not None

    @classmethod
    def has_mother(cls, sim_info: SimInfo) -> bool:
        """has_mother(sim_info)

        Determine if a Sim has a mother.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has a mother. False, if not.
        :rtype: bool
        """
        return cls.get_mother_sim_info(sim_info) is not None

    @classmethod
    def has_mothers_mother(cls, sim_info: SimInfo) -> bool:
        """has_grandmother(sim_info)

        Determine if a Sim has a Grandmother on the Mother's side, otherwise known as the Mother's Mother.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has a grandmother on the Mother's side. False, if not.
        :rtype: bool
        """
        return cls.get_mothers_mother_sim_info(sim_info) is not None

    @classmethod
    def has_mothers_father(cls, sim_info: SimInfo) -> bool:
        """has_mothers_father(sim_info)

        Determine if a Sim has a Grandfather on the Mother's side, otherwise known as the Mother's Father.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has a grandfather on the Mother's side. False, if not.
        :rtype: bool
        """
        return cls.get_mothers_father_sim_info(sim_info) is not None

    @classmethod
    def has_fathers_mother(cls, sim_info: SimInfo) -> bool:
        """has_fathers_mother(sim_info)

        Determine if a Sim has a Grandmother on the Father's side, otherwise known as the Father's Mother.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has a grandmother on the Father's side. False, if not.
        :rtype: bool
        """
        return cls.get_fathers_mother_sim_info(sim_info) is not None

    @classmethod
    def has_fathers_father(cls, sim_info: SimInfo) -> bool:
        """has_fathers_father(sim_info)

        Determine if a Sim has a Grandfather on the Father's side, otherwise known as the Father's Father.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has a grandfather on the Father's side. False, if not.
        :rtype: bool
        """
        return cls.get_fathers_father_sim_info(sim_info) is not None

    @classmethod
    def has_children(cls, sim_info: SimInfo) -> bool:
        """has_children(sim_info)

        Determine if a Sim has any children.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has any children. False, if not.
        :rtype: bool
        """
        return any(cls.get_children_sim_info_gen(sim_info))

    @classmethod
    def get_father_sim_info(cls, sim_info: SimInfo) -> Union[SimInfo, None]:
        """get_father_sim_info(sim_info)

        Retrieve the Father of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The father of the Sim or None if the Sim does not have a father.
        :rtype: Union[SimInfo, None]
        """
        return CommonSimGenealogyUtils._retrieve_relation_sim_info(sim_info, FamilyRelationshipIndex.FATHER)

    @classmethod
    def get_mother_sim_info(cls, sim_info: SimInfo) -> Union[SimInfo, None]:
        """get_mother_sim_info(sim_info)

        Retrieve the Mother of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The mother of the Sim or None if the Sim does not have a mother.
        :rtype: Union[SimInfo, None]
        """
        return CommonSimGenealogyUtils._retrieve_relation_sim_info(sim_info, FamilyRelationshipIndex.MOTHER)

    @classmethod
    def get_mothers_mother_sim_info(cls, sim_info: SimInfo) -> Union[SimInfo, None]:
        """get_mothers_mother_sim_info(sim_info)

        Retrieve the Grandmother of a Sim on their mothers side.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The grandmother of the Sim on their mothers side or None if the Sim does not have a mother or their mother does not have a mother.
        :rtype: Union[SimInfo, None]
        """
        return CommonSimGenealogyUtils._retrieve_relation_sim_info(sim_info, FamilyRelationshipIndex.MOTHERS_MOM)

    @classmethod
    def get_mothers_father_sim_info(cls, sim_info: SimInfo) -> Union[SimInfo, None]:
        """get_mothers_father_sim_info(sim_info)

        Retrieve the Grandfather of a Sim on their mothers side.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The grandfather of the Sim on their mothers side or None if the Sim does not have a mother or their mother does not have a father.
        :rtype: Union[SimInfo, None]
        """
        return CommonSimGenealogyUtils._retrieve_relation_sim_info(sim_info, FamilyRelationshipIndex.MOTHERS_FATHER)

    @classmethod
    def get_fathers_mother_sim_info(cls, sim_info: SimInfo) -> Union[SimInfo, None]:
        """get_fathers_mother_sim_info(sim_info)

        Retrieve the Grandmother of a Sim on their fathers side.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The grandmother of the Sim on their fathers side or None if the Sim does not have a father or their father does not have a mother.
        :rtype: Union[SimInfo, None]
        """
        return CommonSimGenealogyUtils._retrieve_relation_sim_info(sim_info, FamilyRelationshipIndex.FATHERS_MOM)

    @classmethod
    def get_fathers_father_sim_info(cls, sim_info: SimInfo) -> Union[SimInfo, None]:
        """get_fathers_father_sim_info(sim_info)

        Retrieve the Grandfather of a Sim on their fathers side.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The grandfather of the Sim on their fathers side or None if the Sim does not have a father or their father does not have a mother.
        :rtype: Union[SimInfo, None]
        """
        return CommonSimGenealogyUtils._retrieve_relation_sim_info(sim_info, FamilyRelationshipIndex.FATHERS_FATHER)

    @classmethod
    def get_children_sim_info_gen(cls, sim_info: SimInfo) -> Iterator[SimInfo]:
        """get_children_sim_info_gen(sim_info)

        Get the blood related children of a Sim.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: An iterable of children the specified Sim is blood related to.
        :rtype: Iterator[SimInfo]
        """
        with genealogy_caching():
            yield from cls.get_genealogy_tracker(sim_info).get_child_sim_infos_gen()

    @classmethod
    def remove_family_relations_with(cls, sim_info_a: SimInfo, sim_info_b: SimInfo, remove_from_family_tree: bool=True) -> bool:
        """remove_family_relations_with(sim_info_a, sim_info_b, remove_from_family_tree=True)

        Remove the family relations Sim A has with Sim B and the family relations Sim B has with Sim A.

        :param sim_info_a: An instance of a Sim.
        :type sim_info_a: SimInfo
        :param sim_info_b: The Sim to remove from the family of Sim A.
        :type sim_info_b: SimInfo
        :param remove_from_family_tree: If True, Sim A will remove Sim B from their family tree as well. If False, the family tree of Sim A will not be modified. Default is True.
        :type remove_from_family_tree: bool, optional
        :return: True, if the family relations between the Sims was removed successfully. False, if not.
        :rtype: bool
        """
        if remove_from_family_tree:
            if CommonSimGenealogyUtils.is_father_of(sim_info_a, sim_info_b):
                CommonSimGenealogyUtils.remove_father_relation(sim_info_b)
            if CommonSimGenealogyUtils.is_mother_of(sim_info_a, sim_info_b):
                CommonSimGenealogyUtils.remove_mother_relation(sim_info_b)
            if CommonSimGenealogyUtils.is_fathers_father_of(sim_info_a, sim_info_b):
                CommonSimGenealogyUtils.remove_fathers_father_relation(sim_info_b)
            if CommonSimGenealogyUtils.is_fathers_mother_of(sim_info_a, sim_info_b):
                CommonSimGenealogyUtils.remove_fathers_mother_relation(sim_info_b)
            if CommonSimGenealogyUtils.is_mothers_father_of(sim_info_a, sim_info_b):
                CommonSimGenealogyUtils.remove_mothers_father_relation(sim_info_b)
            if CommonSimGenealogyUtils.is_mothers_mother_of(sim_info_a, sim_info_b):
                CommonSimGenealogyUtils.remove_mothers_mother_relation(sim_info_b)

        # noinspection PyTypeChecker
        relationship_bit_ids: Tuple[CommonRelationshipBitId] = (
            CommonRelationshipBitId.FAMILY_AUNT_UNCLE,
            CommonRelationshipBitId.FAMILY_SON_DAUGHTER,
            CommonRelationshipBitId.FAMILY_COUSIN,
            CommonRelationshipBitId.FAMILY_PARENT,
            CommonRelationshipBitId.FAMILY_GRANDCHILD,
            CommonRelationshipBitId.FAMILY_GRANDPARENT,
            CommonRelationshipBitId.FAMILY_HUSBAND_WIFE,
            CommonRelationshipBitId.FAMILY_NIECE_NEPHEW,
            CommonRelationshipBitId.FAMILY_BROTHER_SISTER,
            CommonRelationshipBitId.FAMILY_STEP_SIBLING
        )

        for relationship_bit_id in relationship_bit_ids:
            CommonRelationshipUtils.remove_relationship_bit(sim_info_a, sim_info_b, relationship_bit_id)
        return True

    @classmethod
    def remove_father_relation(cls, sim_info: SimInfo) -> bool:
        """remove_father_relation(sim_info)

        Remove the Father of a Sim from their Family Tree.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the father of the Sim has been removed. False, if not.
        :rtype: bool
        """
        genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(sim_info)
        if genealogy_tracker is None:
            return False
        genealogy_tracker.clear_family_relation(FamilyRelationshipIndex.FATHER)
        return True

    @classmethod
    def remove_mother_relation(cls, sim_info: SimInfo) -> bool:
        """remove_mother_relation(sim_info)

        Remove the Mother of a Sim from their Family Tree.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the mother of the Sim has been removed. False, if not.
        :rtype: bool
        """
        genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(sim_info)
        if genealogy_tracker is None:
            return False
        genealogy_tracker.clear_family_relation(FamilyRelationshipIndex.MOTHER)
        return True

    @classmethod
    def remove_fathers_father_relation(cls, sim_info: SimInfo) -> bool:
        """remove_fathers_father_relation(sim_info)

        Remove the relation of a Sim to their Grandfather on their fathers side from their Family Tree.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the grandfather of the Sim has been removed. False, if not.
        :rtype: bool
        """
        genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(sim_info)
        if genealogy_tracker is None:
            return False
        genealogy_tracker.clear_family_relation(FamilyRelationshipIndex.FATHERS_FATHER)
        return True

    @classmethod
    def remove_fathers_mother_relation(cls, sim_info: SimInfo) -> bool:
        """remove_fathers_mother_relation(sim_info)

        Remove the relation of a Sim to their Grandmother on their fathers side from their Family Tree.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the grandmother of the Sim has been removed. False, if not.
        :rtype: bool
        """
        genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(sim_info)
        if genealogy_tracker is None:
            return False
        genealogy_tracker.clear_family_relation(FamilyRelationshipIndex.FATHERS_MOM)
        return True

    @classmethod
    def remove_mothers_father_relation(cls, sim_info: SimInfo) -> bool:
        """remove_mothers_father_relation(sim_info)

        Remove the Father of the Mother of a Sim from their Family Tree.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the father of the mother of the Sim has been removed. False, if not.
        :rtype: bool
        """
        genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(sim_info)
        if genealogy_tracker is None:
            return False
        genealogy_tracker.clear_family_relation(FamilyRelationshipIndex.MOTHERS_FATHER)
        return True

    @classmethod
    def remove_mothers_mother_relation(cls, sim_info: SimInfo) -> bool:
        """remove_mothers_mother_relation(sim_info)

        Remove the relation of a Sim to their Grandmother on their mothers side from their Family Tree.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the grandmother of the Sim has been removed. False, if not.
        :rtype: bool
        """
        genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(sim_info)
        if genealogy_tracker is None:
            return False
        genealogy_tracker.clear_family_relation(FamilyRelationshipIndex.MOTHERS_MOM)
        return True

    @classmethod
    def is_father_of(cls, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        """is_father_of(sim_info_a, sim_info_b)

        Determine if Sim A is the father of Sim B.

        :param sim_info_a: An instance of a Sim.
        :type sim_info_a: SimInfo
        :param sim_info_b: An instance of a Sim.
        :type sim_info_b: SimInfo
        :return: True, if Sim A is the father of Sim B. False, if not.
        :rtype: bool
        """
        parent_sim_info_b = CommonSimGenealogyUtils.get_father_sim_info(sim_info_b)
        return sim_info_a is parent_sim_info_b

    @classmethod
    def is_mother_of(cls, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        """is_mother_of(sim_info_a, sim_info_b)

        Determine if Sim A is the mother of Sim B.

        :param sim_info_a: An instance of a Sim.
        :type sim_info_a: SimInfo
        :param sim_info_b: An instance of a Sim.
        :type sim_info_b: SimInfo
        :return: True, if Sim A is the mother of Sim B. False, if not.
        :rtype: bool
        """
        parent_sim_info_b = CommonSimGenealogyUtils.get_mother_sim_info(sim_info_b)
        return sim_info_a is parent_sim_info_b

    @classmethod
    def is_fathers_father_of(cls, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        """is_fathers_father_of(sim_info_a, sim_info_b)

        Determine if Sim A is the grandfather of Sim B on the fathers side of Sim B.

        :param sim_info_a: An instance of a Sim.
        :type sim_info_a: SimInfo
        :param sim_info_b: An instance of a Sim.
        :type sim_info_b: SimInfo
        :return: True, if Sim A is the grandfather of Sim B on their fathers side. False, if not.
        :rtype: bool
        """
        grand_parent_sim_info_b = CommonSimGenealogyUtils.get_fathers_father_sim_info(sim_info_b)
        return sim_info_a is grand_parent_sim_info_b

    @classmethod
    def is_fathers_mother_of(cls, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        """is_fathers_mother_of(sim_info_a, sim_info_b)

        Determine if Sim A is the grandmother of Sim B on the fathers side of Sim B.

        :param sim_info_a: An instance of a Sim.
        :type sim_info_a: SimInfo
        :param sim_info_b: An instance of a Sim.
        :type sim_info_b: SimInfo
        :return: True, if Sim A is the grandmother of Sim B on their fathers side. False, if not.
        :rtype: bool
        """
        grand_parent_sim_info_b = CommonSimGenealogyUtils.get_fathers_mother_sim_info(sim_info_b)
        return sim_info_a is grand_parent_sim_info_b

    @classmethod
    def is_mothers_father_of(cls, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        """is_mothers_father_of(sim_info_a, sim_info_b)

        Determine if Sim A is the grandfather of Sim B on the mothers side of Sim B.

        :param sim_info_a: An instance of a Sim.
        :type sim_info_a: SimInfo
        :param sim_info_b: An instance of a Sim.
        :type sim_info_b: SimInfo
        :return: True, if Sim A is the grandfather of Sim B on their mothers side. False, if not.
        :rtype: bool
        """
        grand_parent_sim_info_b = CommonSimGenealogyUtils.get_mothers_father_sim_info(sim_info_b)
        return sim_info_a is grand_parent_sim_info_b

    @classmethod
    def is_mothers_mother_of(cls, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        """is_mothers_mother_of(sim_info_a, sim_info_b)

        Determine if Sim A is the grandmother of Sim B on the mothers side of Sim B.

        :param sim_info_a: An instance of a Sim.
        :type sim_info_a: SimInfo
        :param sim_info_b: An instance of a Sim.
        :type sim_info_b: SimInfo
        :return: True, if Sim A is the grandmother of Sim B on their mothers side. False, if not.
        :rtype: bool
        """
        grand_parent_sim_info_b = CommonSimGenealogyUtils.get_mothers_mother_sim_info(sim_info_b)
        return sim_info_a is grand_parent_sim_info_b

    @classmethod
    def has_father(cls, sim_info: SimInfo) -> bool:
        """has_father(sim_info)

        Determine if a Sim has a father.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has a father. False, if not.
        :rtype: bool
        """
        return CommonSimGenealogyUtils.get_father_sim_info(sim_info) is not None

    @classmethod
    def has_mother(cls, sim_info: SimInfo) -> bool:
        """has_mother(sim_info)

        Determine if Sim A is the mother of Sim B.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has a mother. False, if not.
        :rtype: bool
        """
        return CommonSimGenealogyUtils.get_mother_sim_info(sim_info) is not None

    @classmethod
    def has_grandfather_on_fathers_side(cls, sim_info: SimInfo) -> bool:
        """has_grandfather_on_fathers_side(sim_info)

        Determine if a Sim has a grandfather on the fathers side.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has a grandfather on the fathers side. False, if not.
        :rtype: bool
        """
        return CommonSimGenealogyUtils.get_fathers_father_sim_info(sim_info) is not None

    @classmethod
    def has_grandmother_on_fathers_side(cls, sim_info: SimInfo) -> bool:
        """has_grandmother_on_fathers_side(sim_info)

        Determine if a Sim has a grandmother on the fathers side.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has a grandmother on the fathers side. False, if not.
        :rtype: bool
        """
        return CommonSimGenealogyUtils.get_fathers_mother_sim_info(sim_info) is not None

    @classmethod
    def has_grandfather_on_mothers_side(cls, sim_info: SimInfo) -> bool:
        """has_grandfather_on_mothers_side(sim_info)

        Determine if a Sim has a grandfather on the mothers side.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has a grandfather on the mothers side. False, if not.
        :rtype: bool
        """
        return CommonSimGenealogyUtils.get_mothers_father_sim_info(sim_info) is not None

    @classmethod
    def has_grandmother_on_mothers_side(cls, sim_info: SimInfo) -> bool:
        """has_grandmother_on_mothers_side(sim_info)

        Determine if a Sim has a grandmother on the mothers side.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has a grandmother on the mothers side. False, if not.
        :rtype: bool
        """
        return CommonSimGenealogyUtils.get_mothers_mother_sim_info(sim_info) is not None

    @classmethod
    def _retrieve_relation_sim_info(cls, sim_info: SimInfo, relationship_index: FamilyRelationshipIndex) -> Union[SimInfo, None]:
        return CommonSimUtils.get_sim_info(CommonSimGenealogyUtils._retrieve_relation_sim_id(sim_info, relationship_index))

    @classmethod
    def _retrieve_relation_sim_id(cls, sim_info: SimInfo, relationship_index: FamilyRelationshipIndex) -> Union[SimInfo, None]:
        genealogy_tracker = CommonSimGenealogyUtils.get_genealogy_tracker(sim_info)
        if genealogy_tracker is None:
            return None
        if relationship_index not in genealogy_tracker._family_relations:
            return None
        return genealogy_tracker.get_relation(relationship_index)
