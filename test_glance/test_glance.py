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


