import librosa
import numpy as np
from deeprhythm import DeepRhythmPredictor


from typing import BinaryIO, List


class BeatAnalysis():
    """Performs beat, tempo and BPM detection
    """

    @staticmethod
    def get_beat_deeprhythm(file: BinaryIO) -> tuple[float, float, List[float]]:
        """Gets the beat timings of the file using DeepRhythm.

        Args:
            file (BinaryIO): Loaded file.

        Returns:
            tuple[float, float, List[float]]: BPM, confidence % and list with the timestamps for the beats.
        """
        file.seek(0)
        model = DeepRhythmPredictor(quiet=True)

        # As the audio is loaded with Librosa, it supports loading an BinaryIO file
        bpm, confidence = model.predict(file, include_confidence=True)

        file.seek(0)
        y, sr = librosa.load(file)
        _, beats = librosa.beat.beat_track(y=y, bpm=bpm)
        beats = librosa.frames_to_time(beats, sr=sr)

        return bpm, confidence, beats  # type: ignore

    @staticmethod
    def get_beat_librosa(file: BinaryIO) -> dict:
        """Gets the beat timings of the file using Librosa's beat_track and plp methods.

        Args:
            file (BinaryIO): Loaded file.

        Returns:
            dict: For key 'beat_track', the BPM and beats. For key 'plp', the beats
        """
        # Load the audio file
        file.seek(0)
        y, sr = librosa.load(file)

        bpm, beats = librosa.beat.beat_track(y=y, sr=sr)

        pulse = librosa.beat.plp(y=y, sr=sr)
        beats_plp = np.flatnonzero(librosa.util.localmax(pulse))

        data: dict = {
            'beat_track': (bpm, beats),
            'plp': (beats_plp)
        }

        return data
