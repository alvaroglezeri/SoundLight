from abc import ABC, abstractmethod
from pathlib import Path
from core.model.song import Song
from core.logger import Logger, LOG_CAT


class ProjectCreator(ABC):

    @property
    @abstractmethod
    def fileExtension(self) -> str:
        pass

    @abstractmethod
    def export(self, song: Song) -> None:
        """Starts the export.

        Args:
            song (Song): Dictionary with the data required for the export. Could be modified by this method.
        """
        pass

    @abstractmethod
    def get(self) -> list[str] | None:
        pass

    pass


class Exporter():
    """Acts as an interface for the whole export phase. 
    WRITE

    Raises:
        e: _description_
    """

    def __init__(self) -> None:
        """
        WRITE
        """
        self._song: Song | None = None
        self._pc: ProjectCreator | None = None

    def set_projectCreator(self, projectCreator: ProjectCreator) -> None:
        self._pc = projectCreator

    def set_song(self, song: Song) -> None:
        self._song = song

    def export(self, path: Path):
        """
        WRITE
        """

        if self._song == None:
            Logger.log(LOG_CAT.ERROR, 'Song is not set!')
            raise ValueError('Song is not set!')
        elif self._pc == None:
            Logger.log(LOG_CAT.ERROR, 'Project Creator is not set!')
            raise ValueError('Project Creator is not set!')

        try:
            # Build the export path
            exportPath: Path = Path(
                f'{path.absolute().joinpath(self._song['song']['title'])}.{self._pc.fileExtension}')
            Logger.log(LOG_CAT.INFO, f'Output file: {exportPath}')

            # Run the export process
            self._pc.export(self._song)

            # Save results
            with open(exportPath, 'wt') as output:
                for line in self._pc.get():  # type: ignore (export finished as of now)
                    output.write(f'{line}\n')

        except Exception as e:
            Logger.log(LOG_CAT.ERROR, 'An error ocurred during export:')
            raise e

    # --------------------
