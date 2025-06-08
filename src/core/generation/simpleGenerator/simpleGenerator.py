from ast import If
import random
from allin1.typings import Segment

from core.logger import Logger, LOG_CAT
from core.model.features import IFeature

from ..generator import IGenerationAlgorithm
from ...model.features import *


class SimpleGenerator(IGenerationAlgorithm):
    """Simple Feature generation algorithm, to showcase the features of the program.
    """

    def __init__(self) -> None:
        super().__init__()

    def load_metadata(self, metadata: dict) -> None:
        """
        Loads the required metadata from the dict:
        """
        self._beats = metadata['aio']['beats']
        self._segments = metadata['aio']['segments']
        self._bass = metadata['stems']['bass']['peaks']
        self._bpm = metadata['deeprythm']['bpm']

    def generate(self) -> List[IFeature]:
        ret: List[IFeature] = []

        # for f in self._generateTransitionFlashes():
        #     ret.append(f)

        ret.extend(self._generate_section_specific())
        print(f'Generated {len(ret)} features')

        return ret

    # -----------------------------------------------------------------

    def _generate_transition_flashes(self) -> List[IFeature]:
        """Generates flashes at the transition points of the song.
        """
        Logger.log(LOG_CAT.INFO, f'Starting generation of transition flashes...')

        ret = []
        section: Segment
        for section in self._segments:
            start: int = int(section.start * 1000)
            if start != 0:
                ret.append(SimpleFlash(start, 1000))

        return ret

    def _generate_beat_tracking(self) -> List[IFeature]:
        """Generates beat traking features.
        """
        ret = []
        for i in range(len(self._beats)):
            match i % 4:
                case 0:
                    c = 'white'
                case 1:
                    c = 'red'
                case 2:
                    c = 'green'
                case 3:
                    c = 'blue'
                case _:
                    c = 'white'
            ret.append(RGBWFlash(self._beats[i], 350, c))

        return ret

    def _generate_section_specific(self) -> List[IFeature]:
        """Generates a color wash for each section.
        """
        ret = []
        section_counter = {
            'start': 0,
            'end': 0,
            'intro': 0,
            'outro': 0,
            'break': 0,
            'bridge': 0,
            'inst': 0,
            'solo': 0,
            'verse': 0,
            'chorus': 0,
        }

        for section in self._segments:
            start: int = int(section.start * 1000)
            duration = int((section.end - section.start) * 1000)
            match section.label:
                case 'chorus':
                    ret.append(SimpleFlash(start, 1000))
                    ret.append(RGBWFlash(start, duration, 'red'))
                    if section_counter['chorus'] > 0:
                        ret.extend(
                            self._generate_Rot_flash_beat_tracking(section))
                    else:
                        ret.extend(
                            self._generate_Rot_flash_beat_tracking(section, 'all2'))
                case 'verse':
                    ret.append(RGBWFlash(start, duration, 'green'))
                    if section_counter['verse'] == 0:
                        ret.extend(self._generate_simple_flash_beat_tracking(
                            section, 'alternating'))
                    elif section_counter['verse'] != 0:
                        ret.extend(self._generate_Rot_flash_beat_tracking(
                            section, 'all2'))

                case 'bridge':
                    ret.append(SimpleFlash(start, 1000))
                    ret.append(RGBWFlash(start, duration, 'blue'))
                    ret.extend(
                        self._generate_Rot_flash_beat_tracking(section, 'bar'))

                case 'break':
                    ret.append(SimpleFlash(start, 1000))
                    ret.append(RGBWFlash(start, duration, 'white'))

                case 'inst':
                    ret.append(SimpleFlash(start, 1000))
                    ret.append(RGBWFlash(start, duration, 'white'))
                    ret.extend(
                        self._generate_Rot_flash_beat_tracking(section, 'bar'))

                case 'outro':
                    ret.append(SimpleFlash(start, 1000))
                    ret.extend(
                        self._generate_Rot_flash_beat_tracking(section, 'bar'))

                case _:
                    ret.extend(
                        self._generate_Rot_flash_beat_tracking(section, 'bar'))
            section_counter[section.label] += 1
        return ret

    def _generate_simple_flash_beat_tracking(self, section, mode: str = 'all') -> List[IFeature]:
        """Generates beat tracking in a specific section.

        Modes:
            'all'
            'alternating'
        """
        ret = []
        start: int = int(section.start * 1000)
        duration = int((section.end - section.start) * 1000)
        end = start + duration

        # Getting the beats of this section
        section_beats = [int(b*1000)
                         for b in self._beats if start <= int(b*1000) < end]

        match mode:
            # Generating a flash each beat, 4 per bar
            case 'all':
                for b in section_beats:
                    ret.append(SimpleFlash(b, 250, 'all'))

            # Generating a flash each beat, alternating sides.
            case 'alternating':
                even = True
                for b in section_beats:
                    if even:
                        ret.append(SimpleFlash(b, 250, 'even'))
                    else:
                        ret.append(SimpleFlash(b, 250, 'odd'))
                    even = not even

        return ret

    def _generate_Rot_flash_beat_tracking(self, section, mode: str = 'all') -> List[IFeature]:
        """Generates beat tracking in a specific section.

        Modes:
            'all'
            'all2'
            'bar'
        """
        ret = []
        start: int = int(section.start * 1000)
        duration = int((section.end - section.start) * 1000)
        end = start + duration

        # Getting the beats of this section
        section_beats = [int(b*1000)
                         for b in self._beats if start <= int(b*1000) < end]

        match mode:
            # Generating a flash each beat, 4 per bar
            case 'all':
                even = True
                for b in section_beats:
                    if even:
                        ret.append(RotFlash(b, 250, 'yellow'))
                    else:
                        ret.append(RotFlash(b, 250, 'magenta'))
                    even = not even

            case 'all2':
                even = True
                for b in section_beats:
                    if even:
                        ret.append(RotFlash(b, 250, 'magenta'))
                    else:
                        ret.append(RotFlash(b, 250, 'cyan'))
                    even = not even

            # Generating a flash each bar
            case 'bar':
                # Taking each 4th element
                section_beats = section_beats[0::4]
                yellow = True
                for b in section_beats:
                    if yellow:
                        ret.append(RotFlash(b, 1500, 'yellow'))
                    else:
                        ret.append(RotFlash(b, 1500, 'magenta'))
                    yellow = not yellow
        return ret
