from glance import Look, Watch, Glance
import time
import dateutil.relativedelta
from datetime import datetime

# setup
look = Look("test")
time.sleep(1)
look.stop()

dt_start = datetime.fromtimestamp(time.time())
time.sleep(1)
dt_end = datetime.fromtimestamp(time.time())
time_delta = dateutil.relativedelta.relativedelta(dt_end, dt_start)

watch = Watch("test")
watch.looks[look.id] = look


def test_look_is_done():
    """
    Test is_done property in Look class is working

    :return:
    """
    from glance import Look
    look1 = Look('test')
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
    assert int(watch.longest_look()) == 2


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
    assert int(watch.shortest_look()) == 1


def test_watch_shortest_look_key():
    assert watch.shortest_look.key() == look.id


def test_watch_shortest_look_tuple():
    assert watch.shortest_look.tuple() == (look.id, look.look_time())


def test_watch_stop():
    watch.stop()
    for look in watch.looks.values():
        assert look.is_done is True

    assert watch.end_time is not None

