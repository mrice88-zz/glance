from glance import Look, Watch, Glance
import time
import dateutil.relativedelta
from datetime import datetime, timedelta

# setup
look = Look("test", None)
time.sleep(1)
look.stop()

dt_start = datetime.fromtimestamp(time.time())
time.sleep(1)
dt_end = datetime.fromtimestamp(time.time())
time_delta = dateutil.relativedelta.relativedelta(dt_end, dt_start)

watch = Watch("test")
watch.looks[look.id] = look

def look_generator(start, end, n):
    for i in range(1, n+1):
        look = Look(f"test_{i}", None)
        look.stop()
        look.start_time = start.timestamp()
        look.end_time = end.timestamp()
        yield look



def test_look_is_done():
    """
    Test is_done property in Look class is working

    :return:
    """
    from glance import Look
    look1 = Look('test', None)
    assert look1.is_done is False

    look1.stop()
    assert look1.is_done is True


def test_look_look_time():
    assert int(look.look_time()) is 1


def test_look_look_time_datetime():
    assert look.look_time.datetime().seconds == time_delta.seconds


def test_look_look_time_humanized():
    assert look.look_time.humanized() == '1 second'


def test_watch_start_look():
    look_id = watch.start_look()
    assert watch.looks[look_id] is not None
    assert watch.looks[look_id].is_done is False
    time.sleep(1.1)
    watch.stop_look(look_id)


def test_watch_longest_look():
    id = watch.start_look()
    time.sleep(2)
    watch.stop_look(id)
    assert round(watch.longest_look(), 2) == 2


def test_watch_longest_look_key():
    id = watch.start_look()
    time.sleep(3)
    watch.stop_look(id)
    assert watch.longest_look.key() == id


def test_watch_longest_look_tuple():
    id = watch.start_look()
    time.sleep(3.5)
    watch.stop_look(id)
    assert watch.longest_look.tuple()[0] == id
    assert type(watch.longest_look.tuple()) is tuple


def test_watch_shortest_look():
    assert round(watch.shortest_look(), 2) == 1


def test_watch_shortest_look_key():
    assert watch.shortest_look.key() == look.id


def test_watch_shortest_look_tuple():
    assert watch.shortest_look.tuple() == (look.id, look.look_time())


def test_watch_mean():
    assert round(watch.mean, 2) == 2.12


def test_watch_std():
    assert round(watch.std, 2) == 1.12


def test_watch_stop():
    watch.stop()
    for look in watch.looks.values():
        assert look.is_done is True

    assert watch.end_time is not None

def test_watch_outliers():
    one_sec_looks = list(look_generator(dt_start, dt_end, 5))
    two_sec_looks = list(look_generator(dt_start, dt_start + timedelta(seconds=2), 5))
    three_sec_looks = list(look_generator(dt_start, dt_start + timedelta(seconds=3), 5))
    twenty_sec_looks = list(look_generator(dt_start, dt_start + timedelta(seconds=25), 3))
    test_watch = Watch("test")
    for look in one_sec_looks +two_sec_looks + three_sec_looks +twenty_sec_looks:
        test_watch.looks[look.id] = look
    result = test_watch.find_outliers()
    assert result == [(look.id, look.look_time()) for look in twenty_sec_looks]
    assert len(result) == 3

def test_watch_weak_outliers():
    one_sec_looks = list(look_generator(dt_start, dt_end + timedelta(seconds=delta), 5))
    two_sec_looks = list(look_generator(dt_start, dt_start + timedelta(seconds=2+delta), 5))
    three_sec_looks = list(look_generator(dt_start, dt_start + timedelta(seconds=3+delta), 5))
    ten_sec_looks = list(look_generator(dt_start, dt_start + timedelta(seconds=10 + delta), 1))
    twenty_sec_looks = list(look_generator(dt_start, dt_start + timedelta(seconds=25+delta), 3))
    test_watch = Watch("test")
    for look in one_sec_looks +two_sec_looks + three_sec_looks + ten_sec_looks+twenty_sec_looks:
        test_watch.looks[look.id] = look
    result = test_watch.find_weak_outliers()
    assert result == [(look.id, look.look_time()) for look in ten_sec_looks + twenty_sec_looks]
    assert len(result) == 4


def make_watch(n, delta = 0):
    one_sec_looks = list(look_generator(dt_start, dt_end + timedelta(seconds=delta), 5))
    two_sec_looks = list(look_generator(dt_start, dt_start + timedelta(seconds=2+delta), 5))
    three_sec_looks = list(look_generator(dt_start, dt_start + timedelta(seconds=3+delta), 5))
    ten_sec_looks = list(look_generator(dt_start, dt_start + timedelta(seconds=10 + delta), 1))
    twenty_sec_looks = list(look_generator(dt_start, dt_start + timedelta(seconds=25+delta), 3))
    test_watch = Watch(f"test_{n}")
    for look in one_sec_looks +two_sec_looks + three_sec_looks + ten_sec_looks+twenty_sec_looks:
        test_watch.looks[look.id] = look
    return test_watch



# def test_two_watches():
#     test_watch_1 = make_watch(1)
#     test_watch_2 = make_watch(2, delta = 3)
#     test_glance = Glance()
#     test_glance.watches[test_watch_1.target] = test_watch_1
#     test_glance.watches[test_watch_2.target] = test_watch_2
