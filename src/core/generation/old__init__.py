import os
# Define the __all__ variable
__all__ = ["features", "featureGenerator", "lightGroups", "simpleGenerator"]

print(f'Loading package "{__name__}":')
print(f' > Root package: {__package__}')
print(f' > {os.path.dirname(__file__)}')
for m in __all__:
    print(f'   ┣ {m}')
print()

# Import the submodules

from src.core import lightGroups       
from core.generation import features          # Needs lightGroup, featureGenerator
from core.generation import featureGenerator  # Needs FileManager, features

from core.generation import simpleGenerator   # 
