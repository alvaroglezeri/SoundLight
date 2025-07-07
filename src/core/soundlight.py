from pathlib import Path
import json
from typing import List

from .conf import Conf
from .exceptions import InvalidArgumentException, InvalidStateException, NothingSelectedException
from .fileManager import FileManager
from .analysis.analyzer import Analyzer, IAnalysisAlgorithm
from .generation.generator import Generator, IGenerationAlgorithm
from .export.exporter import Exporter, IExportAlgorithm
from .model.song import Song
from ..lib.helpers import get_OS


class SoundLight():
    """Soundlight interface. Provides an abstraction layer for the whole framework. Configures the options for the algorithms used.
    """

    def __init__(self, config_file_path: Path | str) -> None:
        """Creates a new instance of the SoundLight interface.

        Args:
            configFile_path (Path | str): Path to the TOML file containing the configuration options for the execution.
        """
        if not isinstance(config_file_path, (Path, str)):
            raise InvalidArgumentException(
                'Configuration file path not provided!')

        self._load_config(config_file_path)
        # Start FileManager
        FileManager()
        self._an = Analyzer()
        self._gen = Generator()
        self._ex = Exporter()

        self._patchLoaded = False
        self._analysisAlgorithmSet = False
        self._generationAlgorithmSet = False
        self._exportAlgorithmSet = False
        self._exportPathSet = False
        self._exportPath = None

        self._analysisComplete = False
        self._generationComplete = False
        self._exportComplete = False

    def __del__(self) -> None:
        # Resets the configuration loader
        Conf.reset()
        # Close FileManager
        FileManager.reset()

    def _load_config(self, configFile_path: Path | str) -> None:
        # First call to Conf, to se the export path
        Conf(Path(configFile_path))

    # --------------------------------------------------------------------------
    #                   File Managing
    # --------------------------------------------------------------------------

    def close_selected_song(self) -> None:
        """Closes the file for the selected song.
        If no song is selected, raises NothingSelectedException.
        """
        if FileManager().has_selected_song():
            FileManager().close_song(FileManager().get_selected_song())
        else: 
            raise NothingSelectedException()

    def add_song_from_path(self, path: str | Path) -> None:
        """Adds a song into the song list from a file.

        Args:
            path (str | Path): Path to the song file
        """
        FileManager().load_song(path)

    def select_song(self, i: int) -> None:
        """Selects a song from all songs loaded. If the argument is not valid, raises NotFoundException.

        Args:
            i (int): Index of the song in the list.
        """
        FileManager().select_song(i)

    def get_selected_song(self) -> Song:
        """Returns the currently selected song.

        Raises:
            NothingSelectedException: If no element is selected.

        Returns:
            Song: The currently selected song.
        """

        return FileManager().get_selected_song()

    def get_loaded_songs(self) -> List[Song]:
        """Gets the list of the currently loaded songs.

        Returns:
            List[Song]: List of loaded songs.
        """
        return FileManager().get_songs()

    # --------------------------------------------------------------------------
    #                     Configuration
    # --------------------------------------------------------------------------

    def set_patch_from_path(self, path: str | Path) -> None:
        """Loads a .json file containing the patch description, and configures the algorithms with it.
        Consult the documentation for format expectations.

        Raises:
            ValueError: If the path provided cannot be opened.
            Toml

        Args:
            path (str | Path): Path to the .json file containing the patch.
        """
        path = Path(path)
        try:
            with open(path, "r") as file:
                patch: dict = json.load(file)
        except OSError as e:
            raise ValueError(f'Error opening the patch file: {e}')

        self._patch: dict = patch
        self._patchLoaded = True

    def set_analysis_algorithm(self, algorithm: IAnalysisAlgorithm) -> None:
        """Configures the analysis algorithm for the program.

        Args:
            algorithm (IAnalysisAlgorithm): Analysis algorithm. Must implement the IAnalysisAlgorithm interface.
        """
        if algorithm is not None and isinstance(algorithm, IAnalysisAlgorithm):
            self._an.set_algorithm(algorithm)
            self._analysisAlgorithmSet = True
        else:
            raise InvalidArgumentException(
                'The algorithm supplied does not implement the IAnalysisAlgorithm interface!')

    def set_generation_algorithm(self, algorithm: IGenerationAlgorithm) -> None:
        """Configures the feature generation algorithm for the program.

        Args:
            algorithm (IGenerationAlgorithm): Generation algorithm. Must implement the IGenerationAlgorithm interface.
        """
        if algorithm is not None and isinstance(algorithm, IGenerationAlgorithm):
            self._gen.set_algorithm(algorithm)
            self._generationAlgorithmSet = True
        else:
            raise InvalidArgumentException(
                'The algorithm supplied does not implement the IGenerationAlgorithm interface!')

    def set_export_algorithm(self, algorithm: IExportAlgorithm) -> None:
        """Configures the export algorithm for the program.

        Args:
            exporter (IExportAlgorithm): Export algorithm. Must implement the IExportAlgorithm interface.
        """
        if algorithm is not None and isinstance(algorithm, IExportAlgorithm):
            self._ex.set_algorithm(algorithm)
            self._exportAlgorithmSet = True
        else:
            raise InvalidArgumentException(
                'The algorithm supplied does not implement the IExportAlgorithm interface!')

    def set_export_path(self, path: str | Path) -> None:
        """Configures the export path where the generated projects will be stored. Must point to a folder.

        Args:
            path (str | Path): Path for the folder where the projects will be stored.
        """
        if not isinstance(path, (Path, str)):
            raise InvalidArgumentException('The path provided is invalid!')

        path = Path(path)
        if not path.is_dir():
            raise InvalidArgumentException('The path is not a directory!')

        if path.is_dir():
            self._exportPath = path
            self._exportPathSet = True

    # --------------------------------------------------------------------------
    #                           Running
    # --------------------------------------------------------------------------

    def run(self) -> None:
        """Analyzes the selected song, generates features and exports the results for the selected song.

        Raises:
            NothingSelectedException: If there is no selected song.
            InvalidStateException: If either the patch, analysis algorithm, generation algorithm or export algorithm are not set.
        """
        if not self._patchLoaded or self._patch is None:
            raise InvalidStateException('The patch has not been loaded!')
        if not self._analysisAlgorithmSet:
            raise InvalidStateException(
                'The analysis algorithm has not been loaded!')
        if not self._generationAlgorithmSet:
            raise InvalidStateException(
                'The generation algorithm has not been loaded!')
        if not self._exportAlgorithmSet:
            raise InvalidStateException(
                'The export algorithm has not been loaded!')
        if not self._exportPathSet:
            raise InvalidStateException('The export path has not been loaded!')

        song = FileManager().get_selected_song()
        self._an.analyze(song)
        self._gen.set_patch(self._patch)
        self._gen.generate(song)
        self._ex.set_song(song)
        self._ex.export(self._exportPath)

    # --------------------------------------------------------------------------
    #                       Utils
    # --------------------------------------------------------------------------

    def _print_song_data(self) -> str:
        """Returns the selected song's data.

        Returns:
            str: String containing the data for the song.
        Raises:
            NothingSelectedException: if no song is selected.
        """
        return FileManager().get_selected_song().__repr__()

    def _save_song_data(self) -> None:
        """Saves the selected song's data.
        Takes the path from the config file.

        Raises:
            NothingSelectedException: if no song is selected.
            ValueError: if the path is invalid.
        """
        def default(obj):
            return str(obj)

        path = None
        try:
            folder_path = self._exportPath
            file_name = Path(FileManager().get_selected_song()['path']).stem
            path = Path(f"{folder_path}/{file_name}.json")

            with open(path, 'w') as f:
                json.dump(FileManager().get_selected_song()._struct,
                          f, default=default)
        except NothingSelectedException as e:
            raise e
        except OSError as e:
            raise ValueError(f'Provided an invalid path: {path}')


    def _gpu_available(self) -> bool:
        """Checks if a GPU is available in the system.

        Returns:
            bool: True if a GPU is available, False otherwise.
        """
        return self._an._gpu_available()