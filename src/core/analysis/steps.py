from allin1.analyze import analyze
from allin1.sonify import sonify
from allin1.visualize import visualize
from allin1.typings import AnalysisResult
from deeprhythm import DeepRhythmPredictor

import librosa
import numpy as np
from typing import BinaryIO, cast

class KeyAnalysis():
    """
    WRITE
    """
    
    # Define the mapping of chroma features to keys
    CHROMA_TO_KEY = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    @staticmethod
    def getKey(file: BinaryIO) -> str:
        """
        WRITE
        https://medium.com/@oluyaled/detecting-musical-key-from-audio-using-chroma-feature-in-python-72850c0ae4b1
        """   
        # Load the audio file from the beginning: https://github.com/bastibe/python-soundfile/issues/333
        # DOCUMENT: Take note of this
        file.seek(0)  
        y, sr = librosa.load(file)

        # Compute the Chroma Short-Time Fourier Transform (chroma_stft)
        chromagram = librosa.feature.chroma_stft(y=y, sr=sr)

        # Calculate the mean chroma feature across time
        mean_chroma = np.mean(chromagram, axis=1)

        # Find the key by selecting the maximum chroma feature
        estimated_key_index = np.argmax(mean_chroma)
        estimated_key = KeyAnalysis.CHROMA_TO_KEY[estimated_key_index]

        return estimated_key
    
    
class BeatAnalysis():
    
    @staticmethod
    def getBeat_deeprhythm(file: BinaryIO) -> tuple[float, float, list[float]]:
        """
    WRITE
    """
        file.seek(0)
        model = DeepRhythmPredictor(quiet=True)

        #As the audio is loaded with Librosa, it supports loading an BinaryIO file
        bpm, confidence = model.predict(file, include_confidence=True)

        file.seek(0)
        y, sr = librosa.load(file)
        _, beats = librosa.beat.beat_track(y=y, bpm = bpm)
        beats = librosa.frames_to_time(beats, sr=sr) 

        return bpm, confidence, beats # type: ignore

    @staticmethod
    def getBeat_AIO(filepath: str) -> AnalysisResult:
        """
    WRITE
    """
        # DOCUMENT: AIO does not support BinaryIO objects.

        print(f'Analyzing...')
        result = analyze(filepath, out_dir='./output', keep_byproducts=True)

        #print(f'Sonifying...')
        #sonified = allin1.sonify(result, multiprocess=False, out_dir='./output')

        #print(f'Visualizing...')
        #figure = allin1.visualize(result, multiprocess=False, out_dir='./output')

        # Either this or # type: ignore can be used to avoid warnings
        return cast(AnalysisResult, result)
    
    @staticmethod
    def getBeat_librosa(file: BinaryIO) -> dict:
        """
    WRITE
    """
        # Load the audio file        
        file.seek(0)
        y, sr = librosa.load(file)

        bpm, beats = librosa.beat.beat_track(y=y ,sr=sr)

        pulse = librosa.beat.plp(y=y, sr=sr)
        beats_plp = np.flatnonzero(librosa.util.localmax(pulse))

        data: dict = {
            'beat_track': (bpm, beats), 
            'plp': (beats_plp)
        }

        return data 
    
    
    
    
    