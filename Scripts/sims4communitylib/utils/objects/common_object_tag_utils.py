"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from distributor.shared_messages import IconInfoData
from objects.game_object import GameObject
from typing import Tuple, Set, Union, Iterator, List

from sims4.commands import Command, CommandType, CheatOutput
from sims4communitylib.enums.tags_enum import CommonGameTag
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.common_resource_utils import CommonResourceUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils


class CommonObjectTagUtils:
    """Utilities for manipulating the tags of objects.

    """

    @staticmethod
    def has_game_tags(game_object: GameObject, tags: Iterator[Union[int, CommonGameTag]]) -> bool:
        """has_game_tags(game_object, tags)

        Determine if an Object has any of the specified tags.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param tags: A collection of tags to locate.
        :type tags: Iterator[Union[int, CommonGameTag]]
        :return: True, if the Object has any of the specified tags. False, if not.
        :rtype: bool
        """
        if game_object is None:
            return False
        return game_object.has_any_tag(tuple(tags))

    @staticmethod
    def get_game_tags(game_object: GameObject) -> Set[int]:
        """get_game_tags(game_object)

        Retrieve the tags of an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :return: A collection of tags the Object has.
        :rtype: Set[int]
        """
        if game_object is None:
            return set()
        return game_object.get_tags()

    @staticmethod
    def add_game_tags(game_object: GameObject, tags: Tuple[int], persist: bool=False) -> bool:
        """add_game_tags(game_object, tags, persist=False)

        Add tags to an Object.

        :param game_object: An instance of an Object.
        :type game_object: GameObject
        :param tags: A collection of Game Tags to add.
        :type tags: Tuple[int]
        :param persist: If True, the Tags will persist to all instances of the Object. If False, the Tags will persist only to the specified Object. Default is False.
        :type persist: bool, optional
        :return: True, if the Tags were successfully added. False, if not.
        :rtype: bool
        """
        if game_object is None:
            return False
        game_object.append_tags(set(tags), persist=persist)
        return True


@Command('s4clib.show_game_tags', command_type=CommandType.Live)
def _common_show_game_tags(target_object_id: int=None, _connection: int=None):
    output = CheatOutput(_connection)
    from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
    game_object = CommonObjectUtils.get_game_object(target_object_id)
    if game_object is None:
        output('Failed, no Object Id was specified or the specified Object was not found!')
        return
    output('Showing game tags of {}'.format(game_object))
    try:
        obj_tags_list: List[str] = list()
        for obj_tag in CommonObjectTagUtils.get_game_tags(game_object):
            if obj_tag in CommonGameTag.value_to_name:
                new_obj_tag = CommonResourceUtils.get_enum_by_name(CommonGameTag.value_to_name[obj_tag], CommonGameTag, default_value=None)
                if new_obj_tag is None:
                    obj_tags_list.append(str(obj_tag))
                    continue
                obj_tags_list.append('{} ({})'.format(new_obj_tag.name, str(obj_tag)))
            else:
                obj_tags_list.append(str(obj_tag))
        obj_tags_list = sorted(obj_tags_list, key=lambda x: x)
        obj_tag_list_names = ', '.join(obj_tags_list)
        text = ''
        text += 'Object Tags:\n{}\n\n'.format(obj_tag_list_names)
        CommonBasicNotification(
            CommonLocalizationUtils.create_localized_string('{} Tags ({})'.format(game_object, CommonObjectUtils.get_object_id(game_object))),
            CommonLocalizationUtils.create_localized_string(text)
        ).show(
            icon=IconInfoData(obj_instance=game_object)
        )
    except Exception as ex:
        CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'Failed to show game tags of Object {}.'.format(game_object), exception=ex)
        output('Failed to show game tags of Object {}. {}'.format(game_object, str(ex)))
