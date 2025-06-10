from numpy import ndarray
from io import BufferedReader
from math import ceil
import json

from src.core.exceptions import InvalidArgumentException

from ..logger import Logger, LOG_CAT
from ..model.features import IFeature


class Song():
    """Song object that contains all info of the song under analysis:
    - File metadata.
    - Analysis results.
    - Generated features.
    """

    # --------------------------------------------------------------------------
    # CLASS METHODS
    # -------------------------------------------------------------------------------
    def __init__(self, file: BufferedReader) -> None:
        # Building internal structure of the song as a dict
        if file is None or not isinstance(file, BufferedReader) or file.closed:
            raise InvalidArgumentException(
                'The provided file descriptor is invalid!')

        self._struct: dict = {
            "file": file,
            "path": file.name,
            # Other properties...

            "metadata": {},
            "patch": {},
            "features": []
        }

    def __eq__(self, other) -> bool:
        if not isinstance(other, Song):
            return False
        else:
            return self.__hash__() == other.__hash__()

    def __hash__(self) -> int:
        return hash(self['path'])

    def __repr__(self) -> str:
        return json.dumps(self._struct, default=self._song_repr_helper)

    def __str__(self) -> str:
        def secToMin(seconds) -> str:
            min = int(seconds // 60)
            sec = ceil(seconds - min*60)
            return f'{min}:{sec}'

        try:
            title: str = self['tinytag']['title']
            author: str = self['tinytag']['artist'] if self[
                'tinytag']['artist'] != None else '(No author)'
            length: str = secToMin(self['tinytag.duration'])
            return f'{title} - {author} ({length})'
        except Exception as e:
            Logger.log(LOG_CAT.ERROR, e)
            return f"Error getting properties for {self['path']}"

    # TODO: Replace calls to __getitem__ (song['key']) with this method, as it allows providing a default
    def get(self, key: str):
        return self._struct.get(key)

    def __getitem__(self, key: str):
        return self._struct[key]

    def __setitem__(self, key, value) -> None:
        self._struct[key] = value

    def _song_repr_helper(self, object) -> str:
        if isinstance(object, ndarray):
            return str(list(object))

        if isinstance(object, BufferedReader):
            return object.name

        if isinstance(object, IFeature):
            return json.dumps(object.serialize())
        else:
            return str(object)
