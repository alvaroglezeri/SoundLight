from . import soundlight
from . import export        # Needs ?
from . import generation    # Needs ?
from . import analysis      # Needs SongData, FileManager
from . import fileManager   # Needs SongData, generation.IFeature
from .model import song      # Needs generation.IFeature
from . import logger
from . import exceptions
import os
# Define the __all__ variable
__all__ = ["fileManager", "analysis",
           "exceptions", "logger", "soundlight", "song"]

print(f'Loading package "{__name__}":')
print(f' > Root package: {__package__}')
print(f' > {os.path.dirname(__file__)}')
for m in __all__:
    print(f'   ┣ {m}')
print()

# Import the submodules


# Last one
"""
from core.fileManager import FileManager
from core.analysis.analysisDirector import AnalysisDirector
from core.generation.featureGenerator import FeatureGenerator
from core.generation.simpleGenerator import SimpleGenerator
from core.export.daslight5.Daslight5Exporter import Daslight5Exporter
"""
