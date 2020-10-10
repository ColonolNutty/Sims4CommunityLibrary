"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from time import perf_counter


class CommonStopWatch:
    """CommonStopWatch()

    A class used to see how long things take.

    """
    def __init__(self) -> None:
        self._start_time = None
        self._started: bool = False

    def start(self) -> None:
        """start()

        Start the stop watch.
        """
        if self._started:
            return
        self._start_time = perf_counter()
        self._started = True

    def interval(self) -> float:
        """interval()

        Retrieve a time stamp for how long the watch has been running for without ending it.

        :return: The number of seconds that occurred since the stop watch was started.
        :rtype: float
        """
        if not self._started or self._start_time is None:
            return -1.0
        interval_time = perf_counter()
        fractional_seconds = (interval_time - self._start_time)
        return fractional_seconds

    def stop(self) -> float:
        """stop()

        Stop the stop watch.

        ..warning:: This will also reset the start time of the stop watch. It will also stop the stop watch.

        :return: The number of seconds that occurred since starting the stop watch.
        :rtype: float
        """
        stopped_time = self.interval()
        self._start_time = None
        self._started = False
        return stopped_time
