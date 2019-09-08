import time
import attr
import variants
import uuid
# import functools


@attr.s
class Look:
    target = attr.ib()
    start_time = attr.ib(type=float, default=time.time())
    id = attr.ib(type=str, default=str(uuid.uuid4()))
    end_time = attr.ib(type=float, default=None)

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
    looks = attr.ib(type={}, default={})

    def start_look(self):
        look = Look(self.target)
        self.looks[look.id] = look
        return look.id

    # def last_look(self) -> (Look, None):
    #     if self.looks:
    #         return self.looks[-1]
    #     else:
    #         return None

    def stop_look(self, look_id):
        look = self.looks[look_id]
        look.stop()

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

            look = self.watches[func.__name__].start_look()

            func_output = func(*args, **kwawrgs)

            watch = self.watches[func.__name__]
            watch.stop_look(look)

            return func_output
        return wrapper


