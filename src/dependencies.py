from importlib.metadata import version
import warnings

import natten.utils
import natten.utils.log

#------------------------

with warnings.catch_warnings():
    warnings.simplefilter("ignore", FutureWarning, append=False)
    warnings.simplefilter("ignore", DeprecationWarning, append=False)

#------------------------

print(f'Importing numpy... ', end='')
try:
    import numpy
    print(f'Done ({version("numpy")})')
except Exception as e:
    print(f'Error importing "numpy"')
    print(e)

print(f'Importing librosa... ', end='')
try:
    import librosa
    print(f'Done ({version("librosa")})')
except Exception as e:
    print(f'Error importing "librosa"')
    print(e)

print(f'Importing tinytag... ', end='') 
try:
    import tinytag
    print(f'Done ({version("tinytag")})')
except Exception as e:
    print(f'Error importing "tinytag"')
    print(e)

print(f'Importing typing... ', end='')
try:
    import typing
    print(f'Done ({version("typing")})')
except Exception as e:
    print(f'Error importing "typing"')
    print(e)

print(f'Importing ffmpeg... ', end='')
try:    
    import ffmpeg
    print(f'Done ({version("ffmpeg")})')
except Exception as e:
    print(f'Error importing "ffmpeg"')
    print(e)

print(f'Importing Cython... ', end='')
try:    
    import Cython
    print(f'Done ({version("Cython")})')
except Exception as e:
    print(f'Error importing "Cython"')
    print(e)

print(f'Importing madmom... ', end='')
try:    
    import madmom
    print(f'Done ({version("madmom")})')
except Exception as e:
    print(f'Error importing "madmom"')
    print(f"Try pip install --upgrade --no-deps --force-reinstall --quiet 'git+https://github.com/CPJKU/madmom.git'")
    raise e

print(f'Importing deeprhythm... ', end='')
try:    
    import deeprhythm
    print(f'Done ({version("deeprhythm")})')
except Exception as e:
    print(f'Error importing "deeprhythm"')
    print(e)

print(f'Importing natten... ', end='')
try:    
    import natten
    #natten.utils.log.logging.disable()
    #print(natten.utils.log.LogLevel)
    print(f'Done ({version("natten")})')
except Exception as e:
    print(f'Error importing "natten"')
    print(e)

print(f'Importing allin1... ', end='')
try:    
    import allin1
    print(f'Done ({version("allin1")})')
except Exception as e:
    print(f'Error importing "allin1"')
    print(e)

