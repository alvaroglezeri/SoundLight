from pathlib import Path
import json
from typing import List

from .conf import Conf
from .exceptions import NothingSelectedException
from .fileManager import FileManager
from .analysis.analyzer import Analyzer, IAnalysisAlgorithm
from .generation.generator import Generator, IGenerationAlgorithm
from .export.exporter import Exporter, IExportAlgorithm
from .model.song import Song
from ..lib.helpers import get_OS


class SoundLight():
    """Soundlight interface. Provides an abstraction layer for the whole framework. Configures the options for the algorithms used.
    """

    def __init__(self, configFile_path: Path | str) -> None:
        """Creates a new instance of the SoundLight interface. 

        Args:
            configFile_path (Path | str): Path to the TOML file containing the configuration options for the execution.
        """
        self._load_config(configFile_path)
        self._fm = FileManager()
        self._an = Analyzer()
        self._gen = Generator()
        self._ex = Exporter()

        self._patchLoaded = False
        self._generationAlgorithmSet = False
        self._exportAlgorithmSet = False

        self._analysisComplete = False
        self._generationComplete = False
        self._exportComplete = False

    def _load_config(self, configFile_path: Path | str) -> None:
        # First call to Conf, to se the export path
        Conf(configFile_path)

    # ---------------------------------------------------------
    #                   File Managing
    # ---------------------------------------------------------

    def close_selected_song(self) -> None:
        """Closes the file for the selected song.
        If no song is selected, nothing happens.
        """
        if self._fm.has_selected_song():
            self._fm.close_song(self._fm.get_selected_song())

    def add_song_from_path(self, path: str | Path) -> None:
        """Adds a song into the song list from a file.

        Args:
            path (str | Path): Path to the song file
        """
        self._fm.load_song(path)

    def select_song(self, i: int) -> None:
        """Selects a song from all songs loaded. If the argument is not valid, raises NotFoundException.

        Args:
            i (int): Index of the song in the list.
        """
        self._fm.select_song(i)

    def get_selected_song(self) -> Song | None:
        """Returns the currently selected song. 

        Returns:
            Song | None: The currently selected song. If no song is selected, returns None.
        """
        if self._fm.has_selected_song():
            return self._fm.get_selected_song()
        else:
            return None

    def get_loaded_songs(self) -> List[Song]:
        """Gets the list of the currently loaded songs.

        Returns:
            List[Song]: List of loaded songs.
        """
        return self._fm.get_songs()

    # ---------------------------------------------------------
    #                     Configuration
    # ---------------------------------------------------------

    def set_patch(self, path: str | Path) -> None:
        """Loads a .json file containing the patch description, and configures the algorithms with it.
        Consult the documentation for format expectations.

        Args:
            path (str | Path): Path to the .json file containing the patch.
        """
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

    def set_generation_algorithm(self, algorithm: IGenerationAlgorithm) -> None:
        """Configures the feature generation algorithm for the program.

        Args:
            algorithm (IGenerationAlgorithm): Generation algorithm. Must implement the IGenerationAlgorithm interface.
        """
        if algorithm is not None and isinstance(algorithm, IGenerationAlgorithm):
            self._gen.set_algorithm(algorithm)
            self._generationAlgorithmSet = True

    def set_export_algorithm(self, exporter: IExportAlgorithm) -> None:
        """Configures the export algorithm for the program.

        Args:
            exporter (IExportAlgorithm): Export algorithm. Must implement the IExportAlgorithm interface.
        """
        if exporter is not None and isinstance(exporter, IExportAlgorithm):
            self._ex.set_algorithm(exporter)
            self._exportAlgorithmSet = True

    def set_export_path(self, path: str | Path) -> None:
        """Configures the export path where the generated projects will be stored. Must point to a folder.

        Args:
            path (str | Path): Path for the folder where the projects will be stored.
        """
        if isinstance(path, str):
            path = Path(path)

        if path.is_dir():
            self._exportPath: Path = path

    # ---------------------------------------------------------
    #                           Running
    # ---------------------------------------------------------

    def run(self) -> None:
        """Analyzes the selected song, generates features and exports the results for the selected song.

        Raises:
            NothingSelectedException: If there is no selected song.
            AssertionError: If either the patch, analysis algorithm, generation algorithm or export algorithm are not set.
        """
        assert self._patchLoaded
        assert self._analysisAlgorithmSet
        assert self._generationAlgorithmSet
        assert self._exportAlgorithmSet

        song = self._fm.get_selected_song()

        self._an.analyze(song)

        self._gen.set_patch(self._patch)
        self._gen.generate(song)

        self._ex.set_song(song)
        self._ex.export(self._exportPath)

    # ---------------------------------------------------------
    #                       Utils
    # ---------------------------------------------------------

    def _print_song_data(self) -> str:
        """Returns the selected song's data.

        Returns:
            str: String containing the data for the song.
        Raises:
            NothingSelectedException: if no song is selected.
        """
        return self._fm.get_selected_song().__repr__()

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
            folder_name = Conf()['export']['path'][get_OS()]
            file_name = Path(self._fm.get_selected_song()['path']).stem
            path = Path(f"{folder_name}/{file_name}.json")

            with open(path, 'w') as f:
                json.dump(self._fm.get_selected_song()._struct,
                          f, default=default)
        except NothingSelectedException as e:
            raise e
        except OSError as e:
            raise ValueError(f'Provided an invalid path: {path}')
