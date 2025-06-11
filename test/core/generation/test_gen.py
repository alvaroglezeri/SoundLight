from pathlib import Path
from typing import Iterator, List
from pytest import fixture, raises

from src.core.exceptions import InvalidArgumentException, InvalidStateException
from src.core.generation.generator import Generator, IGenerationAlgorithm
from src.core.model.features import IFeature
from src.core.model.song import Song


@fixture
def get_song() -> Iterator[Song]:
    path = Path('./resources/CamelPhat, Yannis, Foals - Hypercolour.wav')
    with open(path, 'rb') as song:
        yield Song(song)


@fixture
def get_valid_patch() -> dict:
    return {'fixtureTypes': {'ParCan': {'fixtures': []}}}


def get_patch(case) -> dict:
    # Fixture parametrization is out of the scope for such a simple test.
    match case:
        case 1:
            return {}
        case 2:
            return {'invalid_key': {}}
        case 3:
            return {'fixtureTypes': []}
        case 4:
            return {'fixtureTypes': {}}
        case 5:
            return {'fixtureTypes': {'invalid_key': {}}}
        case 6:
            return {'fixtureTypes': {'ParCan': []}}
        case 7:
            return {'fixtureTypes': {'ParCan': {}}}
        case 8:
            return {'fixtureTypes': {'ParCan': {'invalid_key': {}}}}
        case 9:
            return {'fixtureTypes': {'ParCan': {'fixtures': {}}}}
        case _:  # Valid case
            return {'fixtureTypes': {'ParCan': {'fixtures': []}}}


class MockGenerationAlg(IGenerationAlgorithm):
    """Mock implementation of the IGenerationAlgorithm interface for testing."""

    def load_metadata(self, metadata: dict) -> None:
        ...

    def generate(self) -> List[IFeature]:
        ...


# -------------------------------------------------------------------------------
# Generator Song Tests
# -------------------------------------------------------------------------------


def test_no_song(get_valid_patch) -> None:
    gen = Generator()
    gen.set_patch(get_valid_patch)
    gen.set_algorithm(MockGenerationAlg())

    with raises(TypeError):
        gen.generate()


def test_invalid_song(get_valid_patch) -> None:
    gen = Generator()
    gen.set_patch(get_valid_patch)
    gen.set_algorithm(MockGenerationAlg())

    with raises(InvalidArgumentException):
        gen.generate(object())


def test_valid_song(get_song, get_valid_patch) -> None:
    gen = Generator()
    gen.set_patch(get_valid_patch)
    gen.set_algorithm(MockGenerationAlg())

    gen.generate(get_song)

# -------------------------------------------------------------------------------
# Generator Algorithm Tests
# -------------------------------------------------------------------------------


def test_gen_no_alg() -> None:
    gen = Generator()

    with raises(TypeError):
        gen.set_algorithm()

    assert gen._generationAlgorithm == None


def test_gen_invalid_alg() -> None:
    gen = Generator()

    with raises(InvalidArgumentException):
        gen.set_algorithm(object())

    assert gen._generationAlgorithm == None


def test_gen_valid_alg() -> None:
    gen = Generator()
    mock = MockGenerationAlg()
    gen.set_algorithm(mock)

    assert gen._generationAlgorithm is mock

# -------------------------------------------------------------------------------
# Generator Patch Tests
# -------------------------------------------------------------------------------


def test_patch_no_patch() -> None:
    gen = Generator()
    with raises(TypeError):
        gen.set_patch()

    assert gen._patch == None


def test_patch_invalid_patch() -> None:
    gen = Generator()
    with raises(InvalidArgumentException):
        gen.set_patch(object())

    assert gen._patch == None


def test_patch_invalid_patch1() -> None:
    gen = Generator()
    with raises(InvalidArgumentException):
        gen.set_patch(get_patch(1))

    assert gen._patch == None


def test_patch_invalid_patch2() -> None:
    gen = Generator()
    with raises(InvalidArgumentException):
        gen.set_patch(get_patch(2))

    assert gen._patch == None


def test_patch_invalid_patch3() -> None:
    gen = Generator()
    with raises(InvalidArgumentException):
        gen.set_patch(get_patch(3))

    assert gen._patch == None


def test_patch_invalid_patch4() -> None:
    gen = Generator()
    with raises(InvalidArgumentException):
        gen.set_patch(get_patch(4))

    assert gen._patch == None


def test_patch_invalid_patch5() -> None:
    gen = Generator()
    with raises(InvalidArgumentException):
        gen.set_patch(get_patch(5))

    assert gen._patch == None


def test_patch_invalid_patch6() -> None:
    gen = Generator()
    with raises(InvalidArgumentException):
        gen.set_patch(get_patch(6))

    assert gen._patch == None


def test_patch_invalid_patch7() -> None:
    gen = Generator()
    with raises(InvalidArgumentException):
        gen.set_patch(get_patch(7))

    assert gen._patch == None


def test_patch_invalid_patch8() -> None:
    gen = Generator()
    with raises(InvalidArgumentException):
        gen.set_patch(get_patch(8))

    assert gen._patch == None


def test_patch_invalid_patch9() -> None:
    gen = Generator()
    with raises(InvalidArgumentException):
        gen.set_patch(get_patch(9))

    assert gen._patch == None


def test_patch_valid_patch(get_valid_patch) -> None:
    gen = Generator()
    patch = get_valid_patch
    gen.set_patch(patch)

    assert gen._patch is patch
