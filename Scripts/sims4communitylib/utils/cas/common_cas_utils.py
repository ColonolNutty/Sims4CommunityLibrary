"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os
from typing import Tuple, Union, Any

from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.services.sim.cas.common_sim_outfit_io import CommonSimOutfitIO
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils

# ReadTheDocs
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'

if not ON_RTD:
    from server_commands.argument_helpers import OptionalTargetParam
    from sims.outfits.outfit_enums import OutfitCategory, BodyType
    from sims.sim_info import SimInfo
    from sims4.commands import Command, CheatOutput, CommandType
else:
    # noinspection PyMissingOrEmptyDocstring
    class OptionalTargetParam:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class OutfitCategory:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class BodyType:
        NONE = 0

    # noinspection PyMissingOrEmptyDocstring
    class SimInfo:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class Command:
        pass

    # noinspection PyMissingOrEmptyDocstring
    class CheatOutput:
        pass

    # noinspection PyMissingOrEmptyDocstring
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
        return body_type is not None and body_type > 0

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
        if isinstance(body_type, int) and body_type in BodyType.value_to_name:
            new_body_type = CommonResourceUtils.get_enum_by_name(BodyType.value_to_name[body_type], BodyType, default_value=None)
            if new_body_type is not None:
                body_type = new_body_type
        return body_type

    @staticmethod
    def get_body_type_by_name(name: str, default_body_type: Union[BodyType, None]=BodyType.NONE) -> BodyType:
        """get_body_type_by_name(name, default_value=BodyType.NONE)

        Retrieve an BodyType by name.

        :param name: The name of a body type.
        :type name: str
        :param default_body_type: The default body type to use if a body type is not found using the specified name. Default is BodyType.NONE
        :type default_body_type: Union[BodyType, None], optional
        :return: The BodyType with the specified name or the default body type if no body type was found using the specified name.
        :rtype: BodyType
        """
        upper_case_name = str(name).upper().strip()
        return CommonResourceUtils.get_enum_by_name(upper_case_name, BodyType, default_value=default_body_type)

    @staticmethod
    def convert_value_to_body_type(value: Union[BodyType, int]) -> Union[BodyType, int]:
        """convert_value_to_body_type(value)

        Retrieve an BodyType by value.

        :param value: The value of a body type.
        :type value: Union[BodyType, int]
        :return: The BodyType with the specified value or the specified value if no BodyType was found.
        :rtype: Union[BodyType, int]
        """
        if isinstance(value, BodyType):
            return value
        if value in BodyType.value_to_name:
            return CommonResourceUtils.get_enum_by_name(BodyType.value_to_name[value], BodyType, default_value=value)
        return value

    @staticmethod
    def attach_cas_part_to_sim(sim_info: SimInfo, cas_part_id: int, body_type: Union[BodyType, int]=BodyType.NONE, outfit_category_and_index: Union[Tuple[OutfitCategory, int], None]=None, mod_identity: CommonModIdentity=None, **__) -> bool:
        """attach_cas_part_to_sim(sim_info, cas_part_id, body_type=BodyType.NONE, outfit_category_and_index=None, mod_identity=None, **__)

        Add a CAS part at the specified BodyType to the Sims outfit.

        :param sim_info: The SimInfo of a Sim to add the CAS part to.
        :type sim_info: SimInfo
        :param cas_part_id: The decimal identifier of a CAS part to attach to the Sim.
        :type cas_part_id: int
        :param body_type: The BodyType the CAS part will be attached to. If no value is provided or it is None, the BodyType of the CAS part itself will be used.
        :type body_type: Union[BodyType, int], optional
        :param outfit_category_and_index: The outfit category and index of the Sims outfit to modify. If no value is provided, the Sims current outfit will be used.
        :type outfit_category_and_index: Union[Tuple[OutfitCategory, int], None], optional
        :param mod_identity: The identity of the mod making changes. Default is None. Optional, but highly recommended!
        :type mod_identity: CommonModIdentity, optional
        :return: True if the CAS part was successfully attached to the Sim. False if the CAS part was not successfully attached to the Sim.
        :rtype: bool
        """
        from sims4communitylib.services.sim.cas.common_sim_outfit_io import CommonSimOutfitIO
        if cas_part_id == -1 or cas_part_id is None:
            raise RuntimeError('No cas_part_id was provided.')
        log.format_with_message('Attempting to attach CAS part to Sim', sim=sim_info, cas_part_id=cas_part_id, body_type=body_type, outfit_category_and_index=outfit_category_and_index)
        outfit_io = CommonSimOutfitIO(sim_info, outfit_category_and_index=outfit_category_and_index, mod_identity=mod_identity)
        outfit_io.attach_cas_part(cas_part_id, body_type=body_type)
        return outfit_io.apply(**__)

    @staticmethod
    def detach_cas_part_from_sim(sim_info: SimInfo, cas_part_id: int, body_type: Union[BodyType, int, None]=None, outfit_category_and_index: Union[Tuple[OutfitCategory, int], None]=None, mod_identity: CommonModIdentity=None, **__) -> bool:
        """detach_cas_part_from_sim(sim_info, cas_part_id, body_type=None, outfit_category_and_index=None, mod_identity=None, **__)

        Remove a CAS part at the specified BodyType from the Sims outfit.

        :param sim_info: The SimInfo of a Sim to remove the CAS part from.
        :type sim_info: SimInfo
        :param cas_part_id: The decimal identifier of a CAS part to detach from the Sim.
        :type cas_part_id: int
        :param body_type: The BodyType the CAS part will be detached from. If BodyType.NONE is provided, the BodyType of the CAS Part itself will be used. If set to None, the CAS part will be removed from all BodyTypes. Default is None.
        :type body_type: Union[BodyType, int, None], optional
        :param outfit_category_and_index: The outfit category and index of the Sims outfit to modify. If no value is provided, the Sims current outfit will be used.
        :type outfit_category_and_index: Union[Tuple[OutfitCategory, int], None], optional
        :param mod_identity: The identity of the mod making changes. Default is None. Optional, but highly recommended!
        :type mod_identity: CommonModIdentity, optional
        :return: True if the CAS part was successfully detached from the Sim. False if the CAS part was not successfully detached from the Sim.
        :rtype: bool
        """
        from sims4communitylib.services.sim.cas.common_sim_outfit_io import CommonSimOutfitIO
        if cas_part_id == -1 or cas_part_id is None:
            raise RuntimeError('No cas_part_id was provided.')
        log.format_with_message('Attempting to remove CAS part from Sim', sim=sim_info, cas_part_id=cas_part_id, body_type=body_type, outfit_category_and_index=outfit_category_and_index)
        outfit_io = CommonSimOutfitIO(sim_info, outfit_category_and_index=outfit_category_and_index, mod_identity=mod_identity)
        if body_type is None:
            outfit_io.detach_cas_part(cas_part_id)
        elif body_type == BodyType.NONE:
            body_type = CommonCASUtils.get_body_type_of_cas_part(cas_part_id)
            if outfit_io.get_cas_part_at_body_type(body_type) != cas_part_id:
                return False
            outfit_io.detach_body_type(body_type)
        return outfit_io.apply(**__)

    @staticmethod
    def has_cas_part_attached(sim_info: SimInfo, cas_part_id: int, body_type: Union[BodyType, int, None]=None, outfit_category_and_index: Tuple[OutfitCategory, int]=None, mod_identity: CommonModIdentity=None) -> bool:
        """has_cas_part_attached(sim_info, cas_part_id, body_type=None, outfit_category_and_index=None, mod_identity=None)

        Determine if a Sim has the specified CAS part attached to their outfit.

        :param sim_info: The SimInfo of the Sim to check.
        :type sim_info: SimInfo
        :param cas_part_id: A decimal identifier of the CAS part to locate.
        :type cas_part_id: int
        :param body_type: The BodyType the CAS part will be located at. If BodyType.NONE is provided, the body type of the CAS Part itself will be used. If set to None, the CAS part will be located within any BodyType. Default is None.
        :type body_type: Union[BodyType, int, None], optional
        :param outfit_category_and_index: The outfit category and index of the Sims outfit to check. Default is the Sims current outfit.
        :type outfit_category_and_index: Union[Tuple[OutfitCategory, int], None], optional
        :param mod_identity: The identity of the mod performing the function. Default is None. Optional, but highly recommended!
        :type mod_identity: CommonModIdentity, optional
        :return: True, if the Sims outfit contain the specified CAS part. False, if the Sims outfit does not contain the specified CAS part.
        :rtype: bool
        """
        log.format_with_message('Checking if CAS part is attached to Sim.', sim=sim_info, cas_part_id=cas_part_id, body_type=body_type, outfit_category_and_index=outfit_category_and_index)
        outfit_io = CommonSimOutfitIO(sim_info, outfit_category_and_index=outfit_category_and_index, mod_identity=mod_identity)
        if body_type is None:
            return outfit_io.is_cas_part_attached(cas_part_id)
        if body_type == BodyType.NONE:
            body_type = CommonCASUtils.get_body_type_of_cas_part(cas_part_id)
        return outfit_io.get_cas_part_at_body_type(body_type) == cas_part_id

    @staticmethod
    def has_any_cas_part_attached_to_body_type(sim_info: SimInfo, body_type: Union[BodyType, int], outfit_category_and_index: Tuple[OutfitCategory, int]=None, mod_identity: CommonModIdentity=None) -> bool:
        """has_any_cas_part_attached_to_body_type(sim_info, body_type, outfit_category_and_index=None, mod_identity=None)

        Determine if a Sim has a CAS Part attached to a BodyType.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param body_type: A BodyType to check.
        :type body_type: Union[BodyType, int]
        :param outfit_category_and_index: An outfit category and index of the outfit. Default is None, which is whatever outfit a Sim is currently wearing.
        :type outfit_category_and_index: Tuple[OutfitCategory, int], optional
        :param mod_identity: The identity of the mod performing the function. Default is None. Optional, but highly recommended!
        :type mod_identity: CommonModIdentity, optional
        :return: True, if the Sim has any CAS Part attached to the specified BodyType for the specified outfit. False, it not.
        :rtype: bool
        """
        return CommonCASUtils.get_cas_part_id_at_body_type(sim_info, body_type, outfit_category_and_index=outfit_category_and_index, mod_identity=mod_identity) != -1

    @staticmethod
    def get_body_type_cas_part_is_attached_to(sim_info: SimInfo, cas_part_id: int, outfit_category_and_index: Tuple[OutfitCategory, int]=None, mod_identity: CommonModIdentity=None) -> Union[BodyType, int]:
        """get_body_type_cas_part_is_attached_to(sim_info, cas_part_id, outfit_category_and_index=None, mod_identity=None)

        Retrieve the BodyType that a CAS part is attached to within a Sims outfit.

        :param sim_info: The SimInfo of the Sim to check.
        :type sim_info: SimInfo
        :param cas_part_id: A decimal identifier of the CAS part to locate.
        :type cas_part_id: int
        :param outfit_category_and_index: The outfit category and index of the Sims outfit to check. If None, the current outfit of the Sim will be used.
        :type outfit_category_and_index: Tuple[OutfitCategory, int], optional
        :param mod_identity: The identity of the mod performing the function. Default is None. Optional, but highly recommended!
        :type mod_identity: CommonModIdentity, optional
        :return: The BodyType the specified CAS part id is attached to or BodyType.NONE if the CAS part is not found or the Sim does not have body parts for their outfit.
        :rtype: Union[BodyType, int]
        """
        log.format_with_message('Retrieving BodyType for CAS part.', sim=sim_info, cas_part_id=cas_part_id, outfit_category_and_index=outfit_category_and_index)
        outfit_io = CommonSimOutfitIO(sim_info, outfit_category_and_index=outfit_category_and_index, mod_identity=mod_identity)
        return outfit_io.get_body_type_cas_part_is_attached_to(cas_part_id)

    @staticmethod
    def get_cas_part_id_at_body_type(sim_info: SimInfo, body_type: Union[BodyType, int], outfit_category_and_index: Tuple[OutfitCategory, int]=None, mod_identity: CommonModIdentity=None) -> int:
        """get_cas_part_id_at_body_type(sim_info, body_type, outfit_category_and_index=None, mod_identity=None)

        Retrieve the CAS part identifier attached to the specified BodyType within a Sims outfit.

        :param sim_info: The SimInfo of the Sim to check.
        :type sim_info: SimInfo
        :param body_type: The BodyType to check.
        :type body_type: Union[BodyType, int]
        :param outfit_category_and_index: The outfit category and index of the Sims outfit to check. Default is the Sims current outfit.
        :type outfit_category_and_index: Tuple[OutfitCategory, int], optional
        :param mod_identity: The identity of the mod performing the function. Default is None. Optional, but highly recommended!
        :type mod_identity: CommonModIdentity, optional
        :return: The CAS part identifier attached to the specified BodyType or -1 if the BodyType is not found.
        :rtype: int
        """
        log.format_with_message('Checking if CAS part is attached to Sim.', sim=sim_info, body_type=body_type, outfit_category_and_index=outfit_category_and_index)
        outfit_io = CommonSimOutfitIO(sim_info, outfit_category_and_index=outfit_category_and_index, mod_identity=mod_identity)
        return outfit_io.get_cas_part_at_body_type(body_type)

    @staticmethod
    def get_skin_tone(sim_info: SimInfo) -> int:
        """get_skin_tone(sim_info)

        Retrieve the id for the Skin Tone of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The decimal identifier of the skin tone of the specified Sim.
        :rtype: int
        """
        return sim_info.skin_tone

    @staticmethod
    def set_skin_tone(sim_info: SimInfo, skin_tone: int):
        """set_skin_tone(sim_info, skin_tone)

        Set the skin tone of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param skin_tone: The decimal identifier of the skin tone to set the Sim to.
        :type skin_tone: int
        """
        sim_info.skin_tone = skin_tone


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
            body_type = BodyType.NONE
        elif body_type_str.isnumeric():
            try:
                body_type = int(body_type_str)
            except ValueError:
                output('Specified body type is neither a number nor a body type name {}'.format(body_type_str))
                return
        else:
            body_type = CommonResourceUtils.get_enum_by_name(body_type_str.upper(), BodyType, default_value=BodyType.NONE)
            if body_type == BodyType.NONE:
                output('Specified body type is not a body type, it was "{}"'.format(body_type_str))
                return

        output('Attempting to attach CAS Part \'{}\' to Sim \'{}\''.format(cas_part_id, CommonSimNameUtils.get_full_name(sim_info)))
        try:
            if CommonCASUtils.attach_cas_part_to_sim(sim_info, cas_part_id, body_type=body_type):
                output('CAS Part attached to Sim {} successfully.'.format(CommonSimNameUtils.get_full_name(sim_info)))
        except Exception as ex:
            output('An error occurred while trying to attach the CAS Part!')
            CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Error occurred trying to attach a CAS Part to a Sim.', exception=ex)
        output('Done attaching CAS Part to the Sim.')


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


    @Command('s4clib.is_cas_part_available', command_type=CommandType.Live)
    def _s4clib_is_cas_part_available(part_id: int=None, _connection: int=None):
        output = CheatOutput(_connection)
        if part_id is None:
            output('No CAS Part specified!')
            return
        output('Checking if CAS Part {} is available.'.format(part_id))
        if CommonCASUtils.is_cas_part_loaded(part_id):
            output('CAS Part is available.')
        else:
            output('CAS Part is not available.')


    @Command('s4clib.print_skin_tone', command_type=CommandType.Live)
    def _common_print_skin_tone(opt_sim: OptionalTargetParam=None, _connection: int=None):
        from server_commands.argument_helpers import get_optional_target
        output = CheatOutput(_connection)
        output('Attempting to get skin tone.')
        sim_info = CommonSimUtils.get_sim_info(get_optional_target(opt_sim, _connection))
        if sim_info is None:
            output('Failed, no Sim was specified or the specified Sim was not found!')
            return
        output('Sim: {}'.format(CommonSimNameUtils.get_full_name(sim_info)))
        output('Skin Tone: {}'.format(CommonCASUtils.get_skin_tone(sim_info)))


    @Command('s4clib.set_skin_tone', command_type=CommandType.Live)
    def _common_set_skin_tone(skin_tone_id: int, opt_sim: OptionalTargetParam=None, _connection: int=None):
        from server_commands.argument_helpers import get_optional_target
        output = CheatOutput(_connection)
        sim_info = CommonSimUtils.get_sim_info(get_optional_target(opt_sim, _connection))
        if sim_info is None:
            output('Failed, no Sim was specified or the specified Sim was not found!')
            return
        output('Attempting to set the skin tone \'{}\' of Sim \'{}\''.format(skin_tone_id, CommonSimNameUtils.get_full_name(sim_info)))
        CommonCASUtils.set_skin_tone(sim_info, skin_tone_id)
        output('Done setting the skin overlay of the Sim.')
