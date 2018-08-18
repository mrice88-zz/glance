import time
import matplotlib
import maya
import itertools
import attr


@attr.s
class Glance(object):
    start_time = attr.ib()
    end_time = attr.ib()
    look = attr.ib(type=list, default=[])
    current_start = attr.ib(default=None)
    current_end = attr.ib(default=None)

    def __attrs_post_init(self):
        self.start_time = time.time()

    def end(self):
        self.end_time = time.time()

    def start_look(self):
        if self.current_end:
            pass  # This needs to break.
        else:
            self.current_start = time.time()

    def end_look(self):
        self.current_end = time.time()

        if self.current_start:
            self.look.append(
                {
                    'start': self.current_start,
                    'end': self.current_end,
                }
            )

            self.current_start = None
            self.current_end = None

