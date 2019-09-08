import time
import attr
import variants
import functools


@attr.s
class Look:
    target = attr.ib()
    start_time = attr.ib(type=float, default=time.time())
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
    start_time = attr.ib(type=float, default=time.time())
    end_time = attr.ib(type=float, default=None)
    looks = attr.ib(type=[], default=[])

    def start_look(self):
        self.looks.append(Look(self.target))

    def last_look(self) -> (Look, None):
        if self.looks:
            return self.looks[-1]
        else:
            return None

    def stop(self):
        self.end_time = time.time()


@attr.s
class Glance:
    start_time = attr.ib(type=float, default=time.time())
    end_time = attr.ib(type=float, default=None)
    watches = attr.ib(type={}, default={})

    def end(self):
        for watch in self.watches.values():
            watch.stop()

        self.end_time = time.time()

    def watch(self, func):
        def wrapper(*args, **kwawrgs):
            if func.__name__ not in self.watches.items():
                self.watches[func.__name__] = Watch(target=func.__name__)

            self.watches[func.__name__].start_look()

            func_output = func(*args, **kwawrgs)

            self.watches[func.__name__].last_look().stop()

            return func_output
        return wrapper


