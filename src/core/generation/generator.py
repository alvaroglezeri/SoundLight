from allin1.config import HARMONIX_LABELS

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

    def set_algorithm(self, algorithm: IGenerationAlgorithm) -> None:
        """Sets the generation algorithm.
        """
        self._generationAlgorithm = algorithm

    def set_patch(self, patch: dict) -> None:
        """Sets the patch to generate for.
        """
        self._patch: dict = patch

    def generate(self, song: Song) -> None:
        """Arranges features based on the file metadata, according to the algorithm set.

        Args:
            song (Song): Song object for which to generate the features.
        """
        assert self._generationAlgorithm, "No algorithm set!"
        assert self._patch, "No patch loaded!"

        Logger.log(LOG_CAT.INFO, f'Starting feature generation...')

        song['patch'] = self._patch
        self._generationAlgorithm.load_metadata(song['metadata'])

        song['features'] = self._generationAlgorithm.generate()
        # for feature in self._algorithm.generate():
        #    song['features'].append(feature)
