from json import JSONDecodeError
from pathlib import Path
from pytest import raises

from src.core.analysis.simpleAlgorithm.simpleAlgorithm import SimpleAlgorithm
from src.core.exceptions import InvalidArgumentException
from src.core.export.daslight5.Daslight5Exporter import Daslight5Exporter
from src.core.generation.simpleGenerator.simpleGenerator import SimpleGenerator
from src.core.soundlight import SoundLight

# -------------------------------------------------------------------------------
# Patch Loading Tests
# -------------------------------------------------------------------------------


def test_patch_no_path() -> None:
    """
    Test calling set_patch() without an argument.
    Should raise TypeError due to missing required argument.
    """
    sl = SoundLight('./soundlight.toml')
    with raises(TypeError):
        sl.set_patch_from_path()
    assert sl._patchLoaded is False


def test_patch_invalid_path() -> None:
    """
    Test calling set_patch() with an invalid Path.
    An empty Path should raise a ValueError.
    """
    sl = SoundLight('./soundlight.toml')
    with raises(ValueError):
        sl.set_patch_from_path(Path())
    assert sl._patchLoaded is False


def test_patch_invalid_file() -> None:
    """
    Test calling set_patch() with an invalid JSON file.
    Should raise a JSON exception due to parsing errors.
    """
    sl = SoundLight('./soundlight.toml')
    with raises(JSONDecodeError):
        sl.set_patch_from_path(Path('./run.py'))
    assert sl._patchLoaded is False


def test_patch_valid_patch() -> None:
    """
    Test setting a valid patch file.
    The patch should be successfully loaded and contain expected structure.
    """
    sl = SoundLight('./soundlight.toml')
    assert sl._patchLoaded is False

    sl.set_patch_from_path('resources/patch.json')
    assert sl._patchLoaded is True
    assert sl._patch is not None
    assert isinstance(sl._patch, dict)
    assert len(sl._patch.keys()) == 1
    assert len(sl._patch['fixtureTypes'].keys()) == 3


# -------------------------------------------------------------------------------
# Analysis Algorithm Tests
# -------------------------------------------------------------------------------

def test_analysis_no_argument() -> None:
    """
    Test setting analysis algorithm with no argument.
    Should raise TypeError.
    """
    sl = SoundLight('./soundlight.toml')
    with raises(TypeError):
        sl.set_analysis_algorithm()
    assert sl._analysisAlgorithmSet is False


def test_analysis_invalid_argument() -> None:
    """
    Test setting analysis algorithm with invalid argument type.
    Should raise ArgumentException.
    """
    sl = SoundLight('./soundlight.toml')
    with raises(InvalidArgumentException):
        sl.set_analysis_algorithm(object)
    assert sl._analysisAlgorithmSet is False


def test_analysis_valid_argument() -> None:
    """
    Test setting a valid analysis algorithm.
    Should assign algorithm and mark it as set.
    """
    sl = SoundLight('./soundlight.toml')
    assert sl._analysisAlgorithmSet is False

    alg = SimpleAlgorithm()
    sl.set_analysis_algorithm(alg)

    assert sl._analysisAlgorithmSet is True
    assert sl._an._analysisAlgorithm is alg


# -------------------------------------------------------------------------------
# Generation Algorithm Tests
# -------------------------------------------------------------------------------

def test_generation_no_argument() -> None:
    """
    Test setting generation algorithm with no argument.
    Should raise TypeError.
    """
    sl = SoundLight('./soundlight.toml')
    with raises(TypeError):
        sl.set_generation_algorithm()
    assert sl._generationAlgorithmSet is False


def test_generation_invalid_argument() -> None:
    """
    Test setting generation algorithm with invalid argument type.
    Should raise ArgumentException.
    """
    sl = SoundLight('./soundlight.toml')
    with raises(InvalidArgumentException):
        sl.set_generation_algorithm(object)
    assert sl._generationAlgorithmSet is False


def test_generation_valid_argument() -> None:
    """
    Test setting a valid generation algorithm.
    Should assign algorithm and mark it as set.
    """
    sl = SoundLight('./soundlight.toml')
    assert sl._generationAlgorithmSet is False

    alg = SimpleGenerator()
    sl.set_generation_algorithm(alg)

    assert sl._generationAlgorithmSet is True
    assert sl._gen._generationAlgorithm is alg


# -------------------------------------------------------------------------------
# Export Algorithm Tests
# -------------------------------------------------------------------------------

def test_export_no_argument() -> None:
    """
    Test setting export algorithm with no argument.
    Should raise TypeError.
    """
    sl = SoundLight('./soundlight.toml')
    with raises(TypeError):
        sl.set_export_algorithm()
    assert sl._exportAlgorithmSet is False


def test_export_invalid_argument() -> None:
    """
    Test setting export algorithm with invalid argument type.
    Should raise ArgumentException.
    """
    sl = SoundLight('./soundlight.toml')
    with raises(InvalidArgumentException):
        sl.set_export_algorithm(object)
    assert sl._exportAlgorithmSet is False


def test_export_valid_argument() -> None:
    """
    Test setting a valid export algorithm.
    Should assign algorithm and mark it as set.
    """
    sl = SoundLight('./soundlight.toml')
    assert sl._exportAlgorithmSet is False

    alg = Daslight5Exporter()
    sl.set_export_algorithm(alg)

    assert sl._exportAlgorithmSet is True
    assert sl._ex._exportAlgorithm is alg


# -------------------------------------------------------------------------------
# Export Path Tests
# -------------------------------------------------------------------------------

def test_exportPath_no_argument() -> None:
    """
    Test setting export path with no argument.
    Should raise TypeError.
    """
    sl = SoundLight('./soundlight.toml')
    with raises(TypeError):
        sl.set_export_path()
    assert sl._exportPath is None


def test_exportPath_invalid_argument() -> None:
    """
    Test setting export path with an invalid argument type.
    Should raise ArgumentException.
    """
    sl = SoundLight('./soundlight.toml')
    with raises(InvalidArgumentException):
        sl.set_export_path(object)
    assert sl._exportPath is None


def test_exportPath_invalid_argument2() -> None:
    """
    Test setting export path with a file instead of a directory.
    Should raise ArgumentException.
    """
    sl = SoundLight('./soundlight.toml')
    with raises(InvalidArgumentException):
        sl.set_export_path('./soundlight.toml')
    assert sl._exportPath is None


def test_exportPath_valid_argument() -> None:
    """
    Test setting a valid export path.
    Should set path and mark it as configured.
    """
    sl = SoundLight('./soundlight.toml')
    assert sl._exportPathSet is False

    path = Path('./output')
    sl.set_export_path(path)

    assert sl._exportPathSet is True
    assert sl._exportPath == path
