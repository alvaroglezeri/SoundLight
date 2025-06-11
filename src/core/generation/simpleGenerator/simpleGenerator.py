from allin1.typings import Segment

from src.core.generation.simpleGenerator.sections import Sections

from ...logger import Logger, LOG_CAT
from ...model.features import IFeature

from ..generator import IGenerationAlgorithm
from ...model.features import *


class SimpleGenerator(IGenerationAlgorithm):
    """Simple Feature generation algorithm, to showcase the features of the program.
    """

    def __init__(self) -> None:
        super().__init__()

    def load_metadata(self, metadata: dict) -> None:
        """
        Loads the required metadata from the provided dict.
        """
        self._beats: List[float] = metadata['aio']['beats']
        self._segments: List[Segment] = metadata['aio']['segments']
        self._bass = metadata['stems']['bass']['peaks']
        self._bpm = metadata['deeprythm']['bpm']

    def generate(self) -> List[IFeature]:
        ret: List[IFeature] = []

        # The SimpleGenerator just generates features based on the section.
        # No other metadata is used for now.
        sections = Sections(self._segments, self._bass)
        ret.extend(sections.generate_section_specific())

        return ret

    # --------------------------------------------------------------------------
