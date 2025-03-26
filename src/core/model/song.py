from io import BufferedReader
from math import ceil

from core.model.features import IFeature
from core.logger import Logger, LOG_CAT


class Song():
    # WRITE

    # ----- CLASS METHODS -----
    def __init__(self, file: BufferedReader) -> None:
        self._file = file
        self._path = file.name
        self._metadata = {}
        self._features = []

    def __eq__(self, other):
        if not isinstance(other, Song):
            return False
        else:
            return self.__hash__() == other.__hash__()

    def __hash__(self):
        return hash(self.path)

    def __repr__(self):

        def secToMin(seconds) -> str:
            min = int(seconds // 60)
            sec = ceil(seconds - min*60)
            return f'{min}:{sec}'

        try:
            title: str = self.title
            author: str = self._metadata['tinytag']['artist'] if self._metadata[
                'tinytag']['artist'] != None else '(No author)'
            length: str = secToMin(self._metadata['tinytag.duration'])
            return f'{title} - {author} ({length})'
        except Exception as e:
            Logger.log(LOG_CAT.ERROR, e)
            return f'Error getting properties for {self.path}'

    def __str__(self):
        return self.__repr__()

    # ----- COMMON PROPERTIES -----

    @property
    def title(self) -> str:
        """
        Returns the title of the song.
        """
        try:
            return self._metadata['tinytag']['title'][0] if self._metadata['tinytag']['title'][0] != None else '(No title)'
        except:
            return '(No title)'

    @property
    def file(self) -> BufferedReader:
        """
        Returns the file itself

        Returns
        -------
        BufferedReader
            object with the file loaded
        """
        return self._file

    @property
    def path(self) -> str:
        """
        Returns the path to the file in the filesystem
        """
        return self._path

    # ----- FILE METADATA -----

    @property
    def metadata(self) -> object:
        return self._metadata

    def addMetadata(self, key: str, value) -> None:
        self._metadata[key] = value

    # ----- GENERATED FEATURES -----
    @property
    def features(self) -> list[IFeature]:
        return self._features

    def addFeatures(self, features: IFeature | list[IFeature]) -> None:
        if isinstance(features, IFeature):
            self._features.append(features)
        else:
            for f in features:
                self._features.append(f)
