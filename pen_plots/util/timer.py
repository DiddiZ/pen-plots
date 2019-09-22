import time
from collections import OrderedDict


class Timer():
    """
    Simple context timer. Starts counting the time when entering the context and stops as soon as the conext is left.
    """

    def __init__(self):
        self.elapsed = 0

    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.elapsed += self.end - self.start


class MultiTimer():
    """
    Collection for multiple comtext timers.
    """

    def __init__(self):
        self.timers = OrderedDict()

    def measure(self, key, reset=False):
        """
        Creates a new `Timer` and stores it under `key`. If a timer to the same key already exists, this one is
        returned instead.
        """
        timer = self.timers.get(key, None) if not reset else None
        if timer is None:
            timer = Timer()
            self.timers[key] = timer
        return timer

    def all_timings(self):
        return [(key, timer.elapsed) for key, timer in self.timers.items()]

    def __getitem__(self, key):
        timer = self.timers.get(key, None)
        return timer.elapsed if timer is not None else None
