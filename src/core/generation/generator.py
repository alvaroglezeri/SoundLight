from allin1.config import HARMONIX_LABELS

from src.core.exceptions import InvalidStateException

from ..model.song import Song
from ..logger import Logger, LOG_CAT
from ..model.features import *


class IGenerationAlgorithm(ABC):
    """Interface that all generation algorithms must have.
    """
    @abstractmethod
    def load_metadata(self, metadata: dict) -> None:
        """Loads metadata into the generation for later use.
        """
        pass

    @abstractmethod
    def generate(self) -> List[IFeature]:
        """Generates the features for the song.

        Returns:
            List[IFeature]: Features generated.
        """
        pass

# --------------------------------------------------------------------------


class Generator():
    """
    Manages the feature generation process. Requires a generation algorithm.
    """

    def __init__(self) -> None:
        """Constructs the generator object.
        """
        self._generationAlgorithm = None
        self._patch = None

    def set_algorithm(self, algorithm: IGenerationAlgorithm) -> None:
        """Sets the generation algorithm.

        Args:
            algorithm (IAnalysisAlgorithm): algorithm object.
        """
        if not isinstance(algorithm, IGenerationAlgorithm):
            raise InvalidArgumentException(
                'The algorithm provided is invalid!')
        self._generationAlgorithm = algorithm

    def set_patch(self, patch: dict) -> None:
        """Sets the patch to generate for.
        """
        # TODO: Update this function to work with the fixture type from src.model.fixtures
        if not isinstance(patch, dict):
            raise InvalidArgumentException(
                'The patch provided must be a dict instance!')

        # Checking patch structure
        if not patch or 'fixtureTypes' not in patch or not patch['fixtureTypes'] \
                or not isinstance(patch['fixtureTypes'], dict):
            raise InvalidArgumentException(
                'The patch does not follow the required structure!')

        # TODO: Check for valid fixture types
        for ftype in patch['fixtureTypes'].keys():
            if not patch['fixtureTypes'][ftype] \
                    or not isinstance(patch['fixtureTypes'][ftype], dict) \
                    or 'fixtures' not in patch['fixtureTypes'][ftype] \
                    or not isinstance(patch['fixtureTypes'][ftype]['fixtures'], list):
                raise InvalidArgumentException(
                    f'The content for feature {ftype} is invalid!')
        self._patch: dict = patch

    def generate(self, song: Song) -> None:
        """Arranges features based on the file metadata, according to the algorithm set.

        Args:
            song (Song): Song object for which to generate the features.
        """
        if not isinstance(song, Song):
            raise InvalidArgumentException('No song provided!')
        if not self._generationAlgorithm:
            raise InvalidStateException('No algorithm set!')
        if not self._patch:
            raise InvalidStateException('No patch set!')

        Logger.log(LOG_CAT.INFO, f'Starting feature generation...')

        # TODO: Use the patch data to calculate which features to generate.
        song['patch'] = self._patch
        self._generationAlgorithm.load_metadata(song['metadata'])

        song['features'] = self._generationAlgorithm.generate()
        # for feature in self._algorithm.generate():
        #    song['features'].append(feature)
