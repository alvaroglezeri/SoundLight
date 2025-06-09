import pytest

from src.core.soundlight import SoundLight


def test_init():
    try:
        sl = SoundLight()
    except:
        pass


def test_always_passes():
    assert True


def test_always_fails():
    with pytest.raises(Exception) as e_info:
        assert False
