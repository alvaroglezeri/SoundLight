
from io import BufferedReader, BytesIO, RawIOBase
from pathlib import Path
from typing import Iterator

from pytest import fixture, raises

from src.core.exceptions import InvalidArgumentException
from src.core.model.song import Song

# -------------------------------------------------------------------------------
# Song Object Creation Tests
# -------------------------------------------------------------------------------


@fixture
def get_raw_song() -> Iterator[BufferedReader]:
    path = Path('./resources/CamelPhat, Yannis, Foals - Hypercolour.wav')
    with open(path, 'rb') as song:
        yield song


def test_invalid_file(get_raw_song: BufferedReader) -> None:
    song_raw = get_raw_song
    song_raw.close()

    with raises(InvalidArgumentException):
        song = Song(song_raw)


def test_invalid_file2() -> None:
    with raises(InvalidArgumentException):
        song = Song(None)


def test_invalid_file3() -> None:
    with raises(InvalidArgumentException):
        song = Song(object)


def test_valid_file(get_raw_song: BufferedReader) -> None:
    song_raw = get_raw_song
    song = Song(song_raw)

    assert song['file'] is song_raw


def test_eq(get_raw_song: BufferedReader) -> None:
    song_raw = get_raw_song

    song1 = Song(song_raw)
    song2 = Song(song_raw)

    assert song1 == song2
