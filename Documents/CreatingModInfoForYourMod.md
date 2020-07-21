A good way to keep information about your Mod together in one place is to create a `ModInfo` class for your mod in the root of it.

```Python
from sims4communitylib.mod_support.common_mod_info import CommonModInfo


class ModInfo(CommonModInfo):
    """Contains details related to the mod itself.

    """
    _FILE_PATH: str = str(__file__)

    @property
    def _name(self) -> str:
        return 'Sims4CommunityLib'

    @property
    def _author(self) -> str:
        return 'ColonolNutty'

    @property
    def _base_namespace(self) -> str:
        return 'sims4communitylib'

    @property
    def _file_path(self) -> str:
        return ModInfo._FILE_PATH
```

A benefit to having a ModInfo object for your Mod is that other mods will be able to gather information about your mod through this file.

You will also be able to utilize `ModInfo.get_identity()` in various places, such as when registering [[Logs|Logging Tutorial]] or creating [[Custom Interactions|Custom Interaction Tutorial]].
