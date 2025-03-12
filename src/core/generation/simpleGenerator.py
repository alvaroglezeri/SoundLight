from allin1.typings import Segment

from core.logger import Logger, LOG_CAT

from .featureGenerator import IGenerationAlgorithm
from ..model.features import *
from ..model.lightGroups import *


class SimpleGenerator(IGenerationAlgorithm):
    def __init__(self) -> None:
        super().__init__()

    def loadMetadata(self, metadata: dict) -> None:
        """
        WRITE
        """
        self._beats = metadata['aio.beats']
        self._segments = metadata['aio.segments']

    def generateTransitionFeatures(self) -> list[IFeature]:
        """
        WRITE
        """
        Logger.log(LOG_CAT.INFO, f'Starting generation of transition features...')

        ret = []
        section: Segment
        for section in self._segments:
            label = '{:8}'.format(f'"{section.label}"')
            Logger.log(LOG_CAT.INFO,
                       f'Generating for section {label} ({section.start})...')
            """
            Section labels from allin1.config.HARMONIX_LABELS
            'start',
            'end',
            'intro',
            'outro',
            'break',
            'bridge',
            'inst',
            'solo',
            'verse',
            'chorus',
            """
            match section.label:
                case "start":   # Start segment is ignored
                    pass
                case _:  # Default segment switch
                    start = float("{:.2f}".format(section.start))
                    duration = float("{:.2f}".format(
                        section.end - section.start))
                    ret.append(SimpleFlash(start, duration, ParCan()))
                    pass

        return ret

    def generateOther(self) -> list[IFeature]:
        return list()

    def addFixtureGroup(self, group) -> None:
        pass
