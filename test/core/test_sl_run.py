from io import BytesIO
from pathlib import Path
import time
import typing
from pytest import raises, fixture

from src.core.analysis.analyzer import Analyzer, IAnalysisAlgorithm
from src.core.exceptions import InvalidStateException
from src.core.export.exporter import Exporter, IExportAlgorithm
from src.core.generation.generator import Generator, IGenerationAlgorithm
from src.core.model.features import IFeature, List
from src.core.model.song import Song
from src.core.soundlight import SoundLight

MAX_TIME_NO_GPU = 10
MAX_TIME_GPU = 2
_RUN_TEST_NB = 0

# -------------------------------------------------------------------------------
# Mock Algorithm Implementations
# -------------------------------------------------------------------------------


class MockExportAlg(IExportAlgorithm):
    """Mock implementation of the IExportAlgorithm interface for testing."""

    def __init__(self) -> None:
        # By default, returns OK
        self._returns_list()

    def set_song(self, song: Song) -> None:
        self._song = song

    def get_keystring(self) -> str:
        return 'MockExportAlg'

    @property
    def file_extension(self) -> str:
        global _RUN_TEST_NB
        _RUN_TEST_NB += 1
        return f'test{_RUN_TEST_NB}'

    def export(self) -> List[str] | BytesIO:
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


class MockAnalysisAlg(IAnalysisAlgorithm):
    """Mock implementation of the IAnalysisAlgorithm interface for testing."""

    def set_song(self, song: Song) -> None:
        ...

    def get_keystring(self) -> str:
        ...

    def analyze(self) -> None:
        ...


class MockGenerationAlg(IGenerationAlgorithm):
    """Mock implementation of the IGenerationAlgorithm interface for testing."""

    def set_song(self, song: Song) -> None:
        self._song = song

    def get_keystring(self) -> str:
        return 'MockGenerationAlg'

    def generate(self) -> List[IFeature]:
        ...


# -------------------------------------------------------------------------------
# Test Setup Fixture
# -------------------------------------------------------------------------------

@fixture
def setup_sl() -> typing.Iterator[SoundLight]:
    """
    Fixture that sets up a fully configured SoundLight instance,
    including a loaded song, patch, algorithms, and export path.
    """
    # Setup phase of the test fixture
    sl = SoundLight('./soundlight.toml')

    song = Path('./resources/Niklas Dee & Old Jim - Not Fair.mp3')
    sl.add_song_from_path(song)
    sl.select_song(0)

    sl.set_analysis_algorithm(MockAnalysisAlg())
    sl.set_generation_algorithm(MockGenerationAlg())
    sl.set_export_algorithm(MockExportAlg())

    patch = Path('./resources/patch.json')
    sl.set_patch_from_path(patch)

    export = Path('./output')
    sl.set_export_path(export)

    yield sl

    # Teardown phase of the test fixture. Not strictly needed, but more verbose
    del sl


# -------------------------------------------------------------------------------
# Core Run Functionality Tests
# -------------------------------------------------------------------------------

def test_run_autocreate(setup_sl: SoundLight) -> None:
    """
    Verify that the Analyzer, Generator, and Exporter components are
    automatically instantiated and assigned after setup.
    """
    sl = setup_sl

    assert sl._an is not None
    assert isinstance(sl._an, Analyzer)
    assert sl._an._analysisAlgorithm is not None
    assert isinstance(sl._an._analysisAlgorithm, IAnalysisAlgorithm)

    assert sl._gen is not None
    assert isinstance(sl._gen, Generator)
    assert sl._gen._generationAlgorithm is not None
    assert isinstance(sl._gen._generationAlgorithm, IGenerationAlgorithm)

    assert sl._ex is not None
    assert isinstance(sl._ex, Exporter)
    assert sl._ex._exportAlgorithm is not None
    assert isinstance(sl._ex._exportAlgorithm, IExportAlgorithm)


def test_run_checks1(setup_sl: SoundLight) -> None:
    """
    Force analysis algorithm unset and verify that run() raises InvalidStateException.
    """
    sl = setup_sl
    sl._analysisAlgorithmSet = False

    with raises(InvalidStateException):
        sl.run()


def test_run_checks2(setup_sl: SoundLight) -> None:
    """
    Force generation algorithm unset and verify that run() raises InvalidStateException.
    """
    sl = setup_sl
    sl._generationAlgorithmSet = False

    with raises(InvalidStateException):
        sl.run()


def test_run_checks3(setup_sl: SoundLight) -> None:
    """
    Force export algorithm unset and verify that run() raises InvalidStateException.
    """
    sl = setup_sl
    sl._exportAlgorithmSet = False

    with raises(InvalidStateException):
        sl.run()


def test_run_checks4(setup_sl: SoundLight) -> None:
    """
    Simulate missing patch file (unset flag) and verify exception on run().
    """
    sl = setup_sl
    sl._patchLoaded = False

    with raises(InvalidStateException):
        sl.run()


def test_run_checks5(setup_sl: SoundLight) -> None:
    """
    Simulate export path not set and verify that run() raises InvalidStateException.
    """
    sl = setup_sl
    sl._exportPathSet = False

    with raises(InvalidStateException):
        sl.run()

# -------------------------------------------------------------------------------
# Run Performance Tests
# -------------------------------------------------------------------------------


def test_sl_performance(setup_sl: SoundLight) -> None:
    start = time.perf_counter()
    sl = setup_sl
    sl.run()
    end = time.perf_counter()

    time_taken = end - start    # In seconds
    song_length = sl.get_selected_song(
    )['metadata']['tinytag']['duration']  # In seconds

    if sl._gpu_available():
        assert time_taken < song_length * MAX_TIME_GPU
    else:
        assert time_taken < song_length * MAX_TIME_NO_GPU
