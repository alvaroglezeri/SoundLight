from io import BufferedReader
from math import ceil
import json

# from core.model.features import IFeature
from core.logger import Logger, LOG_CAT


class Song():
    # WRITE

    # ----- CLASS METHODS -----
    def __init__(self, file: BufferedReader) -> None:
        # Building internal structure of the song as a dict
        self._struct: dict = {
            "song": {
                "file": file,
                "path": file.name,
                "metadata": {}
            },
            "patch": {},
            "features": []
        }

    def __eq__(self, other) -> bool:
        if not isinstance(other, Song):
            return False
        else:
            return self.__hash__() == other.__hash__()

    def __hash__(self) -> int:
        return hash(self['song']['path'])

    def __repr__(self) -> str:
        return json.dumps(self._struct)

    def __str__(self) -> str:
        def secToMin(seconds) -> str:
            min = int(seconds // 60)
            sec = ceil(seconds - min*60)
            return f'{min}:{sec}'

        try:
            title: str = self['song']['tinytag']['title']
            author: str = self['song']['tinytag']['artist'] if self['song'][
                'tinytag']['artist'] != None else '(No author)'
            length: str = secToMin(self['song']['tinytag.duration'])
            return f'{title} - {author} ({length})'
        except Exception as e:
            Logger.log(LOG_CAT.ERROR, e)
            return f"Error getting properties for {self['song']['path']}"

    def __getitem__(self, key: str):
        return self._struct[key]

    """
    # ----- COMMON PROPERTIES -----

    @property
    def title(self) -> str:

        # Returns the title of the song.

        try:
            return self['song']['tinytag']['title'][0] if self['song']['tinytag']['title'][0] != None else '(No title)'
        except:
            return '(No title)'

    @property
    def file(self) -> BufferedReader:

        # Returns the file itself

        Returns
        -------
        BufferedReader
            object with the file loaded

        return self['song']['file']

    @property
    def path(self) -> str:

        # Returns the path to the file in the filesystem

        return self['song']['path']

  # ----- FILE METADATA -----

    @property
    def metadata(self) -> dict:
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
    """
