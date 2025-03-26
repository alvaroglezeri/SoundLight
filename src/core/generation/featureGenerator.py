from deprecated import deprecated
from allin1.typings import Segment
from allin1.config import HARMONIX_LABELS
from warnings import *

from core.logger import Logger, LOG_CAT
from core.model.features import *
from core.fileManager import FileManager
from core.model.lightGroups import Group


class IGenerationAlgorithm(ABC):
    """
    WRITE
    """
    @abstractmethod
    def loadMetadata(self, metadata: dict) -> None:
        pass

    @abstractmethod
    def generateTransitionFeatures(self) -> list[IFeature]:
        pass

    @abstractmethod
    def generateOther(self) -> list[IFeature]:
        pass

    @abstractmethod
    def addFixtureGroup(self, group: Group) -> None:
        pass


class IFeatureExporter(ABC):
    """
    WRITE
    """
    @abstractmethod
    def generate(self, feature: IFeature) -> str:
        pass

# -----------------------------------------------------


class FeatureGenerator():
    """
    WRITE
    Arranges the feature generation steps. Requires a generation algorithm.
    """

    def __init__(self, generator: IGenerationAlgorithm, fixtureGroups: list[Group] | None) -> None:
        self._fm: FileManager = FileManager()
        self._generator: IGenerationAlgorithm = generator

        # We add all available fixture groups to the generator
        for group in fixtureGroups:
            self._generator.addFixtureGroup(group)

    def loadMetadata(self, metadata: dict) -> None:
        Logger.log(LOG_CAT.INFO, f'Loading metadata...')
        print()
        print(metadata)

    def generate(self, metadata: dict) -> None:
        """
        Arranges features based on the file metadata. Main algorithm for the generator
        """
        Logger.log(LOG_CAT.INFO, f'Starting feature generation...')
        self._generator.loadMetadata(metadata)

        self._fm.getSelectedSong().addFeatures(
            self._generator.generateTransitionFeatures())
