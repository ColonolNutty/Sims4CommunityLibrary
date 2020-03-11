"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""


class CommonEvent:
    """ A custom event, for use with the :class:`.CommonEventHandler`. """
    @property
    def event_name(self) -> str:
        """The name of this event.

        :return: The name of the event.
        :rtype: str
        """
        return self.__class__.__name__

    def __str__(self) -> str:
        return 'CommonEvent[Name:{}]'.format(self.event_name)

    def __repr__(self) -> str:
        return 'common_event_name_{}'.format(self.event_name)
