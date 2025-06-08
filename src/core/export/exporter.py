from abc import ABC, abstractmethod
import builtins
import io
from io import BytesIO
from pathlib import Path
import typing
from typing import List
from core.model.song import Song
from core.logger import Logger, LOG_CAT


class IExportAlgorithm(ABC):
    """Interface that all export algorithms must have.
    """

    @property
    @abstractmethod
    def file_extension(self) -> str:
        """The file extension for the project file generated.

        Returns:
            str: File extension, without preceding dot.
        """
        pass

    @abstractmethod
    def export(self, song: Song) -> None:
        """Starts the export.

        Args:
            song (Song): Dictionary with the data required for the export. Could be modified by this method.
        """
        pass

    @abstractmethod
    def get(self) -> List[str] | BytesIO:
        """Returns the result of the export process.

        Returns:
            List[str] | BytesIO: Either a list of strings, or a in-memory object, depending on the specific algorithm.
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
        self._song: Song | None = None
        self._exportAlgorithm: IExportAlgorithm | None = None

    def set_algorithm(self, exportAlgorithm: IExportAlgorithm) -> None:
        """Sets the algorithm to use. 

        Args:
            exportAlgorithm (IExportAlgorithm): Algorithm to use.
        """
        if exportAlgorithm is not None:
            self._exportAlgorithm = exportAlgorithm

    def set_song(self, song: Song) -> None:
        """Sets the song for which to generate. The features must be already generated.

        Args:
            song (Song): Song to use.
        """
        if song is not None:
            self._song = song

    def export(self, path: Path):
        """Runs te export process

        Args:
            path (Path): _description_

        Raises:
            ValueError: If either the song or export algorithm are None, or the output format of the algorithm is invalid.
        """

        if self._song == None:
            Logger.log(LOG_CAT.ERROR, 'Song is not set!')
            raise ValueError('Song is not set!')
        elif self._exportAlgorithm == None:
            Logger.log(LOG_CAT.ERROR, 'Exporter is not set!')
            raise ValueError('Exporter is not set!')

        try:
            # Build the export path
            exportPath: Path = Path(
                f"{path.absolute().joinpath(self._song['title'])}.{self._exportAlgorithm.file_extension}")
            Logger.log(LOG_CAT.INFO, f'Output file: {exportPath}')

            # Run the export process
            self._exportAlgorithm.export(self._song)

            # Save results
            with open(exportPath, 'wb') as output:
                ret = self._exportAlgorithm.get()

                if isinstance(ret, List):
                    for line in ret:
                        output.write(f'{line}\n'.encode())
                elif isinstance(ret, BytesIO):
                    output.write(ret.read())
                # elif isinstance(ret, bytes):
                #     output.write(ret)
                else:
                    raise ValueError(f'Invalid export format: {type(ret)}')

        except Exception as e:
            Logger.log(LOG_CAT.ERROR, 'An error ocurred during export:')
            raise e

    # --------------------
