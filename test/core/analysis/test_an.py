from pathlib import Path
from typing import Iterator
from pytest import fixture, raises

from src.core.analysis.analyzer import Analyzer, IAnalysisAlgorithm
from src.core.exceptions import InvalidArgumentException, InvalidStateException
from src.core.model.song import Song


@fixture
def get_song() -> Iterator[Song]:
    path = Path('./resources/CamelPhat, Yannis, Foals - Hypercolour.wav')
    with open(path, 'rb') as song:
        yield Song(song)


class MockAnalysisAlg(IAnalysisAlgorithm):
    """Mock implementation of the IAnalysisAlgorithm interface for testing."""

    def set_song(self, song: Song) -> None:
        ...

    def get_keystring(self) -> str:
        ...

    def analyze(self) -> None:
        ...


# -------------------------------------------------------------------------------
# Analyzer Song Tests
# -------------------------------------------------------------------------------


def test_no_song() -> None:
    an = Analyzer()
    an.set_algorithm(MockAnalysisAlg())

    with raises(TypeError):
        an.analyze()


def test_invalid_song() -> None:
    an = Analyzer()
    an.set_algorithm(MockAnalysisAlg())

    with raises(InvalidArgumentException):
        an.analyze(object())


def test_valid_song(get_song) -> None:
    an = Analyzer()
    an.set_algorithm(MockAnalysisAlg())

    an.analyze(get_song)


# -------------------------------------------------------------------------------
# Analyzer Algorithm Tests
# -------------------------------------------------------------------------------


def test_set_no_alg() -> None:
    an = Analyzer()

    with raises(TypeError):
        an.set_algorithm()

    assert an._analysisAlgorithm is None


def test_set_invalid_alg() -> None:
    an = Analyzer()

    with raises(InvalidArgumentException):
        an.set_algorithm(object())

    assert an._analysisAlgorithm is None


def test_set_valid_alg() -> None:
    an = Analyzer()
    mock = MockAnalysisAlg()
    an.set_algorithm(mock)

    assert an._analysisAlgorithm is mock


def test_analyze_no_alg(get_song) -> None:
    an = Analyzer()

    with raises(InvalidStateException):
        an.analyze(get_song)
