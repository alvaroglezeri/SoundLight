from abc import ABC, abstractmethod
from core.exceptions import DuplicateElementException, NotFoundException
from core.logger import DCL, LOG_CAT

from core.analysis.steps import KeyAnalysis, BeatAnalysis

from core.fileManager import FileManager
from core.songData import SongData


class ISubscriber(ABC):
    #WRITE

    #type Notification = dict[str, object]
    
    @abstractmethod
    def update(data) -> None:
        pass

class AnalysisDirector():
    #WRITE

    def __init__(self) -> None:
        self._subscribers: list[ISubscriber] = []
        self._fm: FileManager = FileManager()
        self._key: KeyAnalysis = KeyAnalysis
        self._selected: SongData = None
        
    def subscribe(self, subscriber: ISubscriber) -> None:
        #WRITE
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)
        else:
            raise DuplicateElementException(f'Already subscribed')

    def _notify(self, msg) -> None:
        for subscriber in self._subscribers:
            subscriber.update(msg)

    def analyze(self) -> None:
        #WRITE
        
        self._notify({"step": "1", "msg": "Loading file..."})
        self._loadFile()
        self._notify({"step": "1", "msg": "Loaded file."})
        self._notify({"step": "2", "msg": "Analyzing key..."})
        self._keyAnalysis()
        self._notify({"step": "2", "msg": "Analized key."})
        self._notify({"step": "3", "msg": "Analyzing beat..."})
        self._beatAnalysis()
        self._notify({"step": "3", "msg": "Analized beat."})
        self._aio()
        self._notify({"finished": True}) 
    
# ----------------------------------------------------

    def _loadFile(self) -> None:
        # Step 1: Load file
        file = self._fm.getSelectedFile()
        
        if file is None:
            self._notify({"step": "1", "msg": "No file selected"})
            DCL.log(LOG_CAT.ERROR, f'No file selected!')
            raise NotFoundException(f'No file selected!')
        else:
            self._selected = file
            self._notify({"step": "1", "msg": f'Selected {file.title}'})
            DCL.log(LOG_CAT.INFO, f'Selected "{file.title}"')

    def _keyAnalysis(self) -> None:
        # Step 2: Key analysis
        
        key: str = KeyAnalysis.getKey(self._selected.file)
        self._notify({"step": "2", "msg": f'Got key: {key}'})
        DCL.log(LOG_CAT.INFO, f'Found key: {key}')
          
    def _beatAnalysis(self) -> None:
        # Step 3: Beat analysis
        
        bpm, confidence, beats = BeatAnalysis.getBeat_deeprhythm(self._selected.file)
        self._notify({"step": "3", "msg": f'Got bpm: {bpm}'})
        self._notify({"step": "3", "msg": f'Got beats: {beats}'})
        #DCL.log(CATEGORY.INFO, f'Beats:')
        #DCL.log(CATEGORY.INFO, ["{:.2f}".format(float(b)) for b in beats])
        DCL.log(LOG_CAT.INFO, f'Found bpm: {bpm} with {confidence*100//1}% confidence.')

    def _aio(self) -> None:
        DCL.log(LOG_CAT.INFO, f'AIO Results:')
        results = BeatAnalysis.getBeat_AIO(self._selected.path)
        self._fm.addAIOMetadata(results)