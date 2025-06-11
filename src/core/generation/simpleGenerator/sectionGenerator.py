
from typing import List
from allin1.typings import Segment

from src.core.model.features import IFeature, RGBWFlash, RotFlash, SimpleFlash


class SectionGenerator():
    """This class takes in a list of segments, and a list of beats, 
    """

    def __init__(self, segments: List[Segment], beats: List[float]) -> None:
        self._segments = segments
        # Converting beats from s to ms
        self._beats = [int(b*1000) for b in beats]

    def _simple_flash_bt(self, section: Segment, mode: str = 'all') -> List[IFeature]:
        """Generates beat tracking in a specific section with simple flashes.

        Modes:
            'all'
            'alternating'
        """
        ret = []
        start: int = int(section.start * 1000)
        duration = int((section.end - section.start) * 1000)
        end = start + duration

        # Getting the beats of this section
        section_beats = [b for b in self._beats if start <= b < end]

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

    def _rot_flash_bt(self, section: Segment, mode: str = 'all') -> List[IFeature]:
        """Generates beat tracking in a specific section with rotating flashes.

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
        section_beats = [b for b in self._beats if start <= b < end]

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

    # --------------------------------------------------------------------------

    def generate_section_specific(self) -> List[IFeature]:
        """Generates a color wash for each section.
        """
        ret = []
        self._section_counter = {
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
            match section.label:
                case 'chorus':
                    ret.extend(self._section_chrous(section))
                case 'verse':
                    ret.extend(self._section_verse(section))
                case 'bridge':
                    ret.extend(self._section_bridge(section))
                case 'break':
                    ret.extend(self._section_break(section))
                case 'inst':
                    ret.extend(self._section_inst(section))
                case 'outro':
                    ret.extend(self._section_outro(section))
                case _:
                    ret.extend(
                        self._rot_flash_bt(section, 'bar'))
            self._section_counter[section.label] += 1
        return ret

    def _section_chrous(self, section: Segment) -> List[IFeature]:
        ret = []
        start: int = int(section.start * 1000)
        duration = int((section.end - section.start) * 1000)

        ret.append(SimpleFlash(start, 1000))
        ret.append(RGBWFlash(start, duration, 'red'))
        if self._section_counter['chorus'] > 0:
            ret.extend(
                self._rot_flash_bt(section))
        else:
            ret.extend(
                self._rot_flash_bt(section, 'all2'))

        return ret

    def _section_verse(self, section: Segment) -> List[IFeature]:
        ret = []
        start: int = int(section.start * 1000)
        duration = int((section.end - section.start) * 1000)

        ret.append(RGBWFlash(start, duration, 'green'))
        if self._section_counter['verse'] == 0:
            ret.extend(self._simple_flash_bt(
                section, 'alternating'))
        elif self._section_counter['verse'] != 0:
            ret.extend(self._rot_flash_bt(
                section, 'all2'))

        return ret

    def _section_bridge(self, section: Segment) -> List[IFeature]:
        ret = []
        start: int = int(section.start * 1000)
        duration = int((section.end - section.start) * 1000)

        ret.append(SimpleFlash(start, 1000))
        ret.append(RGBWFlash(start, duration, 'blue'))
        ret.extend(
            self._rot_flash_bt(section, 'bar'))

        return ret

    def _section_break(self, section: Segment) -> List[IFeature]:
        ret = []
        start: int = int(section.start * 1000)
        duration = int((section.end - section.start) * 1000)

        ret.append(SimpleFlash(start, 1000))
        ret.append(RGBWFlash(start, duration, 'white'))

        return ret

    def _section_inst(self, section: Segment) -> List[IFeature]:
        ret = []
        start: int = int(section.start * 1000)
        duration = int((section.end - section.start) * 1000)

        ret.append(SimpleFlash(start, 1000))
        ret.append(RGBWFlash(start, duration, 'white'))
        ret.extend(
            self._rot_flash_bt(section, 'bar'))

        return ret

    def _section_outro(self, section: Segment) -> List[IFeature]:
        ret = []
        start: int = int(section.start * 1000)
        duration = int((section.end - section.start) * 1000)

        ret.append(SimpleFlash(start, 1000))
        ret.extend(
            self._rot_flash_bt(section, 'bar'))

        return ret
