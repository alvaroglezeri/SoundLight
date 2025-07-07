from pathlib import Path
from typing import Type
from pytest import raises

from src.core.exceptions import (
    InvalidArgumentException,
    DuplicateElementException,
    InvalidFileException,
    InvalidStateException,
    NotFoundException,
    NothingSelectedException,
)
from src.core.fileManager import FileManager
from src.core.soundlight import SoundLight

# -------------------------------------------------------------------------------
# Song Loading Tests
# -------------------------------------------------------------------------------

path1 = Path('./resources/CamelPhat, Yannis, Foals - Hypercolour.wav')
path2 = Path('./resources/Niklas Dee & Old Jim - Not Fair.mp3')
path3 = Path('./resources/Niklas Dee & Old Jim - Not Fair.wav')


def test_no_path() -> None:
    """
    Test calling add_song_from_path with no argument.
    Should raise TypeError due to missing required parameter.
    """
    sl = SoundLight('./soundlight.toml')
    with raises(TypeError):
        sl.add_song_from_path()


def test_invalid_path() -> None:
    """
    Test passing a non-existent path to add_song_from_path.
    Should raise FileNotFoundError.
    """
    sl = SoundLight('./soundlight.toml')
    with raises(FileNotFoundError):
        sl.add_song_from_path('invalid_path')


def test_invalid_file() -> None:
    """
    Try to load a non-audio file as a song.
    Should raise InvalidFileException.
    """
    sl = SoundLight('./soundlight.toml')
    with raises(InvalidFileException):
        sl.add_song_from_path('./run.py')


def test_valid_file() -> None:
    """
    Load a valid WAV file and ensure it's added to the song list.
    """
    sl = SoundLight('./soundlight.toml')
    sl.add_song_from_path(path1)

    assert len(sl.get_loaded_songs()) == 1
    assert Path(sl.get_loaded_songs()[0].get('path')) == path1


def test_duplicate_element() -> None:
    """
    Load the same song twice.
    Should raise DuplicateElementException on the second attempt.
    """
    sl = SoundLight('./soundlight.toml')
    sl.add_song_from_path(path1)

    with raises(DuplicateElementException):
        sl.add_song_from_path(path1)


def test_duplicate_element2() -> None:
    """
    Load MP3 version, then try to load its WAV equivalent.
    Should detect duplication after conversion and raise exception.
    """
    sl = SoundLight('./soundlight.toml')
    sl.add_song_from_path(path2)

    with raises(DuplicateElementException):
        sl.add_song_from_path(path3)


def test_file_conversion() -> None:
    """
    Add MP3 file, which gets converted to WAV.
    Verify the selected song path is the converted WAV version.
    """
    sl = SoundLight('./soundlight.toml')
    sl.add_song_from_path(path2)
    sl.select_song(0)

    assert Path(sl.get_selected_song()['path']) == path3


# -------------------------------------------------------------------------------
# Song Selection Tests
# -------------------------------------------------------------------------------

def test_empty_select() -> None:
    """
    Call get_selected_song without loading or selecting anything.
    Should raise NothingSelectedException.
    """
    sl = SoundLight('./soundlight.toml')

    with raises(NothingSelectedException):
        sl.get_selected_song()

    assert len(sl.get_loaded_songs()) == 0


def test_empty_select2() -> None:
    """
    Load one song but do not select it.
    get_selected_song should still raise NothingSelectedException.
    """
    sl = SoundLight('./soundlight.toml')
    sl.add_song_from_path(path1)

    with raises(NothingSelectedException):
        sl.get_selected_song()

    assert len(sl.get_loaded_songs()) == 1


def test_invalid_selection() -> None:
    """
    Try selecting a song from an empty list.
    Should raise NotFoundException.
    """
    sl = SoundLight('./soundlight.toml')
    with raises(NotFoundException):
        sl.select_song(0)


def test_invalid_selection2() -> None:
    """
    Load one song, then try to select an out-of-range index.
    Should raise NotFoundException and leave no selection.
    """
    sl = SoundLight('./soundlight.toml')
    sl.add_song_from_path(path1)

    with raises(NotFoundException):
        sl.select_song(1)

    with raises(NothingSelectedException):
        sl.get_selected_song()


def test_invalid_index() -> None:
    """
    Try selecting a song using an invalid (non-int) index.
    Should raise ArgumentException.
    """
    sl = SoundLight('./soundlight.toml')

    with raises(InvalidArgumentException):
        sl.select_song('invalid_index')  # type: ignore

    with raises(NothingSelectedException):
        sl.get_selected_song()


def test_valid_index() -> None:
    """
    Load and select a song by index.
    get_selected_song should return the correct song.
    """
    sl = SoundLight('./soundlight.toml')
    sl.add_song_from_path(path1)

    assert len(sl.get_loaded_songs()) == 1
    sl.select_song(0)

    assert sl.get_selected_song() is not None
    assert Path(sl.get_selected_song()['path']) == path1


def test_song_list() -> None:
    sl = SoundLight('./soundlight.toml')
    sl.add_song_from_path(path1)
    sl.add_song_from_path(path3)

    assert sl.get_loaded_songs() is not None
    assert len(sl.get_loaded_songs()) == 2

    sl.select_song(0)
    assert sl.get_selected_song() is not None
    assert sl.get_selected_song()['path'] == str(path1) 

    sl.select_song(1)
    assert sl.get_selected_song() is not None
    assert sl.get_selected_song()['path'] == str(path3)


# -------------------------------------------------------------------------------
# Song Closing Tests
# -------------------------------------------------------------------------------

def test_close_no_select() -> None:
    """
    Try to close a loaded but not selected song.
    Should raise NothingSelectedException.
    """
    sl = SoundLight('./soundlight.toml')
    sl.add_song_from_path(path1)

    with raises(NothingSelectedException):
        sl.close_selected_song()

    
def test_close_no_loaded() -> None:
    """
    Try to close when no song is loaded.
    Should raise NothingSelectedException.
    """
    sl = SoundLight('./soundlight.toml')

    with raises(NothingSelectedException):
        sl.close_selected_song()


def test_close_selected() -> None:
    """
    Try to close a loaded song.
    The list of songs should be empty, and no loaded song should remain.
    """
    sl = SoundLight('./soundlight.toml')
    sl.add_song_from_path(path1)
    sl.select_song(0)

    sl.close_selected_song()

    assert FileManager().has_selected_song() == False
    assert len(sl.get_loaded_songs()) == 0

def test_double_close() -> None:
    """
    Try to close an already closed song.
    Should raise NothingSelectedException.
    """
    sl = SoundLight('./soundlight.toml')
    sl.add_song_from_path(path1)
    sl.select_song(0)

    sl.close_selected_song()

    with raises(NothingSelectedException):
        sl.close_selected_song()
