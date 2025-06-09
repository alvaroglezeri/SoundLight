from pathlib import Path
from pytest import raises

from src.core.conf import Conf
from src.core.exceptions import ArgumentException, DuplicateElementException, InvalidFileException, NotFoundException, NothingSelectedException
from src.core.soundlight import SoundLight

# -------------------------------------------------------------------------------
# Loading songs
# -------------------------------------------------------------------------------

path1 = Path('./resources/CamelPhat, Yannis, Foals - Hypercolour.wav')
path2 = Path('./resources/Niklas Dee & Old Jim - Not Fair.mp3')
path3 = Path('./resources/Niklas Dee & Old Jim - Not Fair.wav')


def test_no_path() -> None:
    sl = SoundLight('./soundlight.toml')

    with raises(TypeError):
        sl.add_song_from_path()


def test_invalid_path() -> None:
    sl = SoundLight('./soundlight.toml')

    with raises(FileNotFoundError):
        sl.add_song_from_path('invalid_path')


def test_invalid_path2() -> None:
    sl = SoundLight('./soundlight.toml')

    with raises(ValueError):
        sl.set_patch(Path())


def test_invalid_file() -> None:
    sl = SoundLight('./soundlight.toml')

    with raises(InvalidFileException):
        sl.add_song_from_path('./run.py')


def test_valid_file() -> None:
    sl = SoundLight('./soundlight.toml')
    sl.add_song_from_path(path1)

    assert len(sl.get_loaded_songs()) == 1
    assert Path(sl.get_loaded_songs()[0].get('path')) == path1


def test_duplicate_element() -> None:
    sl = SoundLight('./soundlight.toml')

    sl.add_song_from_path(path1)

    with raises(DuplicateElementException):
        sl.add_song_from_path(path1)


def test_duplicate_element2() -> None:
    sl = SoundLight('./soundlight.toml')

    sl.add_song_from_path(path2)

    with raises(DuplicateElementException):
        sl.add_song_from_path(path3)


def test_file_conversion() -> None:
    sl = SoundLight('./soundlight.toml')
    sl.add_song_from_path(path2)
    sl.select_song(0)

    # Checking that the file conversion has been performed
    assert Path(sl.get_selected_song()['path']) == path3

# -------------------------------------------------------------------------------
# Selecting elements
# -------------------------------------------------------------------------------


def test_empty_select() -> None:
    sl = SoundLight('./soundlight.toml')

    with raises(NothingSelectedException):
        sl.get_selected_song()

    assert len(sl.get_loaded_songs()) == 0


def test_empty_select2() -> None:
    sl = SoundLight('./soundlight.toml')
    sl.add_song_from_path(path1)

    with raises(NothingSelectedException):
        sl.get_selected_song()

    assert len(sl.get_loaded_songs()) == 1


def test_invalid_selection() -> None:
    sl = SoundLight('./soundlight.toml')
    with raises(NotFoundException):
        sl.select_song(0)


def test_invalid_selection2() -> None:
    sl = SoundLight('./soundlight.toml')
    sl.add_song_from_path(path1)

    with raises(NotFoundException):
        sl.select_song(1)

    with raises(NothingSelectedException):
        sl.get_selected_song()


def test_invalid_index() -> None:
    sl = SoundLight('./soundlight.toml')

    with raises(ArgumentException):
        sl.select_song('invalid_index')

    with raises(NothingSelectedException):
        sl.get_selected_song()


def test_valid_index() -> None:
    sl = SoundLight('./soundlight.toml')
    sl.add_song_from_path(path1)

    assert len(sl.get_loaded_songs()) == 1
    sl.select_song(0)

    assert sl.get_selected_song() != None
    assert Path(sl.get_selected_song()['path']) == path1
