import librosa
import numpy as np


from typing import BinaryIO


class KeyAnalysis():
    """
    WRITE
    """

    # Define the mapping of chroma features to keys
    CHROMA_TO_KEY = ['C', 'C#', 'D', 'D#', 'E',
                     'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    @staticmethod
    def getKey(file: BinaryIO) -> str:
        """
        WRITE
        https://medium.com/@oluyaled/detecting-musical-key-from-audio-using-chroma-feature-in-python-72850c0ae4b1
        """
        # DOCUMENT: It is necessary to load the audio file from the beginning: https://github.com/bastibe/python-soundfile/issues/333

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
