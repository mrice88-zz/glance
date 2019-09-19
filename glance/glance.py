import time
import attr
import variants
import uuid
import functools
import dateutil.relativedelta
from datetime import datetime


@attr.s
class Look:
    target = attr.ib(type=str)
    id = attr.ib(type=str, default=None)
    start_time = attr.ib(type=float, default=None)
    end_time = attr.ib(type=float, default=None)

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
            raise ValueError("Look has not been ended, no value for end_time")

    @look_time.variant("datetime")
    def look_time(self):
        if self.is_done:
            dt_start = datetime.fromtimestamp(self.start_time)
            dt_end = datetime.fromtimestamp(self.end_time)
            time_delta = dateutil.relativedelta.relativedelta(dt_end, dt_start)
            return time_delta
        else:
            raise ValueError("Look has not been ended, no value for end_time")

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
        self.end_time = time.time()


@attr.s
class Watch:
    target = attr.ib(type=str)
    start_time = attr.ib(type=float)
    end_time = attr.ib(type=float, default=None)
    looks = attr.ib(type=dict, factory=dict)

    def __attrs_post_init__(self):
        self.start_time = time.time()

    def start_look(self):
        look = Look(self.target)
        self.looks[look.id] = look
        return look.id

    def stop_look(self, look_id):
        look = self.looks[look_id]
        look.stop()

    def stop(self):
        self.end_time = time.time()


@attr.s
class Glance:
    start_time = attr.ib(type=float, default=time.time())
    end_time = attr.ib(type=float, default=None)
    watches = attr.ib(type={}, factory=dict)

    def end(self):
        for watch in self.watches.values():
            watch.stop()

        self.end_time = time.time()

    def watch(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if func.__name__ not in self.watches.keys():
                self.watches[func.__name__] = Watch(target=func.__name__)

            look = self.watches[func.__name__].start_look()

            func_output = func(*args, **kwargs)

            watch = self.watches[func.__name__]
            watch.stop_look(look)

            return func_output
        return wrapper
