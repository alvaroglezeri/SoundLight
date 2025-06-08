from importlib.metadata import version, PackageNotFoundError
import importlib
import warnings

# ------------------------

print(f'Configuring warnings... ', end='')
with warnings.catch_warnings():
    warnings.simplefilter("ignore", FutureWarning, append=False)
    warnings.simplefilter("ignore", DeprecationWarning, append=False)
print('Done')

# ------------------------

modules = ['numpy', 'librosa', 'tinytag', 'typing', 'ffmpeg',
           'Cython', 'madmom', 'deeprythm', 'natten', 'allin1']

for module in modules:
    print(f'Importing {module}... ', end='')
    try:
        importlib.import_module(module)
        print(f'Done ({version(module)})')
    except PackageNotFoundError as e:
        print(f'Error importing "{module}" ({e})')
    except ImportError as e:
        print(f'Error importing "{module}" ({e})')
