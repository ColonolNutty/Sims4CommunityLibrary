"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""


class CommonModIdentity:
    """Information about a mod.

    """
    def __init__(self, name: str, author: str, base_namespace: str, file_path: str):
        self._name = name.replace(' ', '_')
        self._author = author
        self._base_namespace = base_namespace
        self._script_file_path = file_path

    @property
    def name(self) -> str:
        """The name of a mod without spaces.

        """
        return str(self._name)

    @property
    def author(self) -> str:
        """The author of a mod.

        """
        return str(self._author)

    @property
    def base_namespace(self) -> str:
        """The namespace of the ts4script file of a mod.
        Example: S4CL has a base name of sims4communitylib.

        """
        return str(self._base_namespace)

    @property
    def file_path(self) -> str:
        """The path to the ts4script file of a mod.

        """
        return str(self._script_file_path)

    def __repr__(self):
        return 'mod_{}_author_{}_namespace_{}'.format(self.name, self.author, self.base_namespace)

    def __str__(self):
        return 'Identity:\n Mod Name: {}\n Mod Author: {}\n Base Namespace: {}\n Path To Mod: {}'.format(self.name, self.author, self.base_namespace, self.file_path)
