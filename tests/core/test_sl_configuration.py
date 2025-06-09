from pathlib import Path
from pytest import raises

from src.core.analysis.simpleAlgorithm.simpleAlgorithm import SimpleAlgorithm
from src.core.exceptions import ArgumentException
from src.core.export.daslight5.Daslight5Exporter import Daslight5Exporter
from src.core.generation.simpleGenerator.simpleGenerator import SimpleGenerator
from src.core.soundlight import SoundLight

# -------------------------------------------------------------------------------
# Patch
# -------------------------------------------------------------------------------


def test_patch_no_path() -> None:
    sl = SoundLight('./soundlight.toml')

    with raises(TypeError):
        sl.set_patch()

    assert sl._patchLoaded == False


def test_patch_invalid_path() -> None:
    sl = SoundLight('./soundlight.toml')

    with raises(ValueError):
        sl.set_patch(Path())

    assert sl._patchLoaded == False


def test_patch_valid_patch() -> None:
    sl = SoundLight('./soundlight.toml')
    assert sl._patchLoaded == False
    sl.set_patch('resources/patch.json')

    assert sl._patchLoaded == True
    assert sl._patch is not None
    assert isinstance(sl._patch, dict)
    assert len(sl._patch.keys()) == 1
    # FixtureTypes
    assert len(sl._patch['fixtureTypes'].keys()) == 3

# -------------------------------------------------------------------------------
# Analysis algorithm
# -------------------------------------------------------------------------------


def test_analysis_no_argument() -> None:
    sl = SoundLight('./soundlight.toml')

    with raises(TypeError):
        sl.set_analysis_algorithm()

    assert sl._analysisAlgorithmSet == False


def test_analysis_invalid_argument() -> None:
    sl = SoundLight('./soundlight.toml')

    with raises(ArgumentException):
        sl.set_analysis_algorithm(object)

    assert sl._analysisAlgorithmSet == False


def test_analysis_valid_argument() -> None:
    sl = SoundLight('./soundlight.toml')
    assert sl._analysisAlgorithmSet == False

    alg = SimpleAlgorithm()
    sl.set_analysis_algorithm(alg)

    assert sl._analysisAlgorithmSet == True
    assert sl._an._analysisAlgorithm is alg

# -------------------------------------------------------------------------------
# Generation algorithm
# -------------------------------------------------------------------------------


def test_generation_no_argument() -> None:
    sl = SoundLight('./soundlight.toml')

    with raises(TypeError):
        sl.set_generation_algorithm()

    assert sl._generationAlgorithmSet == False


def test_generation_invalid_argument() -> None:
    sl = SoundLight('./soundlight.toml')

    with raises(ArgumentException):
        sl.set_generation_algorithm(object)

    assert sl._generationAlgorithmSet == False


def test_generation_valid_argument() -> None:
    sl = SoundLight('./soundlight.toml')
    assert sl._generationAlgorithmSet == False

    alg = SimpleGenerator()
    sl.set_generation_algorithm(alg)

    assert sl._generationAlgorithmSet == True
    assert sl._gen._generationAlgorithm is alg

# -------------------------------------------------------------------------------
# Export algorithm
# -------------------------------------------------------------------------------


def test_export_no_argument() -> None:
    sl = SoundLight('./soundlight.toml')

    with raises(TypeError):
        sl.set_export_algorithm()

    assert sl._exportAlgorithmSet == False


def test_export_invalid_argument() -> None:
    sl = SoundLight('./soundlight.toml')

    with raises(ArgumentException):
        sl.set_export_algorithm(object)

    assert sl._exportAlgorithmSet == False


def test_export_valid_argument() -> None:
    sl = SoundLight('./soundlight.toml')
    assert sl._exportAlgorithmSet == False

    alg = Daslight5Exporter()
    sl.set_export_algorithm(alg)

    assert sl._exportAlgorithmSet == True
    assert sl._ex._exportAlgorithm is alg

# -------------------------------------------------------------------------------
# Export path
# -------------------------------------------------------------------------------


def test_exportPath_no_argument() -> None:
    sl = SoundLight('./soundlight.toml')

    with raises(TypeError):
        sl.set_export_path()

    assert sl._exportPath is None


def test_exportPath_invalid_argument() -> None:
    sl = SoundLight('./soundlight.toml')

    with raises(ArgumentException):
        sl.set_export_path(object)

    assert sl._exportPath is None


def test_exportPath_invalid_argument2() -> None:
    sl = SoundLight('./soundlight.toml')

    with raises(ArgumentException):
        sl.set_export_path('./soundlight.toml')

    assert sl._exportPath is None


def test_exportPath_valid_argument() -> None:
    sl = SoundLight('./soundlight.toml')
    assert sl._exportPathSet == False

    path = Path('./output')

    sl.set_export_path(path)

    assert sl._exportPathSet == True
    assert sl._exportPath == path
