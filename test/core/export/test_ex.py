from io import BytesIO
from pathlib import Path
from typing import Iterator, List
from unittest.mock import Mock
from pytest import fixture, raises

from src.core.exceptions import InvalidArgumentException, InvalidStateException
from src.core.export.exporter import Exporter, IExportAlgorithm
from src.core.model.song import Song

_TEST_NB = 0


@fixture
def get_song() -> Iterator[Song]:
    path = Path('./resources/CamelPhat, Yannis, Foals - Hypercolour.wav')
    with open(path, 'rb') as song:
        s = Song(song)
        s._struct['title'] = 'Test Song'
        yield s


@fixture
def export_path() -> Path:
    return Path(f'./test/results')


class MockExportAlg(IExportAlgorithm):
    """Mock implementation of the IExportAlgorithm interface for testing."""

    def __init__(self) -> None:
        # By default, returns OK
        self._returns_list()

    @property
    def file_extension(self) -> str:
        global _TEST_NB
        _TEST_NB += 1
        return f'test{_TEST_NB}'

    def export(self, song: Song) -> None:
        ...

    def get(self) -> List[str] | BytesIO:
        return self.ret  # type: ignore

    # As the exporter expects a result, we test the handling

    def _returns_list(self) -> 'MockExportAlg':
        self.ret = ['line1', 'line2']
        return self

    def _returns_bytesIO(self) -> 'MockExportAlg':
        self.ret = BytesIO(b'bytesbytesbytesbytesbytesbytes')
        return self

    def _returns_None(self) -> 'MockExportAlg':
        self.ret = None
        return self

    def _returns_other(self) -> 'MockExportAlg':
        self.ret = {'invalid': 'test'}
        return self


# -------------------------------------------------------------------------------
# Exporter Song Tests
# -------------------------------------------------------------------------------


def test_no_song() -> None:
    ex = Exporter()
    mock = MockExportAlg()
    ex.set_algorithm(mock)

    with raises(TypeError):
        ex.set_song()


def test_invalid_song() -> None:
    ex = Exporter()
    mock = MockExportAlg()
    ex.set_algorithm(mock)

    with raises(InvalidArgumentException):
        ex.set_song(object())


def test_valid_song(get_song) -> None:
    ex = Exporter()
    mock = MockExportAlg()
    ex.set_algorithm(mock)
    song = get_song
    ex.set_song(song)

    assert ex._song is song


def test_export_no_song(export_path) -> None:
    ex = Exporter()
    ex.set_algorithm(MockExportAlg())

    with raises(InvalidStateException):
        ex.export(export_path)

# -------------------------------------------------------------------------------
# Exporter Algorithm Tests
# -------------------------------------------------------------------------------


def test_set_no_alg() -> None:
    ex = Exporter()

    with raises(TypeError):
        ex.set_algorithm()

    assert ex._exportAlgorithm is None


def test_set_invalid_alg() -> None:
    ex = Exporter()

    with raises(InvalidArgumentException):
        ex.set_algorithm(object())

    assert ex._exportAlgorithm is None


def test_set_valid_alg() -> None:
    ex = Exporter()
    mock = MockExportAlg()
    ex.set_algorithm(mock)

    assert ex._exportAlgorithm is mock


def test_export_no_alg(get_song, export_path) -> None:
    ex = Exporter()
    ex.set_song(get_song)

    with raises(InvalidStateException):
        ex.export(export_path)

# -------------------------------------------------------------------------------
# Exporter Path Tests
# -------------------------------------------------------------------------------


def test_no_path(get_song) -> None:
    ex = Exporter()
    ex.set_song(get_song)
    ex.set_algorithm(MockExportAlg())

    with raises(TypeError):
        ex.export()


def test_invalid_path(get_song) -> None:
    ex = Exporter()
    ex.set_song(get_song)
    ex.set_algorithm(MockExportAlg())

    with raises(InvalidArgumentException):
        ex.export(object())


def test_valid_path(get_song, export_path) -> None:
    ex = Exporter()
    ex.set_song(get_song)
    ex.set_algorithm(MockExportAlg())

    ex.export(export_path)

# -------------------------------------------------------------------------------
# Exporter Return Tests
# -------------------------------------------------------------------------------


def test_return_list(get_song, export_path) -> None:
    ex = Exporter()
    ex.set_song(get_song)
    ex.set_algorithm(MockExportAlg()._returns_list())

    ex.export(export_path)


def test_return_bytesIO(get_song, export_path) -> None:
    ex = Exporter()
    ex.set_song(get_song)
    ex.set_algorithm(MockExportAlg()._returns_bytesIO())

    ex.export(export_path)


def test_return_none(get_song, export_path) -> None:
    ex = Exporter()
    ex.set_song(get_song)
    ex.set_algorithm(MockExportAlg()._returns_None())

    with raises(ValueError):
        ex.export(export_path)


def test_return_other(get_song, export_path) -> None:
    ex = Exporter()
    ex.set_song(get_song)
    ex.set_algorithm(MockExportAlg()._returns_other())

    with raises(ValueError):
        ex.export(export_path)
