from pathlib import Path
from pytest import raises

from src.core.conf import Conf
from src.core.exceptions import InvalidArgumentException
from src.core.soundlight import SoundLight

# -------------------------------------------------------------------------------
# Configuration File Loading Tests
# -------------------------------------------------------------------------------


def test_blank_config_path() -> None:
    """
    Test SoundLight initialization with no config path.
    Should raise a TypeError because a required argument is missing.
    """
    with raises(TypeError):
        sl = SoundLight()  # type: ignore


def test_invalid_config_path() -> None:
    """
    Test SoundLight initialization with an argument of incorrect type.
    Passing an integer should raise an ArgumentException.
    """
    with raises(InvalidArgumentException):
        sl = SoundLight(1)  # type: ignore


def test_invalid_config_path2() -> None:
    """
    Test SoundLight with an invalid Path object.
    An empty Path should be considered invalid and raise ArgumentException.
    """
    with raises(InvalidArgumentException):
        # This resolves to '.' which is not a valid file
        sl = SoundLight(Path())


def test_not_existing_file() -> None:
    """
    Test SoundLight with a non-existent file path.
    Should raise ArgumentException because the config file does not exist.
    """
    with raises(InvalidArgumentException):
        sl = SoundLight('not_existent')


def test_invalid_file() -> None:
    """
    Test SoundLight with an existing file that is not a valid TOML config.
    Should raise ArgumentException.
    """
    with raises(InvalidArgumentException):
        sl = SoundLight('./run.py')


def test_valid_file() -> None:
    """
    Test SoundLight with a valid configuration file.
    Should successfully initialize and load the config as a dictionary.
    Also verifies that the configuration object is immutable.
    """
    sl = SoundLight('./soundlight.toml')

    config = Conf()
    assert config._config is not None
    assert isinstance(config._config, dict)
    assert len(config._config.items()) > 0

    # Attempting to mutate the config should raise an exception
    with raises(Exception):
        Conf()['0'] = None
