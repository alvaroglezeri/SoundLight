from genericpath import exists
from io import BufferedReader
from typing import List
from deprecated import deprecated
from pathlib import Path

from tinytag import tinytag, TinyTag, TinyTagException
import ffmpeg

from .logger import Logger, LOG_CAT
from .exceptions import *
from .model.song import Song


class FileManager():
    """
    Manages the files that the program has loaded.
    """
    _FORMAT: tuple = ('wav', tinytag._Wave)

    # --------------------------------------------------------------------------
    # CLASS METHODS
    # -------------------------------------------------------------------------------
    def __new__(cls):
        """
        Singleton implementation. The config is set on the first call.
        """
        if not hasattr(cls, 'instance'):
            cls.instance = object.__new__(cls)
            cls.instance.__setup__()
        return cls.instance

    def __setup__(self) -> None:
        """Sets up the internal song list and selected song.
        """
        self._songs: List[Song] = list()
        self._selected: Song | None = None

    def __init__(self) -> None:
        """Provides an access to the current FileManager, regardless of context.
        Implemented as a singleton. The first call must provide the _config_ param.

        Args:
            config (dict): Employed by the first call to configure the FileManager.
        """
        # Empty __init__, so to not rebuild the singleton
        return

    def __del__(self) -> None:
        """Automatically closes the loaded files.
        """
        try:
            song: Song
            for song in self._songs:
                try:
                    Logger.log(LOG_CAT.INFO, f"Closing '{song['path']}'...")
                    song['file'].close()
                except:
                    pass
        except:
            pass

    @classmethod
    def reset(cls) -> None:
        if hasattr(cls, 'instance'):
            del cls.instance

    # --------------------------------------------------------------------------
    # FILE MANAGING
    # -------------------------------------------------------------------------------

    def get_songs(self) -> List[Song]:
        """Returns all loaded songs.
        """
        return self._songs

    def close_song(self, song: Song) -> None:
        """Removes a song from the loaded songs, closing its handle.

        Args:
            song (Song): Song to remove.

        Raises:
            NotFoundException: If the song is not found.
        """
        if song not in self._songs:
            raise NotFoundException()
        else:
            try:
                song['file'].close()
                self._songs.remove(song)
            except Exception as e:
                Logger.log(LOG_CAT.ERROR, f'Error closing song: {e}')
                pass

    def load_song(self, path: str | Path) -> None:
        """Loads a song into the file manager.

        Args:
            path (str | Path): Path to the song file.

        Raises:
            InvalidFileException: If the format provided is not supported.
            DuplicateElementException: If the file is already opened.
        """
        Logger.log(LOG_CAT.INFO, f'Loading "{path}"...')

        # FileManager manages the life cycle of the files.
        try:
            if not Path(path).exists() or not Path(path).is_file():
                raise FileNotFoundError('This file could not be found!')
            # Checks whether the file has a valid format
            if not TinyTag.is_supported(path):
                validFormats: str = ' '.join(
                    [f for f in TinyTag.SUPPORTED_FILE_EXTENSIONS])
                raise InvalidFileException(
                    f'This file is not supported! Valid file formats are: \n\t{validFormats}')

            # Checks the codec of the file, and converts to .wav if needed
            file: BufferedReader = open(path, "rb")

            # We obtain the metadata for the file now, because it will be lost on file conversion
            tags: TinyTag = TinyTag.get(file_obj=file)

            # Checking file codec and performing conversion if needed
            file, path = self._check_codec(file)

            # Building Song object and adding tags
            song: Song = Song(file)
            self._add_tags(song, tags)

            # Adding the file to the list
            song: Song
            if song not in self._songs:
                self._songs.append(song)
                Logger.log(LOG_CAT.SUCCESS, f"Loaded '{song['title']}'.")
            else:
                raise DuplicateElementException(
                    f'This file is already loaded.')

        except DuplicateElementException as dee:
            raise dee

        except TinyTagException as tte:
            # FIXME: What if the file is not audio?
            raise InvalidFileException(f'Invalid file because: "{tte}"')

        except InvalidFileException as ife:
            raise ife

        except Exception as e:
            Logger.log(LOG_CAT.ERROR, e)
            raise e

    def _add_tags(self, song: Song, tags: TinyTag) -> None:
        """Adds the tags gathered from TinyTag into the song's internal structure.
        """

        tinytagData = tags.as_dict()

        if 'title' in tinytagData.keys():
            if type(tinytagData['title']) is list:
                song['title'] = tinytagData['title'][0]
            else:
                song['title'] = tinytagData['title']
        else:
            # Default song name is the filename
            song['title'] = str(Path(song['path']).name)

        # Everything else is stored in its own key.
        song['metadata']['tinytag'] = tinytagData

    def _check_codec(self, file: BufferedReader) -> tuple[BufferedReader, str]:
        """Checks the codec of the file and performs a conversion if needed.

        Args:
            file (BufferedReader): file to check codec

        Returns:
            tuple[BufferedReader, str]: returns the final file and its path
        """

        # Obtaining file codec from the actual class parsed
        codec: type[TinyTag] = TinyTag.get(file_obj=file).__class__
        Logger.log(LOG_CAT.INFO, f'Detected codec: {codec.__qualname__}')

        # If the codec is not .wav, we convert the file
        if codec != self._FORMAT[1]:

            newPath = self._convert_file(file.name)
            Logger.log(LOG_CAT.SUCCESS, f'Converted file to {self._FORMAT[0]}')
            Logger.log(LOG_CAT.INFO, f'New path: "{newPath}"')
            file.close()
            newFile: BufferedReader = open(newPath, "rb")
            return newFile, newPath
        else:
            return file, file.name

    def _convert_file(self, path: str) -> str:
        """Converts the file to .wav with ffmpeg

        Args:
            path (str): path of the original file

        Returns:
            str: path to the new file
        """
        Logger.log(LOG_CAT.WARN, f'Converting file to .{self._FORMAT[0]}...')

        newPath = f'{Path(path).parents[0]}/{Path(path).stem}.{self._FORMAT[0]}'
        ffmpeg.input(path, v="quiet").output(newPath).overwrite_output().run()

        Logger.log(LOG_CAT.SUCCESS, f'Successfully converted to "{newPath}"')

        # DOCUMENT: A lot of ffmpeg options were tried to solve 'Format not recognized' errors, until the seek(0) was discovered.

        return newPath

    # --------------------------------------------------------------------------
    # SONG SELECTION
    # -------------------------------------------------------------------------------

    def has_selected_song(self) -> bool:
        """Returns ``True`` if the FileManager has a song selected, ``False`` otherwise.
        """
        return self._selected is not None

    def select_song(self, n: int) -> None:
        """Selects a song by index of the list of loaded songs.

        Args:
            n (int): Index of the song in the list.

        Raises:
            ArgumentException: If the argument is invalid.
            NotFoundException: If the song cannot be loaded.
        """

        if not isinstance(n, int):
            raise ArgumentException('The argument is invalid!')
        try:
            self._selected = self._songs[n]
            if self._selected:
                Logger.log(LOG_CAT.SUCCESS,
                           f"Selected '{self._selected['path']}'")
                pass
            else:
                raise NotFoundException()
        except Exception as e:
            Logger.log(LOG_CAT.ERROR, e)
            raise NotFoundException()

    def get_selected_song(self) -> Song:
        """Returns the selected song.

        Raises:
            NothingSelectedException: If no song is selected.
        """
        if self._selected is not None:
            return self._selected
        else:
            raise NothingSelectedException(msg="No file selected!")
