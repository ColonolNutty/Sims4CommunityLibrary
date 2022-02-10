"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union


class CommonModIdentity:
    """CommonModIdentity(name, author, base_namespace, file_path)

    The identity of a mod

    .. note:: It contains information about a mod such as Mod Name, Mod Author,\
        the script base namespace, and the file path to your mod.

    :param name: The name of a mod.
    :type name: str
    :param author: The author of a mod.
    :type author: str
    :param base_namespace: The base namespace of the `.ts4script` file of a mod.
    :type base_namespace: str
    :param file_path: The path to the ts4script file of a mod.
    :type file_path: str
    """
    def __init__(self, name: str, author: str, base_namespace: str, file_path: str, version: str):
        self._name = name.replace(' ', '_')
        self._author = author
        self._base_namespace = base_namespace
        self._script_file_path = file_path
        self._version = version

    @property
    def name(self) -> str:
        """The name of a mod.

        .. note:: The name should not contain spaces.

        :return: The name of a mod.
        :rtype: str
        """
        return str(self._name)

    @property
    def author(self) -> str:
        """The author of a mod.

        :return: The name of the author of a mod.
        :rtype: str
        """
        return str(self._author)

    @property
    def base_namespace(self) -> str:
        """The base namespace of the `.ts4script` file of a mod.

        .. note:: S4CL has the base namespace of `sims4communitylib`.

        :return: The base script namespace of a mod.
        :rtype: str
        """
        return str(self._base_namespace)

    @property
    def file_path(self) -> str:
        """The path to the ts4script file of a mod.

        .. note::

           A good override value can be `__file__`, it will retrieve the file path automatically,\
           assuming the inheriting class is at the root of the mod.

        :return: The file path to a mod.
        :rtype: str
        """
        return str(self._script_file_path)

    @property
    def version(self) -> str:
        """The version a mod is currently at.

        :return: The version of a mod. The Default value is '1.0'.
        :rtype: str
        """
        return str(self._version)

    @staticmethod
    def _get_mod_name(mod_identifier: Union[str, 'CommonModIdentity']) -> Union[str, None]:
        from sims4communitylib.utils.misc.common_mod_identity_utils import CommonModIdentityUtils
        return CommonModIdentityUtils.determine_mod_name_from_identifier(mod_identifier)

    def __eq__(self, other: 'CommonModIdentity') -> bool:
        if isinstance(other, str):
            return self.name == other
        if not isinstance(other, CommonModIdentity):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return 'mod_{}_version_{}_author_{}_namespace_{}'.format(self.name, self.version.replace('.', '_').replace('/', '_').replace('\\', '_'), self.author, self.base_namespace)

    def __str__(self) -> str:
        return 'Identity:\n Mod Name: {}\n Version: {}\n Mod Author: {}\n Base Namespace: {}\n Path To Mod: {}'.format(self.name, self.version, self.author, self.base_namespace, self.file_path)
