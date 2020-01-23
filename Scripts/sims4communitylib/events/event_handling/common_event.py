"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""


class CommonEvent:
    """ A custom event, for use with the Event Handler. """
    @property
    def event_name(self) -> str:
        """The name of this event.

        """
        return self.__class__.__name__

    def __str__(self):
        return 'CommonEvent[Name:{}]'.format(self.event_name)

    def __repr__(self):
        return super().__repr__()
