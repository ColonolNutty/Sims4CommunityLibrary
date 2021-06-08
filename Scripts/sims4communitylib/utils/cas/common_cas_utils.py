"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from typing import Tuple, Union, Any

from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.sim.cas.common_sim_outfit_io import CommonSimOutfitIO
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils

# ReadTheDocs
ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'

if not ON_RTD:
    from server_commands.argument_helpers import OptionalTargetParam
    from sims.outfits.outfit_enums import OutfitCategory, BodyType
    from sims.sim_info import SimInfo
    from sims4.commands import Command, CheatOutput, CommandType
else:
    class OptionalTargetParam:
        pass

    class OutfitCategory:
        pass

    class BodyType:
        NONE = 0

    class SimInfo:
        pass

    class Command:
        pass

    class CheatOutput:
        pass

    class CommandType:
        pass

log = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 's4cl_common_cas_utils')


class CommonCASUtils:
    """Utilities for manipulating the CAS parts of Sims.

    """

    @staticmethod
    def is_cas_part_loaded(cas_part_id: int) -> bool:
        """is_cas_part_loaded(cas_part_id)

        Determine if a CAS part is loaded within the game.

        .. note:: If the CAS part is part of a package that is not installed, it will be considered as not loaded.

        .. note:: A CAS part is considered as "loaded" when the BodyType it has can be found within the sims.outfits.outfit_enums.BodyType enum.

        :param cas_part_id: The Decimal identifier of a CAS part.
        :type cas_part_id: int
        :return: True if the CAS part is loaded within the game, False if not.
        :rtype: bool
        """
        body_type = CommonCASUtils.get_body_type_of_cas_part(cas_part_id)
        if body_type is None:
            return False
        return body_type > 0

    @staticmethod
    def get_body_type_of_cas_part(cas_part_id: int) -> Union[BodyType, int]:
        """get_body_type_of_cas_part(cas_part_id)

        Retrieve the BodyType of a CAS part.

        .. note:: Some Body Types don't appear in the BodyType enum.

        :param cas_part_id: The decimal identifier of a CAS part.
        :type cas_part_id: int
        :return: The default BodyType of the CAS part or an int if the Body Type is not within the BodyType enum.
        :rtype: Union[BodyType, int]
        """
        from cas.cas import get_caspart_bodytype
        body_type = get_caspart_bodytype(cas_part_id)
        if body_type not in BodyType:
            return body_type
        # noinspection PyBroadException
        try:
            return BodyType(body_type)
        except:
            return body_type

    @staticmethod
    def attach_cas_part_to_sim(sim_info: SimInfo, cas_part_id: int, body_type: Union[BodyType, int]=BodyType.NONE, outfit_category_and_index: Union[Tuple[OutfitCategory, int], None]=None) -> bool:
        """attach_cas_part_to_sim(sim_info, cas_part_id, body_type=BodyType.NONE, outfit_category_and_index=None)

        Add a CAS part at the specified BodyType to the Sims outfit.

        :param sim_info: The SimInfo of a Sim to add the CAS part to.
        :type sim_info: SimInfo
        :param cas_part_id: The decimal identifier of a CAS part to attach to the Sim.
        :type cas_part_id: int
        :param body_type: The BodyType the CAS part will be attached to. If no value is provided or it is None, the BodyType of the CAS part itself will be used.
        :type body_type: Union[BodyType, int], optional
        :param outfit_category_and_index: The outfit category and index of the Sims outfit to modify. If no value is provided, the Sims current outfit will be used.
        :type outfit_category_and_index: Union[Tuple[OutfitCategory, int], None], optional
        :return: True if the CAS part was successfully attached to the Sim. False if the CAS part was not successfully attached to the Sim.
        :rtype: bool
        """
        from sims4communitylib.services.sim.cas.common_sim_outfit_io import CommonSimOutfitIO
        if cas_part_id == -1 or cas_part_id is None:
            raise RuntimeError('No cas_part_id was provided.')
        log.format_with_message('Attempting to attach CAS part to Sim', sim=sim_info, cas_part_id=cas_part_id, body_type=body_type, outfit_category_and_index=outfit_category_and_index)
        outfit_io = CommonSimOutfitIO(sim_info, outfit_category_and_index=outfit_category_and_index)
        outfit_io.attach_cas_part(cas_part_id, body_type=body_type)
        return outfit_io.apply()

    @staticmethod
    def detach_cas_part_from_sim(sim_info: SimInfo, cas_part_id: int, body_type: Union[BodyType, int, None]=BodyType.NONE, outfit_category_and_index: Union[Tuple[OutfitCategory, int], None]=None) -> bool:
        """detach_cas_part_from_sim(sim_info, cas_part_id, body_type=BodyType.NONE, outfit_category_and_index=None)

        Remove a CAS part at the specified BodyType from the Sims outfit.

        :param sim_info: The SimInfo of a Sim to remove the CAS part from.
        :type sim_info: SimInfo
        :param cas_part_id: The decimal identifier of a CAS part to detach from the Sim.
        :type cas_part_id: int
        :param body_type: The BodyType the CAS part will be detached from. If no value is provided, the BodyType of the CAS part itself will be used. If set to None, the CAS part will be removed from all BodyTypes.
        :type body_type: Union[BodyType, int, None], optional
        :param outfit_category_and_index: The outfit category and index of the Sims outfit to modify. If no value is provided, the Sims current outfit will be used.
        :type outfit_category_and_index: Union[Tuple[OutfitCategory, int], None], optional
        :return: True if the CAS part was successfully detached from the Sim. False if the CAS part was not successfully detached from the Sim.
        :rtype: bool
        """
        from sims4communitylib.services.sim.cas.common_sim_outfit_io import CommonSimOutfitIO
        if cas_part_id == -1 or cas_part_id is None:
            raise RuntimeError('No cas_part_id was provided.')
        log.format_with_message('Attempting to remove CAS part from Sim', sim=sim_info, cas_part_id=cas_part_id, body_type=body_type, outfit_category_and_index=outfit_category_and_index)
        outfit_io = CommonSimOutfitIO(sim_info, outfit_category_and_index=outfit_category_and_index)
        if body_type is None:
            outfit_io.detach_cas_part(cas_part_id)
        elif body_type == BodyType.NONE:
            body_type = CommonCASUtils.get_body_type_of_cas_part(cas_part_id)
            if outfit_io.get_cas_part_at_body_type(body_type) != cas_part_id:
                return False
            outfit_io.detach_body_type(body_type)
        return outfit_io.apply()

    @staticmethod
    def has_cas_part_attached(sim_info: SimInfo, cas_part_id: int, body_type: Union[BodyType, int, None]=BodyType.NONE, outfit_category_and_index: Tuple[OutfitCategory, int]=None) -> bool:
        """has_cas_part_attached(sim_info, cas_part_id, body_type=BodyType.NONE, outfit_category_and_index=None)

        Determine if a Sim has the specified CAS part attached to their outfit.

        :param sim_info: The SimInfo of the Sim to check.
        :type sim_info: SimInfo
        :param cas_part_id: A decimal identifier of the CAS part to locate.
        :type cas_part_id: int
        :param body_type: The BodyType the CAS part will be located at. If no value is provided, it defaults to the BodyType of the CAS part itself. If set to None, the CAS part will be located within any BodyType.
        :type body_type: Union[BodyType, int, None], optional
        :param outfit_category_and_index: The outfit category and index of the Sims outfit to check. Default is the Sims current outfit.
        :type outfit_category_and_index: Union[Tuple[OutfitCategory, int], None], optional
        :return: True, if the Sims outfit contain the specified CAS part. False, if the Sims outfit does not contain the specified CAS part.
        :rtype: bool
        """
        log.format_with_message('Checking if CAS part is attached to Sim.', sim=sim_info, cas_part_id=cas_part_id, body_type=body_type, outfit_category_and_index=outfit_category_and_index)
        outfit_io = CommonSimOutfitIO(sim_info, outfit_category_and_index=outfit_category_and_index)
        if body_type is None:
            return outfit_io.is_cas_part_attached(cas_part_id)
        if body_type == BodyType.NONE:
            body_type = CommonCASUtils.get_body_type_of_cas_part(cas_part_id)
        return outfit_io.get_cas_part_at_body_type(body_type) == cas_part_id

    @staticmethod
    def has_any_cas_part_attached_to_body_type(sim_info: SimInfo, body_type: Union[BodyType, int], outfit_category_and_index: Tuple[OutfitCategory, int]=None) -> bool:
        """has_any_cas_part_attached_to_body_type(sim_info, body_type, outfit_category_and_index=None)

        Determine if a Sim has a CAS Part attached to a BodyType.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param body_type: A BodyType to check.
        :type body_type: Union[BodyType, int]
        :param outfit_category_and_index: An outfit category and index of the outfit. Default is None, which is whatever outfit a Sim is currently wearing.
        :type outfit_category_and_index: Tuple[OutfitCategory, int], optional
        :return: True, if the Sim has any CAS Part attached to the specified BodyType for the specified outfit. False, it not.
        :rtype: bool
        """
        return CommonCASUtils.get_cas_part_id_at_body_type(sim_info, body_type, outfit_category_and_index=outfit_category_and_index) != -1

    @staticmethod
    def get_body_type_cas_part_is_attached_to(sim_info: SimInfo, cas_part_id: int, outfit_category_and_index: Tuple[OutfitCategory, int]=None) -> Union[BodyType, int]:
        """get_body_type_cas_part_is_attached_to(sim_info, cas_part_id, outfit_category_and_index=None)

        Retrieve the BodyType that a CAS part is attached to within a Sims outfit.

        :param sim_info: The SimInfo of the Sim to check.
        :type sim_info: SimInfo
        :param cas_part_id: A decimal identifier of the CAS part to locate.
        :type cas_part_id: int
        :param outfit_category_and_index: The outfit category and index of the Sims outfit to check. If None, the current outfit of the Sim will be used.
        :type outfit_category_and_index: Tuple[OutfitCategory, int], optional
        :return: The BodyType the specified CAS part id is attached to or BodyType.NONE if the CAS part is not found or the Sim does not have body parts for their outfit.
        :rtype: Union[BodyType, int]
        """
        log.format_with_message('Retrieving BodyType for CAS part.', sim=sim_info, cas_part_id=cas_part_id, outfit_category_and_index=outfit_category_and_index)
        outfit_io = CommonSimOutfitIO(sim_info, outfit_category_and_index=outfit_category_and_index)
        return outfit_io.get_body_type_cas_part_is_attached_to(cas_part_id)

    @staticmethod
    def get_cas_part_id_at_body_type(sim_info: SimInfo, body_type: Union[BodyType, int], outfit_category_and_index: Tuple[OutfitCategory, int]=None) -> int:
        """get_cas_part_id_at_body_type(sim_info, body_type, outfit_category_and_index=None)

        Retrieve the CAS part identifier attached to the specified BodyType within a Sims outfit.

        :param sim_info: The SimInfo of the Sim to check.
        :type sim_info: SimInfo
        :param body_type: The BodyType to check.
        :type body_type: Union[BodyType, int]
        :param outfit_category_and_index: The outfit category and index of the Sims outfit to check. Default is the Sims current outfit.
        :type outfit_category_and_index: Tuple[OutfitCategory, int], optional
        :return: The CAS part identifier attached to the specified BodyType or -1 if the BodyType is not found.
        :rtype: int
        """
        log.format_with_message('Checking if CAS part is attached to Sim.', sim=sim_info, body_type=body_type, outfit_category_and_index=outfit_category_and_index)
        outfit_io = CommonSimOutfitIO(sim_info, outfit_category_and_index=outfit_category_and_index)
        return outfit_io.get_cas_part_at_body_type(body_type)


if not ON_RTD:
    @Command('s4clib.attach_cas_part', command_type=CommandType.Live)
    def _s4clib_attach_cas_part(cas_part_id: int, body_type_str: str='any', opt_sim: OptionalTargetParam=None, _connection: Any=None):
        from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        from server_commands.argument_helpers import get_optional_target
        output = CheatOutput(_connection)
        if cas_part_id < 0:
            output('ERROR: cas_part_id must be a positive number.')
            return
        if not CommonCASUtils.is_cas_part_loaded(cas_part_id):
            output('ERROR: No cas part was found with id: {}'.format(cas_part_id))
            return
        sim_info = CommonSimUtils.get_sim_info(get_optional_target(opt_sim, _connection))
        if sim_info is None:
            output('Failed, no Sim was specified or the specified Sim was not found!')
            return
        if body_type_str is None:
            output('No body_type specified.')
            return
        if body_type_str == 'any':
            body_type_str = 'none'
        if body_type_str.isnumeric():
            try:
                body_type = int(body_type_str)
            except ValueError:
                output('Specified body type is neither a number nor a body type name {}'.format(body_type_str))
                return
        else:
            body_type = CommonResourceUtils.get_enum_by_name(body_type_str.upper(), BodyType, default_value=BodyType.NONE)
            if body_type == BodyType.NONE:
                output('Specified body type is not a body type {}'.format(body_type_str))
                return

        output('Attempting to attach CAS Part \'{}\' to Sim \'{}\''.format(cas_part_id, CommonSimNameUtils.get_full_name(sim_info)))
        try:
            if CommonCASUtils.attach_cas_part_to_sim(sim_info, cas_part_id, body_type=body_type):
                output('CAS Part attached to Sim {} successfully.'.format(CommonSimNameUtils.get_full_name(sim_info)))
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Error occurred trying to attach a CAS Part to a Sim.', exception=ex)
        output('Done attaching CAS Pat to the Sim.')


    @Command('s4clib.detach_cas_part', command_type=CommandType.Live)
    def _s4clib_detach_cas_part(cas_part_id: int, body_type_str: str='all', opt_sim: OptionalTargetParam=None, _connection: Any=None):
        from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        from server_commands.argument_helpers import get_optional_target
        output = CheatOutput(_connection)
        if cas_part_id < 0:
            output('ERROR: cas_part_id must be a positive number.')
            return
        if not CommonCASUtils.is_cas_part_loaded(cas_part_id):
            output('ERROR: No cas part was found with id: {}'.format(cas_part_id))
            return
        sim_info = CommonSimUtils.get_sim_info(get_optional_target(opt_sim, _connection))
        if sim_info is None:
            output('Failed, no Sim was specified or the specified Sim was not found!')
            return
        if body_type_str is None:
            output('ERROR: No body_type was specified.')
            return
        if body_type_str == 'all':
            body_type = None
        elif body_type_str.isnumeric():
            try:
                body_type = int(body_type_str)
            except ValueError:
                output('Specified body type is neither a number nor a body type name {}'.format(body_type_str))
                return
        else:
            body_type = CommonResourceUtils.get_enum_by_name(body_type_str.upper(), BodyType, default_value=BodyType.NONE)
            if body_type == BodyType.NONE:
                output('Specified body type is not a body type {}'.format(body_type_str))
                return
        output('Attempting to detach CAS Part \'{}\' from Sim \'{}\''.format(cas_part_id, CommonSimNameUtils.get_full_name(sim_info)))
        try:
            if CommonCASUtils.detach_cas_part_from_sim(sim_info, cas_part_id, body_type=body_type):
                output('CAS Part detached from Sim {} successfully.'.format(CommonSimNameUtils.get_full_name(sim_info)))
        except Exception as ex:
            CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Error occurred trying to detach a CAS Part from a Sim.', exception=ex)
        output('Done detaching CAS Pat to the Sim.')


    @Command('s4clib.print_cas_part_at_body_type', command_type=CommandType.Live)
    def _s4clib_print_cas_part_at_body_type(body_type_str: str, opt_sim: OptionalTargetParam=None, _connection: int=None):
        from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
        from server_commands.argument_helpers import get_optional_target
        output = CheatOutput(_connection)
        output('Printing CAS Part at body type. ')
        if body_type_str is None:
            output('No body_type specified.')
            return
        if not body_type_str.isnumeric():
            body_type = CommonResourceUtils.get_enum_by_name(body_type_str.upper(), BodyType, default_value=BodyType.NONE)
            if body_type == BodyType.NONE:
                output('Specified body type is not a body type {}'.format(body_type_str))
                return
        else:
            try:
                body_type = int(body_type_str)
            except ValueError:
                output('Specified body type is neither a number nor a body type name {}'.format(body_type_str))
                return
        sim_info = CommonSimUtils.get_sim_info(get_optional_target(opt_sim, _connection))
        if sim_info is None:
            output('Failed, no Sim was specified or the specified Sim was not found!')
            return
        cas_part_id = CommonCASUtils.get_cas_part_id_at_body_type(sim_info, body_type)
        output('Found cas part id at body type {}: {}'.format(body_type, cas_part_id))
