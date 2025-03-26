from abc import ABC, abstractmethod
from pathlib import Path

from allin1.typings import AnalysisResult
from core.analysis.beatAnalysis import BeatAnalysis
from core.analysis.keyAnalysis import KeyAnalysis
from core.analysis.phraseAnalysis import PhraseAnalysis
from core.analysis.stems.common import Common
from core.exceptions import DuplicateElementException, NotFoundException
from core.logger import Logger, LOG_CAT

from core.analysis import *
from core.analysis.stems.bassAnalysis import BassAnalysis

from core.fileManager import FileManager
from core.model.song import Song


class ISubscriber(ABC):
    # WRITE

    # type Notification = dict[str, object]

    @abstractmethod
    def update(data) -> None:
        pass


class AnalysisDirector():
    # WRITE

    def __init__(self) -> None:
        self._subscribers: list[ISubscriber] = []
        self._fm: FileManager = FileManager()
        self._key: KeyAnalysis = KeyAnalysis
        self._selected: Song = None

    def subscribe(self, subscriber: ISubscriber) -> None:
        # WRITE
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)
        else:
            raise DuplicateElementException(f'Already subscribed')

    def _notify(self, msg) -> None:
        for subscriber in self._subscribers:
            subscriber.update(msg)

    def analyze(self) -> None:
        # WRITE

        self._notify({"step": "1", "msg": "Loading file..."})
        self._loadFile()
        self._notify({"step": "1", "msg": "Loaded file."})

        self._notify({"step": "2", "msg": "Analyzing key..."})
        self._keyAnalysis()
        self._notify({"step": "2", "msg": "Analized key."})

        self._notify({"step": "3", "msg": "Analyzing beat with DeepRhythm..."})
        self._beatDeeprhythm()
        self._notify({"step": "3", "msg": "Analized beat."})

        self._notify({"step": "4", "msg": "Analyzing sections..."})
        self._sectionAIO()
        self._notify({"step": "4", "msg": "Analized sections."})

        self._notify({"step": "5", "msg": "Analyzing stems..."})
        self._stemAnalysis()
        self._notify({"step": "5", "msg": "Analized stems."})

        self._notify({"finished": True})

# ----------------------------------------------------

    def _loadFile(self) -> None:
        # Step 1: Load file
        file = self._fm.getSelectedSong()

        if file is None:
            self._notify({"step": "1", "msg": "No file selected"})
            Logger.log(LOG_CAT.ERROR, f'No file selected!')
            raise NotFoundException(f'No file selected!')
        else:
            self._selected = file
            self._notify({"step": "1", "msg": f'Selected {file.title}'})
            Logger.log(LOG_CAT.INFO, f'Selected "{file.title}"')

# ----------------------------------------------------

    def _keyAnalysis(self) -> None:
        # Step 2: Key analysis

        key: str = KeyAnalysis.getKey(self._selected.file)
        self._notify({"step": "2", "msg": f'Got key: {key}'})
        Logger.log(LOG_CAT.INFO, f'Found key: {key}')
        self._fm.getSelectedSong().addMetadata('key.key', key)

    def _beatDeeprhythm(self) -> None:
        # Step 3: Beat analysis

        bpm, confidence, beats = BeatAnalysis.getBeat_deeprhythm(
            self._selected.file)
        self._notify({"step": "3", "msg": f'Got bpm: {bpm}'})
        self._notify({"step": "3", "msg": f'Got beats: {beats}'})
        Logger.log(LOG_CAT.INFO,
                   f'Found bpm: {bpm} with {confidence*100//1}% confidence.')

        self._fm.getSelectedSong().addMetadata('deeprhythm.bpm', bpm)
        self._fm.getSelectedSong().addMetadata('deeprhythm.confidence', confidence)
        self._fm.getSelectedSong().addMetadata('deeprhythm.beats', beats)

    def _sectionAIO(self) -> None:
        Logger.log(LOG_CAT.INFO, f'Running AIO analysis...')

        results: AnalysisResult = PhraseAnalysis.getSections_AIO(
            self._selected.path)

        Logger.log(LOG_CAT.SUCCESS, f'AIO Analysis complete.')

        song: Song = self._fm.getSelectedSong()
        resultDict = results.__dict__
        resultDict['demucs'] = {}
        Logger.log(
            LOG_CAT.INFO, f'Saving path to demixes to "demix/htdemucs/{Path(song.path).with_suffix("").name}/<stem>.wav')
        resultDict['demucs']['bass'] = Path(
            f'demix/htdemucs/{Path(song.path).with_suffix("").name}/bass.wav')
        resultDict['demucs']['drums'] = Path(
            f'demix/htdemucs/{Path(song.path).with_suffix("").name}/drums.wav')
        resultDict['demucs']['other'] = Path(
            f'demix/htdemucs/{Path(song.path).with_suffix("").name}/other.wav')
        resultDict['demucs']['vocals'] = Path(
            f'demix/htdemucs/{Path(song.path).with_suffix("").name}/vocals.wav')

        song.addMetadata(f'aio', results.__dict__)

    def _stemAnalysis(self) -> None:
        Logger.log(LOG_CAT.INFO, f'Starting stem analysis...')

        Logger.log(LOG_CAT.INFO, f' > Bass Analysis:')
        bass_peaks = BassAnalysis(self._selected).analyze(
            display=True, sonify=True)
        Logger.log(LOG_CAT.SUCCESS, f'Successfully analized bass stem')
