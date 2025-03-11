from deprecated import deprecated
from allin1.typings import Segment
from allin1.config import HARMONIX_LABELS
from warnings import *

from core.logger import DCL, LOG_CAT
from core.generation.features import *
from core.fileManager import FileManager
from core.lightGroups import Group


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

    def generate(self, metadata: dict) -> None:
        """
        Arranges features based on the file metadata. Main algorithm for the generator
        """
        DCL.log(LOG_CAT.INFO, f'Starting feature generation...')
        self._generator.loadMetadata(metadata)

        # self._loadMetadata()

        self._fm.addFeatures(self._generator.generateTransitionFeatures())

    @deprecated
    def generate(self) -> None:
        """
        Arranges features based on the file metadata. Main algorithm for the generator
        """
        DCL.log(LOG_CAT.INFO, f'Starting feature generation...')
        self._generator.loadMetadata(self._fm.getMetadata())

        # self._loadMetadata()

        self._fm.addFeatures(self._generator.generateTransitionFeatures())
