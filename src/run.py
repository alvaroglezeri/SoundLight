import dependencies
import os

from core.soundlight import SoundLight
from core.logger import Logger

# TODO: Update function, class and variable names to follow Python code conventions

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    # We configure the logging to be done in the built-in console
    Logger.setOutputFunction(print)

    try:
        sl = SoundLight()

        sl.addSongFromPath(
            r"resources/CamelPhat, Yannis, Foals - Hypercolour.mp3")
        sl.selectSong(0)

        # sl._printSongMetadata()

        sl.analyze()
        sl.generate()
        sl.export(r"output/")

        # for key, value in sl._fm.getSelectedSong().getMetadata().items():
        #    print(f'{key}: {value}')

    except Exception as e:
        raise e
