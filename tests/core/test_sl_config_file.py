from pathlib import Path
from pytest import raises

from src.core.conf import Conf
from src.core.exceptions import ArgumentException
from src.core.soundlight import SoundLight

# -------------------------------------------------------------------------------
# Loading the configuration file
# -------------------------------------------------------------------------------


def test_blank_config_path() -> None:

    with raises(TypeError):
        # No Config file path provided
        sl = SoundLight()


def test_invalid_config_path() -> None:

    with raises(ArgumentException):
        # Argument is of invalid type
        sl = SoundLight(1)


def test_invalid_config_path2() -> None:

    with raises(ArgumentException):
        # Path is invalid itself
        sl = SoundLight(Path())


def test_not_existing_file() -> None:

    with raises(ArgumentException):
        # File does not exist
        sl = SoundLight('not_existent')


def test_invalid_file() -> None:

    with raises(ArgumentException):
        # File is not TOML
        sl = SoundLight('./run.py')


def test_valid_file() -> None:
    # File exists and is valid
    sl = SoundLight('./soundlight.toml')

    # Checking that it is loaded correctly
    assert Conf()._config is not None
    assert isinstance(Conf()._config, dict)
    assert len(Conf()._config.items()) > 0

    # Checking that the config cannot be modified
    with raises(Exception):
        Conf()['0'] = None
