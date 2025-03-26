import librosa
import numpy as np
from deeprhythm import DeepRhythmPredictor


from typing import BinaryIO


class BeatAnalysis():

    @staticmethod
    def getBeat_deeprhythm(file: BinaryIO) -> tuple[float, float, list[float]]:
        """
    WRITE
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
    def getBeat_librosa(file: BinaryIO) -> dict:
        """
        WRITE
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
