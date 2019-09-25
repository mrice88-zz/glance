import glance
from glance.errors import GlanceLookOpenError
import pytest

look = glance.Look("test", None)


def test_look_open_error():
    with pytest.raises(GlanceLookOpenError):
        look.look_time()
