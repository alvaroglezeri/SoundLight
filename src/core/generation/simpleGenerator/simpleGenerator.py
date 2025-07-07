from allin1.typings import Segment

from ...exceptions import InvalidStateException
from ...generation.simpleGenerator.sections import Sections
from ...model.song import Song
from ...logger import Logger, LOG_CAT
from ...model.features import IFeature
from ..generator import IGenerationAlgorithm
from ...model.features import *


class SimpleGenerator(IGenerationAlgorithm):
    """Simple Feature generation algorithm, to showcase the features of the program.
    """

    def set_song(self, song: Song) -> None:
        self._song = song

    def get_keystring(self) -> str:
        return 'simpleGenerator'

    def generate(self) -> List[IFeature]:
        ret: List[IFeature] = []

        # Load the metadata from the song.
        if not self._song:
            raise InvalidStateException('No metadata found in the song.')
        else:
            self._load_metadata(self._song['metadata'])

        # The SimpleGenerator just generates features based on the section.
        # No other metadata is used for now.
        sections = Sections(self._segments, self._bass)
        ret.extend(sections.generate_section_specific())

        return ret

    # --------------------------------------------------------------------------

    def _load_metadata(self, metadata: dict) -> None:
        """
        Loads the required metadata from the provided dict.
        """
        self._beats: List[float] = metadata['aio']['beats']
        self._segments: List[Segment] = metadata['aio']['segments']
        self._bass = metadata['stems']['bass']['peaks']
        self._bpm = metadata['deeprythm']['bpm']
