"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Union, Any, Dict


class CommonSerializable:
    """Indicates an object can be serialized and deserialized."""
    def serialize(self) -> Union[str, Dict[str, Any]]:
        """serialize()

        Serialize the object into a JSON Serializable form.

        :return: A serializable representation of the object.
        :rtype: Union[str, Dict[str, Any]]
        """
        raise NotImplementedError()

    @classmethod
    def deserialize(cls, data: Union[str, Dict[str, Any]]) -> Union['CommonSerializable', None]:
        """deserialize(data)

        Deserialize the object from a JSON Serializable form.

        :return: The deserialized form of the object or None if it fails to deserialize.
        :rtype: Union[CommonSerializable, None]
        """
        raise NotImplementedError()
