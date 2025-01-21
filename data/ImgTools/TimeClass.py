# timer.py

import time


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class Timer:
    def __init__(self):
        self._start_time = None
        self.elapsed_time = None

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            self.stop()

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            self.start()

        self.elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
