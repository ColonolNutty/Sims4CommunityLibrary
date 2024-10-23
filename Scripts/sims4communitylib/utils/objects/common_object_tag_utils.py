"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from distributor.shared_messages import IconInfoData
from objects.game_object import GameObject
from typing import Tuple, Set, Union, Iterator, List

from objects.script_object import ScriptObject
from sims4communitylib.enums.tags_enum import CommonGameTag
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, \
    CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_log_registry import CommonLogRegistry
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils


class CommonObjectTagUtils:
    """Utilities for manipulating the tags of objects.

    """

    @classmethod
    def has_game_tag(cls, game_object: Union[GameObject, ScriptObject], tag: Union[int, CommonGameTag]) -> bool:
        """has_game_tag(game_object, tag)

        Determine if an Object has the specified tag.

        :param game_object: An instance of an Object.
        :type game_object: Union[GameObject, ScriptObject]
        :param tag: A tag to locate.
        :type tag: Union[int, CommonGameTag]
        :return: True, if the Object has the specified tag. False, if not.
        :rtype: bool
        """
        return CommonObjectTagUtils.has_game_tags(game_object, (tag,))

    @classmethod
    def has_game_tags(cls, game_object: Union[GameObject, ScriptObject], tags: Iterator[Union[int, CommonGameTag]]) -> bool:
        """has_game_tags(game_object, tags)

        Determine if an Object has any of the specified tags.

        :param game_object: An instance of an Object.
        :type game_object: Union[GameObject, ScriptObject]
        :param tags: A collection of tags to locate.
        :type tags: Iterator[Union[int, CommonGameTag]]
        :return: True, if the Object has any of the specified tags. False, if not.
        :rtype: bool
        """
        if game_object is None or not hasattr(game_object, 'has_any_tag'):
            return False
        return game_object.has_any_tag(tuple(tags))

    @classmethod
    def get_game_tags(cls, game_object: Union[GameObject, ScriptObject]) -> Set[int]:
        """get_game_tags(game_object)

        Retrieve the tags of an Object.

        :param game_object: An instance of an Object.
        :type game_object: Union[GameObject, ScriptObject]
        :return: A collection of tags the Object has.
        :rtype: Set[int]
        """
        if game_object is None or not hasattr(game_object, 'get_tags'):
            return set()
        return game_object.get_tags()

    @classmethod
    def add_game_tags(cls, game_object: Union[GameObject, ScriptObject], tags: Tuple[Union[int, CommonGameTag]], persist: bool = False) -> bool:
        """add_game_tags(game_object, tags, persist=False)

        Add tags to an Object.

        :param game_object: An instance of an Object.
        :type game_object: Union[GameObject, ScriptObject]
        :param tags: A collection of Game Tags to add.
        :type tags: Tuple[Union[int, CommonGameTag]]
        :param persist: If True, the Tags will persist to all instances of the Object. If False, the Tags will persist only to the specified Object. Default is False.
        :type persist: bool, optional
        :return: True, if the Tags were successfully added. False, if not.
        :rtype: bool
        """
        if game_object is None or not hasattr(game_object, 'append_tags'):
            return False
        game_object.append_tags(set(tags), persist=persist)
        return True

    @classmethod
    def remove_game_tags(cls, game_object: Union[GameObject, ScriptObject], tags: Tuple[Union[int, CommonGameTag]]) -> bool:
        """remove_game_tags(game_object, tags)

        Remove tags from an Object.

        :param game_object: An instance of an Object.
        :type game_object: Union[GameObject, ScriptObject]
        :param tags: A collection of Game Tags to remove.
        :type tags: Tuple[Union[int, CommonGameTag]]
        :return: True, if the Tags were successfully removed. False, if not.
        :rtype: bool
        """
        if game_object is None or not hasattr(game_object, 'remove_dynamic_tags'):
            return False
        game_object.remove_dynamic_tags(set(tags))
        return True

    @classmethod
    def _print_game_tags(cls, game_object: Union[GameObject, ScriptObject]) -> None:
        obj_tags_list: List[str] = list()
        for obj_tag in CommonObjectTagUtils.get_game_tags(game_object):
            if not isinstance(obj_tag, CommonGameTag):
                # noinspection PyTypeChecker
                obj_tag = CommonResourceUtils.get_enum_by_int_value(obj_tag, CommonGameTag, default_value=obj_tag)

            if hasattr(obj_tag, 'name'):
                obj_tag_name = obj_tag.name
            else:
                obj_tag_name = 'Unknown'

            obj_tags_list.append(f'{obj_tag_name} ({int(obj_tag)})')

        obj_tags_list = sorted(obj_tags_list, key=lambda x: x)
        obj_tag_list_names = ',\n'.join(obj_tags_list)
        text = ''
        text += f'Game Tags:\n{obj_tag_list_names}\n\n'
        from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
        game_object_id = CommonObjectUtils.get_object_id(game_object)
        log.debug(f'Object {game_object} Tags ({game_object_id})')
        log.debug(text)
        CommonBasicNotification(
            CommonLocalizationUtils.create_localized_string(f'Object {game_object} Tags ({game_object_id})'),
            CommonLocalizationUtils.create_localized_string(text)
        ).show(
            icon=IconInfoData(obj_instance=game_object)
        )


log = CommonLogRegistry().register_log(ModInfo.get_identity(), 's4cl_object_tag_utils')
log.enable()


# noinspection SpellCheckingInspection
@CommonConsoleCommand(
    ModInfo.get_identity(),
    's4clib_testing.print_game_tags',
    'Print a list of Game Tags on a Game Object.',
    command_arguments=(
        CommonConsoleCommandArgument('game_object', 'Game Object Instance Id', 'The instance id of a game object to check.'),
    ),
    command_aliases=(
        's4clib_testing.printgametags',
    )
)
def _common_print_game_tags(output: CommonConsoleCommandOutput, game_object: GameObject):
    if game_object is None:
        return

    output(f'Printing game tags of {game_object}')
    CommonObjectTagUtils._print_game_tags(game_object)
    output('------------------------------------')
