from abc import ABC, abstractmethod
from pathlib import Path

from core.conf import Conf
from core.model.song import Song
from core.logger import Logger, LOG_CAT


class IAnalysisAlgorithm(ABC):
    """Interface that all analysis algorithms should implement.
    """

    @abstractmethod
    def set_song(self, song: Song) -> None:
        """Sets the song to analyze. Must be set before analyzing.
        """
        pass

    @abstractmethod
    def get_keystring(self) -> str:
        """Returns the key string to be used when searching for the config values of this algorithm.

        Returns:
            str: Key string
        """
        pass

    @abstractmethod
    def analyze(self) -> None:
        """Starts the analysis process. Stores results in the song itself.
        """
        pass


class Analyzer():
    """
    Manages the analysis process. Interface for the analysis algorithm
    """

    def __init__(self) -> None:
        """Constructs the analysis object.
        """
        self._analysisAlgorithm: IAnalysisAlgorithm | None = None

    def set_algorithm(self, analysisAalgorithm: IAnalysisAlgorithm) -> None:
        """Sets the analysis algorithm for this analysis run.

        Args:
            analysisAalgorithm (IAnalysisAlgorithm): algorithm object.
        """
        self._analysisAlgorithm = analysisAalgorithm

    def analyze(self, song: Song) -> None:
        """Analyzes the provided song. Stores results within the song itself.

        Args:
            song (Song): Song object to analyze.

        Raises:
            AssertionError: if the analysis algoritm is not set.
        """
        assert self._analysisAlgorithm is not None

        if song:
            self._analysisAlgorithm.set_song(song)
            self._analysisAlgorithm.analyze()

        else:
            raise ValueError('Song cannot be None')

# ----------------------------------------------------
