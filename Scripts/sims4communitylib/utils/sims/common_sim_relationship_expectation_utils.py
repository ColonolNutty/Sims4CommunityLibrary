"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils


class CommonSimRelationshipExpectationUtils:
    """ Utilities for Sim relationship expectations. """
    @classmethod
    def is_open_to_change(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_open_to_change(sim_info)

        Determine if the jealousy triggers of a Sim can be changed through talking.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of the test. True, if the test passes. False, if not.
        :rtype: CommonTestResult
        """
        if CommonTraitUtils.has_trait(sim_info, CommonTraitId.RELATIONSHIP_EXPECTATIONS_OPEN_TO_CHANGE_NO):
            return CommonTestResult(False, reason=f'{sim_info} is not open to relationship expectation changes.', tooltip_text=CommonStringId.S4CL_SIM_IS_NOT_OPEN_TO_RELATIONSHIP_EXPECTATION_CHANGES, tooltip_tokens=(sim_info,))
        if CommonTraitUtils.has_trait(sim_info, CommonTraitId.RELATIONSHIP_EXPECTATIONS_OPEN_TO_CHANGE_YES):
            return CommonTestResult(True, reason=f'{sim_info} is open to relationship expectation changes.', tooltip_text=CommonStringId.S4CL_SIM_IS_OPEN_TO_RELATIONSHIP_EXPECTATION_CHANGES, tooltip_tokens=(sim_info,))
        return CommonTestResult(True, reason=f'{sim_info} is open to relationship expectation changes.', tooltip_text=CommonStringId.S4CL_SIM_IS_OPEN_TO_RELATIONSHIP_EXPECTATION_CHANGES, tooltip_tokens=(sim_info,))

    @classmethod
    def is_not_open_to_change(cls, sim_info: SimInfo) -> CommonTestResult:
        """is_not_open_to_change(sim_info)

        Determine if the jealousy triggers of a Sim can not be changed through talking.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of the test. True, if the test passes. False, if not.
        :rtype: CommonTestResult
        """
        if CommonTraitUtils.has_trait(sim_info, CommonTraitId.RELATIONSHIP_EXPECTATIONS_OPEN_TO_CHANGE_YES):
            return CommonTestResult(False, reason=f'{sim_info} is open to relationship expectation changes.', tooltip_text=CommonStringId.S4CL_SIM_IS_OPEN_TO_RELATIONSHIP_EXPECTATION_CHANGES, tooltip_tokens=(sim_info,))
        if CommonTraitUtils.has_trait(sim_info, CommonTraitId.RELATIONSHIP_EXPECTATIONS_OPEN_TO_CHANGE_NO):
            return CommonTestResult(True, reason=f'{sim_info} is not open to relationship expectation changes.', tooltip_text=CommonStringId.S4CL_SIM_IS_NOT_OPEN_TO_RELATIONSHIP_EXPECTATION_CHANGES, tooltip_tokens=(sim_info,))
        return CommonTestResult(False, reason=f'{sim_info} is open to relationship expectation changes.', tooltip_text=CommonStringId.S4CL_SIM_IS_OPEN_TO_RELATIONSHIP_EXPECTATION_CHANGES, tooltip_tokens=(sim_info,))

    @classmethod
    def set_open_to_change(cls, sim_info: SimInfo, is_open_to_change: bool) -> CommonExecutionResult:
        """set_open_to_change(sim_info, is_open_to_change)

        Set if the jealousy triggers of a Sim can be changed through talking.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param is_open_to_change: Set True to indicate a Sim is open to change. Set False, if not.
        :type is_open_to_change: bool
        :return: The result of the test. True, if the test passes. False, if not.
        :rtype: CommonTestResult
        """
        if is_open_to_change:
            to_remove_trait = CommonTraitId.RELATIONSHIP_EXPECTATIONS_OPEN_TO_CHANGE_NO
            to_add_trait = CommonTraitId.RELATIONSHIP_EXPECTATIONS_OPEN_TO_CHANGE_YES
        else:
            to_remove_trait = CommonTraitId.RELATIONSHIP_EXPECTATIONS_OPEN_TO_CHANGE_YES
            to_add_trait = CommonTraitId.RELATIONSHIP_EXPECTATIONS_OPEN_TO_CHANGE_NO
        CommonTraitUtils.remove_trait(sim_info, to_remove_trait)
        return CommonTraitUtils.add_trait(sim_info, to_add_trait)

    @classmethod
    def has_emotional_exclusivity(cls, sim_info: SimInfo) -> CommonTestResult:
        """has_emotional_exclusivity(sim_info)

        Determine if the Sim has emotional exclusivity.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of the test. True, if the test passes. False, if not.
        :rtype: CommonTestResult
        """
        if CommonTraitUtils.has_trait(sim_info, CommonTraitId.RELATIONSHIP_EXPECTATIONS_EMOTIONAL_EXCLUSIVITY_NO):
            return CommonTestResult(False, reason=f'{sim_info} does not have emotional exclusivity.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_EMOTIONAL_EXCLUSIVITY, tooltip_tokens=(sim_info,))
        if CommonTraitUtils.has_trait(sim_info, CommonTraitId.RELATIONSHIP_EXPECTATIONS_EMOTIONAL_EXCLUSIVITY_YES):
            return CommonTestResult(True, reason=f'{sim_info} has emotional exclusivity.', tooltip_text=CommonStringId.S4CL_SIM_HAS_EMOTIONAL_EXCLUSIVITY, tooltip_tokens=(sim_info,))
        return CommonTestResult(True, reason=f'{sim_info} has emotional exclusivity.', tooltip_text=CommonStringId.S4CL_SIM_HAS_EMOTIONAL_EXCLUSIVITY, tooltip_tokens=(sim_info,))

    @classmethod
    def does_not_have_emotional_exclusivity(cls, sim_info: SimInfo) -> CommonTestResult:
        """does_not_have_emotional_exclusivity(sim_info)

        Determine if the Sim does not have emotional exclusivity.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of the test. True, if the test passes. False, if not.
        :rtype: CommonTestResult
        """
        if CommonTraitUtils.has_trait(sim_info, CommonTraitId.RELATIONSHIP_EXPECTATIONS_EMOTIONAL_EXCLUSIVITY_YES):
            return CommonTestResult(False, reason=f'{sim_info} has emotional exclusivity.', tooltip_text=CommonStringId.S4CL_SIM_HAS_EMOTIONAL_EXCLUSIVITY, tooltip_tokens=(sim_info,))
        if CommonTraitUtils.has_trait(sim_info, CommonTraitId.RELATIONSHIP_EXPECTATIONS_EMOTIONAL_EXCLUSIVITY_NO):
            return CommonTestResult(True, reason=f'{sim_info} does not have emotional exclusivity.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_EMOTIONAL_EXCLUSIVITY, tooltip_tokens=(sim_info,))
        return CommonTestResult(False, reason=f'{sim_info} has emotional exclusivity.', tooltip_text=CommonStringId.S4CL_SIM_HAS_EMOTIONAL_EXCLUSIVITY, tooltip_tokens=(sim_info,))

    @classmethod
    def set_emotional_exclusivity(cls, sim_info: SimInfo, has_emotional_exclusivity: bool) -> CommonExecutionResult:
        """set_emotional_exclusivity(sim_info, has_emotional_exclusivity)

        Set if a Sim has emotional exclusivity with their partner.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param has_emotional_exclusivity: Set True to indicate a Sim has emotional exclusivity with their partner. Set False, if not.
        :type has_emotional_exclusivity: bool
        :return: The result of the test. True, if the test passes. False, if not.
        :rtype: CommonTestResult
        """
        if has_emotional_exclusivity:
            to_remove_trait = CommonTraitId.RELATIONSHIP_EXPECTATIONS_EMOTIONAL_EXCLUSIVITY_NO
            to_add_trait = CommonTraitId.RELATIONSHIP_EXPECTATIONS_EMOTIONAL_EXCLUSIVITY_YES
        else:
            to_remove_trait = CommonTraitId.RELATIONSHIP_EXPECTATIONS_EMOTIONAL_EXCLUSIVITY_YES
            to_add_trait = CommonTraitId.RELATIONSHIP_EXPECTATIONS_EMOTIONAL_EXCLUSIVITY_NO
        CommonTraitUtils.remove_trait(sim_info, to_remove_trait)
        return CommonTraitUtils.add_trait(sim_info, to_add_trait)

    @classmethod
    def has_physical_exclusivity(cls, sim_info: SimInfo) -> CommonTestResult:
        """has_physical_exclusivity(sim_info)

        Determine if the Sim has physical exclusivity.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of the test. True, if the test passes. False, if not.
        :rtype: CommonTestResult
        """
        if CommonTraitUtils.has_trait(sim_info, CommonTraitId.RELATIONSHIP_EXPECTATIONS_PHYSICAL_EXCLUSIVITY_NO):
            return CommonTestResult(False, reason=f'{sim_info} does not have physical exclusivity.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_PHYSICAL_EXCLUSIVITY, tooltip_tokens=(sim_info,))
        if CommonTraitUtils.has_trait(sim_info, CommonTraitId.RELATIONSHIP_EXPECTATIONS_PHYSICAL_EXCLUSIVITY_YES):
            return CommonTestResult(True, reason=f'{sim_info} has physical exclusivity.', tooltip_text=CommonStringId.S4CL_SIM_HAS_PHYSICAL_EXCLUSIVITY, tooltip_tokens=(sim_info,))
        return CommonTestResult(True, reason=f'{sim_info} has physical exclusivity.', tooltip_text=CommonStringId.S4CL_SIM_HAS_PHYSICAL_EXCLUSIVITY, tooltip_tokens=(sim_info,))

    @classmethod
    def does_not_have_physical_exclusivity(cls, sim_info: SimInfo) -> CommonTestResult:
        """does_not_have_physical_exclusivity(sim_info)

        Determine if the Sim does not have physical exclusivity.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of the test. True, if the test passes. False, if not.
        :rtype: CommonTestResult
        """
        if CommonTraitUtils.has_trait(sim_info, CommonTraitId.RELATIONSHIP_EXPECTATIONS_PHYSICAL_EXCLUSIVITY_YES):
            return CommonTestResult(False, reason=f'{sim_info} has physical exclusivity.', tooltip_text=CommonStringId.S4CL_SIM_HAS_PHYSICAL_EXCLUSIVITY, tooltip_tokens=(sim_info,))
        if CommonTraitUtils.has_trait(sim_info, CommonTraitId.RELATIONSHIP_EXPECTATIONS_PHYSICAL_EXCLUSIVITY_NO):
            return CommonTestResult(True, reason=f'{sim_info} does not have physical exclusivity.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_PHYSICAL_EXCLUSIVITY, tooltip_tokens=(sim_info,))
        return CommonTestResult(False, reason=f'{sim_info} has physical exclusivity.', tooltip_text=CommonStringId.S4CL_SIM_HAS_PHYSICAL_EXCLUSIVITY, tooltip_tokens=(sim_info,))

    @classmethod
    def set_physical_exclusivity(cls, sim_info: SimInfo, has_physical_exclusivity: bool) -> CommonExecutionResult:
        """set_physical_exclusivity(sim_info, has_physical_exclusivity)

        Set if a Sim has physical exclusivity with their partner.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param has_physical_exclusivity: Set True to indicate a Sim has physical exclusivity with their partner. Set False, if not.
        :type has_physical_exclusivity: bool
        :return: The result of the test. True, if the test passes. False, if not.
        :rtype: CommonTestResult
        """
        if has_physical_exclusivity:
            to_remove_trait = CommonTraitId.RELATIONSHIP_EXPECTATIONS_PHYSICAL_EXCLUSIVITY_NO
            to_add_trait = CommonTraitId.RELATIONSHIP_EXPECTATIONS_PHYSICAL_EXCLUSIVITY_YES
        else:
            to_remove_trait = CommonTraitId.RELATIONSHIP_EXPECTATIONS_PHYSICAL_EXCLUSIVITY_YES
            to_add_trait = CommonTraitId.RELATIONSHIP_EXPECTATIONS_PHYSICAL_EXCLUSIVITY_NO
        CommonTraitUtils.remove_trait(sim_info, to_remove_trait)
        return CommonTraitUtils.add_trait(sim_info, to_add_trait)

    @classmethod
    def has_woohoo_exclusivity(cls, sim_info: SimInfo) -> CommonTestResult:
        """has_woohoo_exclusivity(sim_info)

        Determine if the Sim has woohoo exclusivity.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of the test. True, if the test passes. False, if not.
        :rtype: CommonTestResult
        """
        if CommonTraitUtils.has_trait(sim_info, CommonTraitId.RELATIONSHIP_EXPECTATIONS_WOOHOO_EXCLUSIVITY_NO):
            return CommonTestResult(False, reason=f'{sim_info} does not have woohoo exclusivity.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_WOOHOO_EXCLUSIVITY, tooltip_tokens=(sim_info,))
        if CommonTraitUtils.has_trait(sim_info, CommonTraitId.RELATIONSHIP_EXPECTATIONS_WOOHOO_EXCLUSIVITY_YES):
            return CommonTestResult(True, reason=f'{sim_info} has woohoo exclusivity.', tooltip_text=CommonStringId.S4CL_SIM_HAS_WOOHOO_EXCLUSIVITY, tooltip_tokens=(sim_info,))
        return CommonTestResult(True, reason=f'{sim_info} has woohoo exclusivity.', tooltip_text=CommonStringId.S4CL_SIM_HAS_WOOHOO_EXCLUSIVITY, tooltip_tokens=(sim_info,))

    @classmethod
    def does_not_have_woohoo_exclusivity(cls, sim_info: SimInfo) -> CommonTestResult:
        """does_not_have_woohoo_exclusivity(sim_info)

        Determine if the Sim does not have woohoo exclusivity.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The result of the test. True, if the test passes. False, if not.
        :rtype: CommonTestResult
        """
        if CommonTraitUtils.has_trait(sim_info, CommonTraitId.RELATIONSHIP_EXPECTATIONS_WOOHOO_EXCLUSIVITY_YES):
            return CommonTestResult(False, reason=f'{sim_info} has woohoo exclusivity.', tooltip_text=CommonStringId.S4CL_SIM_HAS_WOOHOO_EXCLUSIVITY, tooltip_tokens=(sim_info,))
        if CommonTraitUtils.has_trait(sim_info, CommonTraitId.RELATIONSHIP_EXPECTATIONS_WOOHOO_EXCLUSIVITY_NO):
            return CommonTestResult(True, reason=f'{sim_info} does not have woohoo exclusivity.', tooltip_text=CommonStringId.S4CL_SIM_DOES_NOT_HAVE_WOOHOO_EXCLUSIVITY, tooltip_tokens=(sim_info,))
        return CommonTestResult(False, reason=f'{sim_info} has woohoo exclusivity.', tooltip_text=CommonStringId.S4CL_SIM_HAS_WOOHOO_EXCLUSIVITY, tooltip_tokens=(sim_info,))

    @classmethod
    def set_woohoo_exclusivity(cls, sim_info: SimInfo, has_woohoo_exclusivity: bool) -> CommonExecutionResult:
        """set_woohoo_exclusivity(sim_info, has_woohoo_exclusivity)

        Set if a Sim has woohoo exclusivity with their partner.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param has_woohoo_exclusivity: Set True to indicate a Sim has woohoo exclusivity with their partner. Set False, if not.
        :type has_woohoo_exclusivity: bool
        :return: The result of the test. True, if the test passes. False, if not.
        :rtype: CommonTestResult
        """
        if has_woohoo_exclusivity:
            to_remove_trait = CommonTraitId.RELATIONSHIP_EXPECTATIONS_WOOHOO_EXCLUSIVITY_NO
            to_add_trait = CommonTraitId.RELATIONSHIP_EXPECTATIONS_WOOHOO_EXCLUSIVITY_YES
        else:
            to_remove_trait = CommonTraitId.RELATIONSHIP_EXPECTATIONS_WOOHOO_EXCLUSIVITY_YES
            to_add_trait = CommonTraitId.RELATIONSHIP_EXPECTATIONS_WOOHOO_EXCLUSIVITY_NO
        CommonTraitUtils.remove_trait(sim_info, to_remove_trait)
        return CommonTraitUtils.add_trait(sim_info, to_add_trait)
