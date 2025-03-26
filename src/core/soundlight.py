from os import PathLike
from pathlib import Path

from core.fileManager import FileManager
from core.analysis.analysisDirector import AnalysisDirector
from core.generation.featureGenerator import FeatureGenerator
from core.generation.simpleGenerator import SimpleGenerator
from core.export.daslight5.Daslight5Exporter import Daslight5Exporter
from core.model.lightGroups import *
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
        ret: list = list()
        parcan: ParCan = ParCan()

        # TODO
        ret.append(parcan)

        return ret

    def enableLogger(self, setting: bool) -> None:
        logger.enable = setting

    def addSongFromPath(self, path: str) -> None:
        self._fm.loadSong(path)

    def selectSong(self, i: int) -> None:
        self._fm.selectSong(i)

    def analyze(self) -> None:
        self._ad.analyze()

    def generate(self) -> None:
        self._gen.generate()

    def export(self, path: str) -> None:
        self._ex.export(Path(path))

    # ----------------

    def _printSongMetadata(self) -> None:
        for k1, v1 in self._fm.getSelectedSong().metadata.items():
            if type(v1) == dict:
                print(f'{k1}: ')
                for k2, v2 in v1.items():
                    print(f'  {k2}: {v2}')
            else:
                print(f'{k1}: {v1}')
