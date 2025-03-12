from io import BufferedReader
from deprecated import deprecated
from pathlib import Path

from tinytag import tinytag, TinyTag, TinyTagException
import allin1
import ffmpeg

from core.logger import Logger, LOG_CAT
from core.exceptions import *
from core.model.song import Song
from core.model.features import IFeature


class FileManager():
    """
    Manages the files that the app has loaded
    """
    _FORMAT: tuple[str, TinyTag] = ('wav', tinytag._Wave)

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
        self._songs: list[Song] = list()
        self._selected: Song = None
        self._convert: bool = True

    def __init__(self) -> None:
        # Empty __init__, so to not rebuild the singleton
        return

    def __del__(self) -> None:
        try:
            file: Song
            for file in self._songs:
                try:
                    Logger.log(LOG_CAT.INFO, f'Closing "{file.path}"...')
                    file._file.close()
                except:
                    pass
        except:
            pass

    # ----- FILE MANAGING -----

    def getLoadedFiles(self) -> list[Song]:
        return list(self._songs)

    @deprecated
    def getAllFilesSummary(self) -> list[str]:
        """
        Returns a summary of all files loaded 
        """
        summary = []

        file: Song
        for file in self._songs:
            summary.append(print(file))
        return summary

    def setConvert(self, mode: bool) -> None:
        Logger.log(LOG_CAT.INFO,
                   f'Filetype conversion is {"enabled" if mode else "disabled"}')
        self._convert = mode

    @deprecated
    def setConversionFormat(self, formatName: str) -> None:
        """
        Sets the conversion format. Must be one of SUPPORTED_FORMATS, else is set to the default.
        """
        if formatName in _SUPPORTED_FORMATS:
            self._conversionFormat = _SUPPORTED_FORMATS[formatName]
        else:
            self._conversionFormat = _SUPPORTED_FORMATS[_DEFAULT_FORMAT]
        Logger.log(
            LOG_CAT.INFO, f'Filetype Conversion format set to {self._conversionFormat[1].__qualname__}')

    def loadFileFromPath(self, path: str) -> None:
        """
        WRITE

        Loads the file
        """
        Logger.log(LOG_CAT.INFO, f'Loading "{path}"...')

        # FileManager manages the life cycle of the files.
        try:
            # Checks whether the file has a valid format
            if not TinyTag.is_supported(path):
                validFormats: str = ' '.join(
                    [f for f in TinyTag.SUPPORTED_FILE_EXTENSIONS])
                raise InvalidFileException(
                    f'This file is not supported! Valid file formats are: {validFormats}')

            # Checks the codec of the file, and converts to .wav if needed
            file: BufferedReader = open(path, "rb")

            # We obtain the metadata for the file now, because it is lost on file conversion
            tags: TinyTag = TinyTag.get(file_obj=file)

            # Checking file codec and performing conversion if needed
            file, path = self.checkCodec(file)

            # Building Song object and adding tags
            song: Song = Song(file)
            self._addTags(song, tags)

            # Adding the file to the list
            song: Song
            if song not in self._songs:
                self._songs.append(song)
                Logger.log(LOG_CAT.SUCCESS, f'Loaded "{song.title}".')
            else:
                Logger.log(LOG_CAT.ERROR,
                           f'File "{song.title}" already exists.')
                raise DuplicateElementException(
                    f'This file is already loaded.')

        except DuplicateElementException as dee:
            Logger.log(LOG_CAT.ERROR, dee)
            raise dee

        except TinyTagException as tte:
            # FIXME: What if the file is not audio?
            Logger.log(LOG_CAT.ERROR, f'TinyTag error: {tte}')
            raise InvalidFileException(f'Invalid file because: "{tte}"')

        except InvalidFileException as ife:
            Logger.log(LOG_CAT.ERROR, f'This format is not supported!')
            raise ife

        except Exception as e:
            Logger.log(LOG_CAT.ERROR, e)
            raise e

    def _addTags(self, song: Song, tags: TinyTag) -> None:
        """Adds the tags gathered to the song
        WRITE

        Args:
            song (Song): _description_
            tags (TinyTag): _description_
        """
        for key, value in tags.as_dict().items():
            song.addMetadata(f'tinytag.{key}', value)

    def checkCodec(self, file: BufferedReader) -> tuple[BufferedReader, str]:
        """Checks the codec of the file and performs a conversion if needed.

        Args:
            file (BufferedReader): _description_

        Returns:
            tuple[BufferedReader, str]: returns the final file and its path
        """

        # Obtaining file codec from the actual class parsed
        codec: TinyTag = TinyTag.get(file_obj=file).__class__
        Logger.log(
            LOG_CAT.INFO, f'Detected codec: {codec.__qualname__}')

        # If the codec is not .wav, we convert the file
        if codec != self._FORMAT[1] and self._convert:

            newPath = self._convertFile(file.name)
            Logger.log(LOG_CAT.SUCCESS,
                       f'Converted file to {self._FORMAT[0]}')
            Logger.log(LOG_CAT.INFO, f'New path: "{newPath}"')
            file.close()
            newFile: BufferedReader = open(newPath, "rb")
            return newFile, newPath
        else:
            return file, file.name

    def _convertFile(self, path: str) -> str:
        """Converts the file to .wav with ffmpeg

        Args:
            path (str): path of the original file

        Returns:
            str: path to the new file
        """
        Logger.log(
            LOG_CAT.WARN, f'Converting file to .{self._FORMAT[0]}...')

        newPath = f'{Path(path).parents[0]}/{Path(path).stem}.{self._FORMAT[0]}'
        ffmpeg.input(path, v="quiet").output(newPath).overwrite_output().run()

        Logger.log(LOG_CAT.SUCCESS, f'Successfully converted to "{newPath}"')

        # DOCUMENT: A lot of ffmpeg options were tried to solve 'Format not recognized' errors, until the seek(0) was discovered.

        return newPath

    # ----- FILE SELECTION -----

    def hasSelectedFile(self) -> bool:
        return self._selected is not None

    def selectFile(self, n) -> None:
        try:
            self._selected = self._songs[n]
            Logger.log(LOG_CAT.SUCCESS, f'Selected "{self._selected.path}"')
        except Exception as e:
            Logger.log(LOG_CAT.ERROR, e)
            raise NotFoundException()

    def getSelectedFile(self) -> Song:
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
