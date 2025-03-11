from os import PathLike
from pathlib import Path

from core.fileManager import FileManager
from core.analysis.analysisDirector import AnalysisDirector
from core.generation.featureGenerator import FeatureGenerator
from core.generation.simpleGenerator import SimpleGenerator
from core.export.daslight5.Daslight5Exporter import Daslight5Exporter
from core.lightGroups import *
from core import logger


class SoundLight():
    """
    WRITE
    """

    def __init__(self) -> None:
        self._fm = FileManager()
        self._ad = AnalysisDirector()
        self._gen = FeatureGenerator(
            SimpleGenerator(), fixtureGroups=self._createFixtureGroups())
        self._ex = Daslight5Exporter()

    def _createFixtureGroups(self) -> list[Group]:
        ret = list()
        parcan = ParCan()
        ret.append()

    def enableLogger(self, setting: bool) -> None:
        logger.enable = setting

    def addFileFromPath(self, path: str) -> None:
        self._fm.loadFileFromPath(path)

    def selectFile(self, i: int) -> None:
        self._fm.selectFile(i)

    def analyze(self) -> None:
        self._ad.analyze()

    def generate(self) -> None:
        self._gen.generate()

    def export(self, path: str) -> None:
        self._ex.export(Path(path))
