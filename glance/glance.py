import time
import attr
import variants
import uuid


@attr.s
class Look:
    target = attr.ib()
    start_time = attr.ib(type=float, default=None)
    id = attr.ib(type=str, default=None)
    end_time = attr.ib(type=float, default=None)

    def __attrs_post_init__(self):
        self.start_time = time.time()
        self.id = str(uuid.uuid4().int)

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
    looks = attr.ib(type={}, factory=dict)

    # def __attrs_post_init__(self):
    #     self.start_time = time.time()

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
        def wrapper(*args, **kwawrgs):
            if func.__name__ not in self.watches.keys():
                self.watches[func.__name__] = Watch(target=func.__name__)

            look = self.watches[func.__name__].start_look()

            func_output = func(*args, **kwawrgs)

            watch = self.watches[func.__name__]
            watch.stop_look(look)

            return func_output
        return wrapper


