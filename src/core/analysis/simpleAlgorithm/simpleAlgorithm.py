from pathlib import Path
from allin1.typings import AnalysisResult

from ..analyzer import IAnalysisAlgorithm
from ..simpleAlgorithm.beatAnalysis import BeatAnalysis
from ..simpleAlgorithm.keyAnalysis import KeyAnalysis
from ..simpleAlgorithm.phraseAnalysis import PhraseAnalysis
from ..simpleAlgorithm.bassAnalysis import BassAnalysis
from ...conf import Conf
from ...logger import LOG_CAT, Logger
from ...model.song import Song


class SimpleAlgorithm(IAnalysisAlgorithm):
    """Simple analysis algorithm. Performs key detection, beat and tempo detection, section segmenting, and bass stem peak detection.
    """

    def set_song(self, song: Song) -> None:
        self._song = song

    def get_keystring(self) -> str:
        return 'simpleAlgorithm'

    def analyze(self) -> None:
        self._key_analysis()
        self._beats_deeprhythm()
        self._sections_aio()
        self._bass_analysis()

    # --------------------------------------------------------------------------

    def _key_analysis(self) -> None:
        """Analyzes the key of the song.
        """

        key: str = KeyAnalysis.get_key(self._song['file'])
        Logger.log(LOG_CAT.INFO, f'Found key: {key}')
        self._song['metadata']['key'] = key

    # --------------------------------------------------------------------------

    def _beats_deeprhythm(self) -> None:
        """Analyzes the beat of the song with Deeprhythm.
        """

        bpm, confidence, beats = BeatAnalysis.get_beat_deeprhythm(
            self._song['file'])
        Logger.log(
            LOG_CAT.INFO, f'Found bpm: {bpm} with {confidence*100//1}% confidence.')

        self._song['metadata']['deeprythm'] = {}
        self._song['metadata']['deeprythm']['bpm'] = bpm
        self._song['metadata']['deeprythm']['confidence'] = confidence
        self._song['metadata']['deeprythm']['beats'] = beats

    # --------------------------------------------------------------------------

    def _sections_aio(self) -> None:
        """Analyzes the sections of the song with AllIn1
        """
        Logger.log(LOG_CAT.INFO, f'Running AIO analysis...')

        results: AnalysisResult = PhraseAnalysis.get_sections_aio(
            self._song['path'])

        Logger.log(LOG_CAT.SUCCESS, f'AIO Analysis complete.')

        demixPath = Conf()['analysis']['simpleAlgorithm']['aio']['demix_dir']
        resultDict = results.__dict__
        resultDict['demucs'] = {}
        Logger.log(
            LOG_CAT.INFO, f"Saving path to demixes to '{demixPath}/{Path(self._song['path']).with_suffix('').name}/<stem>.wav'")
        resultDict['demucs']['bass'] = Path(
            f"{demixPath}/{Path(self._song['path']).with_suffix('').name}/bass.wav")
        resultDict['demucs']['drums'] = Path(
            f"{demixPath}/{Path(self._song['path']).with_suffix('').name}/drums.wav")
        resultDict['demucs']['other'] = Path(
            f"{demixPath}/{Path(self._song['path']).with_suffix('').name}/other.wav")
        resultDict['demucs']['vocals'] = Path(
            f"{demixPath}/{Path(self._song['path']).with_suffix('').name}/vocals.wav")

        self._song['metadata']['aio'] = results.__dict__
        # We delete the absolute path loaded by AIO to avoid confusions with song['path]
        if 'path' in self._song['metadata']['aio']:
            del self._song['metadata']['aio']['path']

    # --------------------------------------------------------------------------

    def _bass_analysis(self) -> None:
        """Analyzes the bass stem to detect peaks.
        """
        Logger.log(LOG_CAT.INFO, f'Starting stem analysis...')
        Logger.log(LOG_CAT.INFO, f' > Bass Analysis:')

        bass_peaks = BassAnalysis(self._song).analyze()

        if 'stems' not in self._song['metadata']:
            self._song['metadata']['stems'] = {}
        self._song['metadata']['stems']['bass'] = {}
        self._song['metadata']['stems']['bass']['peaks'] = bass_peaks
        Logger.log(LOG_CAT.SUCCESS, f'Successfully analized bass stem')
