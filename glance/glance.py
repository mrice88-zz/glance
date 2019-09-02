import time
import attr
import variants
import functools


@attr.s
class Look:
    start_time = attr.ib(type=float)
    end_time = attr.ib(type=float, default=None)

    def __attrs_post_init(self):
        self.start_time = time.time()

    @variants.primary
    def look_time(self):
        if self.end_time:
            return self.end_time - self.start_time

    @look_time.variant("datetime")
    def look_time(self):
        pass

    def stop(self):
        self.end_time = time.time()


@attr.s
class Watch:
    target = attr.ib(type=str)
    start_time = attr.ib()
    end_time = attr.ib()
    looks = attr.ib(type=[Look], default=[])

    def __attrs_post_init(self):
        self.start_time = time.time()

    @property
    def last_look(self) -> Look:
        return self.looks[-1]

    def stop(self):
        for look in self.looks:
            look.stop()
        self.end_time = time.time()


@attr.s
class Glance:
    start_time = attr.ib()
    end_time = attr.ib()
    watches = attr.ib(type={}, default={})
    current_start = attr.ib(default=None)
    current_end = attr.ib(default=None)

    def __attrs_post_init(self):
        self.start_time = time.time()

    def end(self):
        for watch in self.watches.values():
            watch.stop()

        self.end_time = time.time()

    def watch(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwawrgs):
            if func.__name__ not in self.watches.items():
                self.watches[func.__name__] = Watch(target=func.__name__)

            watch = self.watches[func.__name__]

            func_output = func(*args, **kwawrgs)

            watch.last_look.stop()

            return func_output

        return wrapper


