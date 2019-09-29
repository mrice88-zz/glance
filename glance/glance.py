import time
import attr
import variants
import uuid
import functools
import statistics
import inspect
import dateutil.relativedelta
from datetime import datetime
from glance.errors import (
    GlanceLookOpenError,
    GlanceLookClosedError,
    GlanceLookNotFoundError,
    GlanceWatchClosedError,
    GlanceWatchNotFoundError,
    GlanceWatchOpenError,
    GlanceClosedError,
    GlanceWatchExistsError
)


@attr.s
class Look:
    """
    Look class is the base unit of the glance package. It is the actual timer of whatever is being watched.
    """
    target = attr.ib(type=str)  #: What is being timed.
    expected_args = attr.ib(type=inspect.Signature, default=None)  #: Expected arguments if any.
    given_args = attr.ib(type=dict, factory=dict)  #: Arguments in this looks instance of watch item, if any.
    id = attr.ib(type=str, default=None)
    start_time = attr.ib(type=float, default=None)
    end_time = attr.ib(type=float, default=None)

    @property
    def is_done(self):
        """
        property which indicates look has ended.
        :return: boolean
        """
        if self.start_time and self.end_time:
            return True
        else:
            return False

    def __attrs_post_init__(self):
        self.start_time = time.time()
        self.id = str(uuid.uuid4())

    @variants.primary
    def look_time(self):
        """
        Returns length of look in seconds since epoch.
        :return: float
        """
        if self.is_done:
            return self.end_time - self.start_time
        else:
            raise GlanceLookOpenError()

    @look_time.variant("datetime")
    def look_time(self):
        """
        Returns length of look in relative time delta.
        :return: dateutil.relativedelta
        """
        if self.is_done:
            dt_start = datetime.fromtimestamp(self.start_time)
            dt_end = datetime.fromtimestamp(self.end_time)
            time_delta = dateutil.relativedelta.relativedelta(dt_end, dt_start)
            return time_delta
        else:
            raise GlanceLookOpenError()

    @look_time.variant("humanized")
    def look_time(self):
        """
        Returns length of look in human readable string.
        :return: str
        """
        if self.is_done:
            dt_start = datetime.fromtimestamp(self.start_time)
            dt_end = datetime.fromtimestamp(self.end_time)
            time_delta = dateutil.relativedelta.relativedelta(dt_end, dt_start)

            def human_readable(delta):
                attrs = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']
                readable_str = [
                    '%d %s' % (getattr(delta, attr), getattr(delta, attr) > 1 and attr or attr[:-1])
                    for attr in attrs if getattr(delta, attr)
                ]

                return readable_str
            return ", ".join(human_readable(time_delta))
        else:
            raise ValueError("Look has not been ended, no value for end_time")

    def stop(self):
        if self.end_time:
            raise GlanceLookClosedError(self)
        else:
            self.end_time = time.time()


@attr.s
class Watch:
    """
    Class which represents an object to be watched.
    """
    target = attr.ib(type=str)  #: Name of what is being timed.
    expected_args = attr.ib(type=inspect.Signature, default=None)
    start_time = attr.ib(type=float, default=None)
    end_time = attr.ib(type=float, default=None)
    looks = attr.ib(type=dict, factory=dict)  #: Dictionary of looks, for each instance of what is being watched.

    @property
    def is_done(self):
        """
        property which indicates Watch has ended.
        :return: boolean
        """
        if self.start_time and self.end_time:
            return True
        else:
            return False

    def __attrs_post_init__(self):
        self.start_time = time.time()

    def start_look(self):
        """
        Starts a new Look instance and adds it to Watch.looks dictionary.
        :return: str of Look.id
        """
        look = Look(self.target, expected_args=self.expected_args)
        self.looks[look.id] = look
        return look.id

    def stop_look(self, look_id):
        """
        Stops a given look in this instance of Watch.looks
        :param look_id:
        :return:
        """
        if look_id in self.looks.keys():
            look = self.looks[look_id]
            look.stop()
        else:
            raise GlanceLookNotFoundError()

    def stop(self):
        """
        Stops the given Watch and all open looks within it. Raises error if watch is closed.
        :return:
        """
        if self.end_time is None:
            for look in self.looks.values():
                if not look.is_done:
                    look.stop()
            self.end_time = time.time()
        else:
            raise GlanceWatchClosedError()

    @variants.primary
    def longest_look(self):  # TODO refactor to use max()?
        """
        Returns the longest look time in the given watch instance.
        :return:
        """
        longest = None
        for look in self.looks.values():
            if longest:
                if longest < look.look_time():
                    longest = look.look_time()
            else:
                longest = look.look_time()
        return longest

    @longest_look.variant("key")
    def longest_look(self):  # TODO refactor to use max()?
        """
        Returns the key of the longest look in the watch.
        :return: str Look.id
        """
        longest = None
        for key, look in self.looks.items():
            if longest:
                if longest[1] < look.look_time():
                    longest = (key, look.look_time())
            else:
                longest = (key, look.look_time())
        return longest[0]

    @longest_look.variant("tuple")
    def longest_look(self):  # TODO refactor to use max()?
        """
        Returns both the key, and the look_time of the longest look in the watch as a tuple.
        :return: (key, look_time)
        """
        longest = None
        for key, look in self.looks.items():
            if longest:
                if longest[1] < look.look_time():
                    longest = (key, look.look_time())
            else:
                longest = (key, look.look_time())
        return longest

    @variants.primary
    def shortest_look(self):  # TODO refactor to use min()?
        """
        Returns shortest look time in the watch.
        :return:
        """
        shortest = None
        for look in self.looks.values():
            if shortest:
                if shortest > look.look_time():
                    shortest = look.look_time()
            else:
                shortest = look.look_time()
        return shortest

    @shortest_look.variant("key")
    def shortest_look(self):  # TODO refactor to use min()?
        """
        Returns shortest look time's key in the watch.
        :return:
        """
        shortest = None
        for key, look in self.looks.items():
            if shortest:
                if shortest[1] > look.look_time():
                    shortest = (key, look.look_time())
            else:
                shortest = (key, look.look_time())
        return shortest[0]

    @shortest_look.variant("tuple")
    def shortest_look(self):  # TODO refactor to use min()?
        """
        Returns both the key, and the look_time of the shortest look in the watch as a tuple.
        :return: (key, look_time)
        """
        shortest = None
        for key, look in self.looks.items():
            if shortest:
                if shortest[1] > look.look_time():
                    shortest = (key, look.look_time())
            else:
                shortest = (key, look.look_time())
        return shortest

    @property
    def mean(self):  # TODO might need to convert to method and handle open looks.
        """
        Returns mean of the Looks in the watch.
        :return: float
        """
        times = [look.look_time() for look in self.looks.values()]
        return statistics.mean(times)

    @property
    def std(self):  # TODO might need to convert to method and handle open looks.
        """
        Returns the standard deviation of the watch's Looks
        :return: float
        """
        times = [look.look_time() for look in self.looks.values()]
        return statistics.stdev(times)

    @variants.primary
    def find_outliers(self):  # TODO might need to convert to method and handle open looks.
        """
        Finds outliers in the given watch's Looks as a list of tuples [(id, time)]
        Outlier = 2 * standard deviation
        :return: list(tuple)
        """
        outliers = list()
        for look in self.looks.values():
            if look.look_time() > 2 * self.std:
                outliers.append((look.id, look.look_time()))
        return outliers

    @find_outliers.variant("looks")
    def find_outliers(self):  # TODO might need to convert to method and handle open looks.
        """
        Finds outliers in the given watch's Looks as a list of looks [Look]
        Outlier = 2 * standard deviation
        :return: list()
        """
        outliers = list()
        for look in self.looks.values():
            if look.look_time() > 2 * self.std:
                outliers.append(look)
        return outliers

    @variants.primary
    def find_weak_outliers(self):  # TODO might need to convert to method and handle open looks.
        """
        Finds "weak" outliers in the given watch's Looks as a list of tuples [(id, time)]
        Weak_Outlier > standard deviation
        :return: list(tuple)
        """
        outliers = list()
        for look in self.looks.values():
            if look.look_time() > self.std:
                outliers.append((look.id, look.look_time()))
        return outliers

    @find_weak_outliers.variant("looks")
    def find_weak_outliers(self):  # TODO might need to convert to method and handle open looks.
        """
        Finds "weak" outliers in the given watch's Looks as a list of looks [Look]
        Weak_Outlier > standard deviation
        :return: list()
        """
        outliers = list()
        for look in self.looks.values():
            if look.look_time() > self.std:
                outliers.append(look)
        return outliers


@attr.s
class Glance:
    """
    Class that contains everything being watched, and all of their looks.
    """
    start_time = attr.ib(type=float, default=time.time())
    end_time = attr.ib(type=float, default=None)
    watches = attr.ib(type={}, factory=dict)  #: Dictionary of watches in this glance.

    def end(self):
        """
        End current Glance instance.
        :return:
        """
        if self.end_time:
            raise GlanceClosedError()
        else:
            for watch in self.watches.values():
                if not watch.is_done:
                    watch.stop()
            self.end_time = time.time()

    def start_watch(self, target_name: str):
        """
        Starts a new watch with a given target.
        :param target_name:
        :return:
        """
        if target_name in self.watches.keys():
            raise GlanceWatchExistsError()
        self.watches[target_name] = Watch(target=target_name)

    def stop_watch(self, target_name: str):
        """
        Stops a given watch.
        :param target_name:
        :return:
        """
        if target_name in self.watches.keys():
            watch = self.watches[target_name]
            if watch.is_done:
                raise GlanceWatchOpenError(watch)
            else:
                watch.stop()
        else:
            raise GlanceWatchNotFoundError(target_name)

    def watch(self, func):
        """
        Decorator to place a watch on a given function. Starts a new watch on that object in glance. and creates a new
        look at every call.
        :param func:
        :return:
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if func.__name__ not in self.watches.keys():
                self.watches[func.__name__] = Watch(target=func.__name__)
                self.watches[func.__name__].expected_args = inspect.signature(func)

            look = self.watches[func.__name__].start_look()

            func_output = func(*args, **kwargs)
            watch = self.watches[func.__name__]
            watch.stop_look(look)
            current_look = watch.looks[look]
            current_look.given_args = {
                "args": args,
                "kwargs": kwargs,
            }

            return func_output
        return wrapper
