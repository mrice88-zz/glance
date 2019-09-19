from glance import Glance
import itertools


def average_run(glance: Glance) -> float:
    run_times: list = []
    for i, peek in enumerate(glance.looks):
        peek_length = peek['end_time'] - peek['start_time']
        run_times.append(peek_length)


