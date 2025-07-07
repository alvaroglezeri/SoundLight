import dependencies
import os

from src.core.soundlight import SoundLight

# TODO: Refactor code to use the built-in logger
from src.core.logger import Logger

from src.core.analysis.simpleAlgorithm.simpleAlgorithm import SimpleAlgorithm
from src.core.generation.simpleGenerator.simpleGenerator import SimpleGenerator 
from src.core.export.daslight5.Daslight5Exporter import Daslight5Exporter

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    # We configure the logging to be done in the built-in console
    Logger.set_output_function(print)
    
    sl = SoundLight('soundlight.toml')

    sl.add_song_from_path(
        r"resources/CamelPhat, Yannis, Foals - Hypercolour.wav")
    sl.select_song(0)

    sl.set_patch_from_path(r"resources/patch.json")

    sl.set_analysis_algorithm(SimpleAlgorithm())
    sl.set_generation_algorithm(SimpleGenerator())
    sl.set_export_algorithm(Daslight5Exporter())
    sl.set_export_path(r"output/")

    sl.run()
    sl._save_song_data()
   
