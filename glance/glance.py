import time
import attr
import variants
import uuid
import functools
import statistics
import inspect
import dateutil.relativedelta
from datetime import datetime
from glance.errors import GlanceLookOpenError


@attr.s
class Look:
    target = attr.ib(type=str)
    expected_args = attr.ib(type=inspect.Signature)
    id = attr.ib(type=str, default=None)
    start_time = attr.ib(type=float, default=None)
    end_time = attr.ib(type=float, default=None)
    given_args = attr.ib(type=dict, factory=dict)

    @property
    def is_done(self):
        if self.start_time and self.end_time:
            return True
        else:
            return False

    def __attrs_post_init__(self):
        self.start_time = time.time()
        self.id = str(uuid.uuid4())

    @variants.primary
    def look_time(self):
        if self.is_done:
            return self.end_time - self.start_time
        else:
            raise GlanceLookOpenError()

    @look_time.variant("datetime")
    def look_time(self):
        if self.is_done:
            dt_start = datetime.fromtimestamp(self.start_time)
            dt_end = datetime.fromtimestamp(self.end_time)
            time_delta = dateutil.relativedelta.relativedelta(dt_end, dt_start)
            return time_delta
        else:
            raise GlanceLookOpenError()

    @look_time.variant("humanized")
    def look_time(self):
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
            pass
        else:
            self.end_time = time.time()


@attr.s
class Watch:
    target = attr.ib(type=str)
    expected_args = attr.ib(type=inspect.Signature, default=None)
    start_time = attr.ib(type=float, default=None)
    end_time = attr.ib(type=float, default=None)
    looks = attr.ib(type=dict, factory=dict)

    def __attrs_post_init__(self):
        self.start_time = time.time()

    def start_look(self):
        look = Look(self.target, expected_args=self.expected_args)
        self.looks[look.id] = look
        return look.id

    def stop_look(self, look_id):
        look = self.looks[look_id]
        look.stop()

    def stop(self):
        for look in self.looks.values():
            look.stop()
        self.end_time = time.time()

    @variants.primary
    def longest_look(self):  # TODO refactor to use max()?
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
        shortest = None
        for key, look in self.looks.items():
            if shortest:
                if shortest[1] > look.look_time():
                    shortest = (key, look.look_time())
            else:
                shortest = (key, look.look_time())
        return shortest

    @property
    def mean(self):
        times = [look.look_time() for look in self.looks.values()]
        return statistics.mean(times)

    @property
    def std(self):
        times = [look.look_time() for look in self.looks.values()]
        return statistics.stdev(times)

    @variants.primary
    def find_outliers(self):
        outliers = list()
        for look in self.looks.values():
            if look.look_time() > 2 * self.std:
                outliers.append((look.id, look.look_time()))
        return outliers

    @find_outliers.variant("looks")
    def find_outliers(self):
        outliers = list()
        for look in self.looks.values():
            if look.look_time() > 2 * self.std:
                outliers.append(look)
        return outliers

    @variants.primary
    def find_weak_outliers(self):
        outliers = list()
        for look in self.looks.values():
            if look.look_time() > self.std:
                outliers.append((look.id, look.look_time()))
        return outliers

    @find_weak_outliers.variant("looks")
    def find_weak_outliers(self):
        outliers = list()
        for look in self.looks.values():
            if look.look_time() > self.std:
                outliers.append(look)
        return outliers


@attr.s
class Glance:
    start_time = attr.ib(type=float, default=time.time())
    end_time = attr.ib(type=float, default=None)
    watches = attr.ib(type={}, factory=dict)

    def end(self):
        for watch in self.watches.values():
            watch.stop()

        self.end_time = time.time()

    def start_watch(self, target_name: str):
        self.watches[target_name] = Watch(target=target_name)

    def stop_watch(self, target_name: str):
        watch = self.watches[target_name]
        watch.stop()

    def watch(self, func):
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
