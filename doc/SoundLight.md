<!--- Link references --->
[1]: https://ffmpeg.org/ (ffmpeg.org)
[2]: https://github.com/tinytag/tinytag (GitHub: tinytag)
[3]: https://github.com/mir-aidj/all-in-one (GitHub: AllInONe)
[4]: https://github.com/bleugreen/deeprhythm (GitHub: DeepRhythm)

<!--- --->

---
# SoundLight

SoundLight is a framework for creating automatic generators of lighting projects for lighting controllers, with the ability to analyze a song and automatically create the project files for the lighting controllers.

## Data Model
The data model for the app is as follows:

1. Class `SongData`: models a song. It contains the audio file itself, its metadata, and all analysis and generation artifacts created in the process. Its structure is as follows:
    - `file`: contains all info regarding the original song: the file, its path and metadata extracted with [tinytag][2].

    - `analysis`: contains all info extracted from the [Analysis](./Analysis.md) phase:
        - `aio`: contains the info extracted from [All In One][3].
        - `deeprhythm`: contains the info extracted from [DeepRhythm][4]
        - `a`:

    - `features`: contains the generated [features](./Generation.md#features) for this file.

## Audio Input 
In this task, the audio is loaded in the program. The file metadata is read and, if needed, converted to the appropriate format.
Also, the audio levels might be normalized and other preprocessing steps are taken, if necessary.

This task employs [ffmpeg][1] to convert audio between codecs and [tinytag][2] to read the file's metadata.

[ffmpeg][1] needs to be installed in the host system. If running on Windows, use `winget install ffmpeg`.
[tinytag][2] is installed with `pip install tinytag`.