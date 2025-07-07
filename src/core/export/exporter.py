from abc import ABC, abstractmethod
from io import BytesIO
from pathlib import Path
from typing import List

from src.core.exceptions import InvalidArgumentException, InvalidStateException

from ..model.song import Song
from ..logger import Logger, LOG_CAT


class IExportAlgorithm(ABC):
    """Interface that all export algorithms must have.
    """

    @abstractmethod
    def set_song(self, song: Song) -> None:
        """Sets the song to export for. Must be set before exporting.
        """
        pass

    @abstractmethod
    def get_keystring(self) -> str:
        """Returns the key string to be used when searching for the config values of this algorithm.

        Returns:
            str: Key string
        """
        pass

    @property
    @abstractmethod
    def file_extension(self) -> str:
        """The file extension for the project file generated.

        Returns:
            str: File extension, without preceding dot.
        """
        pass

    @abstractmethod
    def export(self) -> List[str] | BytesIO:
        """Starts the export.

        Returns:
            List[str] | BytesIO: The exported data. 
            If the export is a text file, it should return a list of strings, each representing a line. 
            If the export is a binary file, it should return a BytesIO object containing the binary data.

        """
        pass

    pass


class Exporter():
    """
    Manages the export process. Requires an export algorithm.
    """

    def __init__(self) -> None:
        """Constructs the exporter object.        
        """
        self._song = None
        self._exportAlgorithm = None

    def set_algorithm(self, algorithm: IExportAlgorithm) -> None:
        """Sets the algorithm to use. 

        Args:
            algorithm (IExportAlgorithm): Algorithm to use.
        """
        if not isinstance(algorithm, IExportAlgorithm):
            raise InvalidArgumentException(
                'The algorithm provided is invalid!')
        self._exportAlgorithm = algorithm

    def set_song(self, song: Song) -> None:
        """Sets the song for which to generate. The features must be already generated.

        Args:
            song (Song): Song to use.
        """
        if not isinstance(song, Song):
            raise InvalidArgumentException('The song provided is invalid!')
        self._song = song

    def export(self, path: Path):
        """Runs te export process. Saves the result file in the provided path.

        Args:
            path (Path): _description_

        Raises:
            ValueError: If either the song or export algorithm are None, or the output format of the algorithm is invalid.
        """

        if not isinstance(path, Path):
            raise InvalidArgumentException('The path provided is invalid!')

        if not self._song:
            raise InvalidStateException('The song has not been set!')
        if not self._exportAlgorithm:
            raise InvalidStateException(
                'The export algorithm has not been set!')

        try:
            # Build the export path
            exportPath: Path = Path(
                f"{path.absolute().joinpath(self._song['title'])}.{self._exportAlgorithm.file_extension}")
            Logger.log(LOG_CAT.INFO, f'Output file: {exportPath}')

            # Run the export process
            self._exportAlgorithm.set_song(self._song)
            ret = self._exportAlgorithm.export()

            # Save results
            with open(exportPath, 'wb') as output:
                if isinstance(ret, List):
                    for line in ret:
                        output.write(f'{line}\n'.encode())
                elif isinstance(ret, BytesIO):
                    output.write(ret.read())
                else:
                    raise ValueError(f'Invalid export format: {type(ret)}')

        except Exception as e:
            Logger.log(LOG_CAT.ERROR, 'An error ocurred during export:')
            raise e

    # --------------------------------------------------------------------------
