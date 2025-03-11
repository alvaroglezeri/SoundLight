from tinytag import tinytag, TinyTag, TinyTagException
from pathlib import Path
import allin1
import ffmpeg
from deprecated import deprecated

from core.logger import DCL, LOG_CAT
from core.exceptions import *
from core.songData import SongData
from core.generation.features import IFeature


_SUPPORTED_FORMATS: dict[str, tuple[str, TinyTag]] = {
    'wav': ('wav', tinytag._Wave)
}

_DEFAULT_FORMAT: str = 'wav'


class FileManager():
    """
    Manages the files that the app has loaded
    """
    # ----- CLASS METHODS -----
    def __new__(cls):
        """
        Singleton implementation
        """
        if not hasattr(cls, 'instance'):
            cls.instance = object.__new__(cls)
            cls.instance.__setup__()
        return cls.instance

    def __setup__(self) -> None:
        # WRITE
        self._files: list[SongData] = list()
        self._selected: SongData = None
        self._convert: bool = True
        # Tuple containing extension and codec class
        self._conversionFormat: tuple[str, TinyTag] = _SUPPORTED_FORMATS["wav"]

    def __init__(self) -> None:
        # Empty __init__, so to not rebuild the singleton
        return

    def __del__(self) -> None:
        try:
            for file in self._files:
                DCL.log(LOG_CAT.INFO, f'Closing "{file.path}"...')
                # f: BufferedReader
                file._file.close()
        except:
            pass

    # ----- FILE MANAGING -----

    def getLoadedFiles(self) -> list[SongData]:
        return list(self._files)

    def getAllFilesSummary(self) -> list[str]:
        """
        Returns a summary of all files loaded 
        """
        summary = []

        file: SongData
        for file in self._files:
            summary.append(print(file))
        return summary

    def setConvert(self, mode: bool) -> None:
        DCL.log(LOG_CAT.INFO,
                f'Filetype conversion is {"enabled" if mode else "disabled"}')
        self._convert = mode

    def setConversionFormat(self, formatName: str) -> None:
        """
        Sets the conversion format. Must be one of SUPPORTED_FORMATS, else is set to the default.
        """
        if formatName in _SUPPORTED_FORMATS:
            self._conversionFormat = _SUPPORTED_FORMATS[formatName]
        else:
            self._conversionFormat = _SUPPORTED_FORMATS[_DEFAULT_FORMAT]
        DCL.log(
            LOG_CAT.INFO, f'Filetype Conversion format set to {self._conversionFormat[1].__qualname__}')

    def loadFileFromPath(self, path: str) -> None:
        """
        WRITE

        Loads the file and its metadata with tinytag and magic.
        """

        DCL.log(LOG_CAT.INFO, f'Loading "{path}"...')
        try:
            # FileManager manages the life cycle of the files.
            file = open(path, "rb")  # with open(path, "rb") as file:

            songTags: TinyTag = TinyTag.get(file_obj=file)
            # Obtaining file codec from the actual class parsed
            songTags.codec = {
                "name": songTags.__class__.__qualname__, "class": songTags.__class__}

            # Converting file format to .wav
            DCL.log(LOG_CAT.INFO, f'Detected codec: {songTags.codec["name"]}')
            if songTags.codec["class"] != self._conversionFormat[1] and self._convert:
                newPath = self._convertFile(path)
                DCL.log(LOG_CAT.INFO, "FileManager.loadFileFromPath",
                        f'Converted file to {self._conversionFormat[1].__qualname__}')
                raise CodecConversionExeption()

            # Building SongData object
            songData: SongData = SongData(file, path)
            for key, value in songTags.__dict__.items():
                songData.addMetadata(f'tinytag.{key}', value)

            if songData not in self._files:
                self._files.append(songData)
                DCL.log(LOG_CAT.SUCCESS, f'Loaded "{path}".')
            else:
                DCL.log(LOG_CAT.ERROR, f'File "{path}" already exists.')
                raise DuplicateElementException(
                    f'This file is already loaded.')
        except CodecConversionExeption:
            # If the codec is invalid, we drop the current file and open the new, converted file
            file.close()
            DCL.log(LOG_CAT.WARN, f'Reloading file...')
            self.loadFileFromPath(newPath)
        except DuplicateElementException as dee:
            DCL.log(LOG_CAT.ERROR, dee)
            raise dee
        except TinyTagException as tte:
            # FIXME: What if the file is not audio?
            DCL.log(LOG_CAT.ERROR, f'TinyTag error: {tte}')
            raise InvalidFileException(f'Invalid file because: "{tte}"')
        except Exception as e:
            DCL.log(LOG_CAT.ERROR, e)
            raise e

    def _convertFile(self, path) -> str:
        # WRITE
        DCL.log(
            LOG_CAT.WARN, f'Converting file to {self._conversionFormat[1].__qualname__}...')

        # print(Path(path).anchor)
        # print(Path(path).parents[0])

        newPath = f'{Path(path).parents[0]}/{Path(path).stem}.{self._conversionFormat[0]}'
        # DOCUMENT: A lot of ffmpeg options were tried to solve 'Format not recognized' errors, until the seek(0) was discovered.
        ffmpeg.input(path, v="quiet").output(newPath).overwrite_output().run()

        return newPath

    def hasSelectedFile(self) -> bool:
        return self._selected is not None

    def selectFile(self, n) -> None:
        try:
            self._selected = self._files[n]
            DCL.log(LOG_CAT.SUCCESS, f'Selected "{self._selected.path}"')
        except Exception as e:
            DCL.log(LOG_CAT.ERROR, e)
            raise NotFoundException()

    def getSelectedFile(self) -> SongData:
        # WRITE
        if self._selected is not None:
            return self._selected
        else:
            raise NothingSelectedException(msg="No file selected!")

    # ----- METADATA -----
    # FIXME: Change responsabilities of class to avoid these methods -> use getSelectedFile
    @deprecated
    def addAIOMetadata(self, properties: allin1.typings.AnalysisResult):
        if not self.hasSelectedFile():
            raise NothingSelectedException()
        else:
            for key, value in properties.__dict__.items():
                self._selected.addMetadata(f'aio.{key}', value)

    @deprecated
    def getMetadata(self) -> dict:
        """
        Loads metadata for the current song
        """
        if not self.hasSelectedFile():
            raise NothingSelectedException()
        else:
            return self._selected.metadata

    # ----- FEATURES -----
    # FIXME: Change responsabilities of class to avoid these methods -> use getSelectedFile
    @deprecated
    def addFeatures(self, features: list[IFeature]) -> None:
        """
        WRITE
        """
        if not self.hasSelectedFile():
            raise NothingSelectedException()
        else:
            self._selected.addFeatures(features)
        pass

    @deprecated
    def getFeatures(self) -> list[IFeature]:
        if not self.hasSelectedFile():
            raise NothingSelectedException()
        else:
            return self._selected.features
