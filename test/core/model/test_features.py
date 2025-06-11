

from pytest import raises
from src.core.exceptions import InvalidArgumentException
from src.core.model.features import IFeature, RGBWFlash, RotFlash, SimpleFlash


from io import BufferedReader, BytesIO, RawIOBase
from pathlib import Path
from typing import Iterator

from pytest import fixture, raises

from src.core.exceptions import InvalidArgumentException
from src.core.model.song import Song

# -------------------------------------------------------------------------------
# SimpleFlash Creation Tests
# -------------------------------------------------------------------------------


def test_SimpleFlash_creation1() -> None:
    f = SimpleFlash(100, 200)

    assert isinstance(f, IFeature)
    assert f.get_timestamp() == 100
    assert f.get_duration() == 200
    # Default mode
    assert f.get_mode() == f._MODES[0]


def test_SimpleFlash_creation2() -> None:
    with raises(ValueError):
        f = SimpleFlash('invalid', 200)

    with raises(ValueError):
        f = SimpleFlash(0, 'invalid')

    with raises(InvalidArgumentException):
        f = SimpleFlash(-100, 200)

    with raises(InvalidArgumentException):
        f = SimpleFlash(100, -200)

    with raises(InvalidArgumentException):
        f = SimpleFlash(100.100, 200)

    with raises(InvalidArgumentException):
        f = SimpleFlash(100, 200.200)


def test_SimpleFlash_creation3() -> None:
    f = SimpleFlash(100, 200, 'not_supported')
    assert f.get_mode() == f._MODES[0]

    f = SimpleFlash(100, 200, 'even')
    assert f.get_mode() == f._MODES[1]

    f = SimpleFlash(100, 200, 'odd')
    assert f.get_mode() == f._MODES[2]

# -------------------------------------------------------------------------------
# RGBWFlash Creation Tests
# -------------------------------------------------------------------------------


def test_RGBWFlash_creation1() -> None:
    f = RGBWFlash(100, 200)

    assert isinstance(f, IFeature)
    assert f.get_timestamp() == 100
    assert f.get_duration() == 200
    # Default mode
    assert f.get_mode() == f._MODES[0]


def test_RGBWFlash_creation2() -> None:
    with raises(ValueError):
        f = RGBWFlash('invalid', 200)

    with raises(ValueError):
        f = RGBWFlash(0, 'invalid')

    with raises(InvalidArgumentException):
        f = RGBWFlash(-100, 200)

    with raises(InvalidArgumentException):
        f = RGBWFlash(100, -200)

    with raises(InvalidArgumentException):
        f = RGBWFlash(100.100, 200)

    with raises(InvalidArgumentException):
        f = RGBWFlash(100, 200.200)


def test_RGBWFlash_creation3() -> None:
    f = RGBWFlash(100, 200, 'not_supported')
    assert f.get_mode() == f._MODES[0]

    f = RGBWFlash(100, 200, 'red')
    assert f.get_mode() == f._MODES[1]

    f = RGBWFlash(100, 200, 'green')
    assert f.get_mode() == f._MODES[2]

    f = RGBWFlash(100, 200, 'blue')
    assert f.get_mode() == f._MODES[3]

# -------------------------------------------------------------------------------
# RotFlash Creation Tests
# -------------------------------------------------------------------------------


def test_RotFlash_creation1() -> None:
    f = RotFlash(100, 200)

    assert isinstance(f, IFeature)
    assert f.get_timestamp() == 100
    assert f.get_duration() == 200
    # Default mode
    assert f.get_mode() == f._MODES[0]


def test_RotFlash_creation2() -> None:
    with raises(ValueError):
        f = RotFlash('invalid', 200)

    with raises(ValueError):
        f = RotFlash(0, 'invalid')

    with raises(InvalidArgumentException):
        f = RotFlash(-100, 200)

    with raises(InvalidArgumentException):
        f = RotFlash(100, -200)

    with raises(InvalidArgumentException):
        f = RotFlash(100.100, 200)

    with raises(InvalidArgumentException):
        f = RotFlash(100, 200.200)


def test_RotFlash_creation3() -> None:
    f = RotFlash(100, 200, 'not_supported')
    assert f.get_mode() == f._MODES[0]

    f = RotFlash(100, 200, 'magenta')
    assert f.get_mode() == f._MODES[1]

    f = RotFlash(100, 200, 'cyan')
    assert f.get_mode() == f._MODES[2]
