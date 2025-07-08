# SoundLight

SoundLight is a framework for automatic generation of lighting projects for lighting controllers. It analyzes a song and creates project files compatible with various lighting control software, streamlining the process of synchronizing light shows to music.

## Table of Contents
- [About](#about)
- [Repository Structure](#repository-structure)
- [Prerequisites for Development](#prerequisites-for-development)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## About

SoundLight automates the process of creating synchronized lighting projects from audio tracks. It performs audio analysis, feature extraction, and exports the results to formats compatible with lighting controllers such as Daslight and Sweetlight. The framework is modular, allowing for custom analysis, generation, and export algorithms.

The goal of the repository is to provide a flexible, extensible, and easy-to-use tool for DJs, lighting designers, and event organizers who want to automate lightshow creation.

---

## Repository Structure

```
SoundLight/
│
├── notebooks/                # Jupyter notebooks for UI, tests, analysis, etc.
│   ├── UI.ipynb
│   ├── Analysis.ipynb
│   ├── dev_analysis.ipynb
│   ├── Generation.ipynb
│   ├── Exporter.ipynb
│   ├── Installation.ipynb
│   └── tests/
│       ├── notes.ipynb
│       └── tempo3.ipynb
│
├── src/                      # Main source code
│   ├── core/
│   │   ├── analysis/
│   │   │   └── simpleAlgorithm/
│   │   ├── export/
│   │   │   └── daslight5/
│   │   │       ├── features/
│   │   │       └── sections/
│   │   ├── generation/
│   │   │   └── simpleGenerator/
│   │   ├── model/
│   │   └── ...
│   ├── lib/
│   └── ...
│
├── test/                     # Unit and integration tests
│   ├── core/
│   │   ├── analysis/
│   │   ├── export/
│   │   ├── generation/
│   │   ├── model/
│   │   └── ...
│   ├── conftest.py
│   └── ...
│
├── resources/                # Audio and patch resources
│   ├── *.json
│   └── *.wav
│
├── output/                   # Output files (e.g., .dvc)
│
├── doc/                      # Documentation in Markdown
│   ├── Analysis.md
│   ├── Generation.md
│   └── SoundLight.md
│
├── requirements_1.txt        # Python requirements (part 1)
├── requirements_2.txt        # Python requirements (part 2)
├── dependencies.py           # Dependency checker script
├── run.py                    # Main entry point
├── soundlight.toml           # Project configuration
├── pytest.ini                # Pytest configuration
└── ...
```

Each directory contains code or resources relevant to its purpose. The `src/core` directory is the main entry point for the framework logic.

---

## Prerequisites for Development

Before running or developing SoundLight, ensure you have:

- **Python 3.10**: The framework is developed and tested with Python 3.10.  
  Install with:  
  ```bash
  sudo apt-get install python3.10 python3.10-dev
  ```
- **Build tools**:  
  ```bash
  sudo apt-get install build-essential
  ```
- **ffmpeg**: Required for audio conversion and processing.  
  Install with:  
  ```bash
  sudo apt install ffmpeg
  ```
- **pip**: For installing Python dependencies.
- **Other dependencies**: Listed in `requirements_1.txt` and `requirements_2.txt` (includes `tinytag`, `librosa`, `pytest`, `madmom`, `allin1`, etc.).
- **NATTEN**: Special installation required (see below).
- **MADMOM**: Install from GitHub (see below).
- **All-In-One**: Install via pip (see below).

---

## Installation

### Linux / Mac

1. Install `ffmpeg`:
   ```bash
   sudo apt install ffmpeg
   ```
2. Install Python 3.10 and development headers:
   ```bash
   sudo apt-get install python3.10 python3.10-dev
   ```
3. Install build tools:
   ```bash
   sudo apt-get install build-essential
   ```
4. Upgrade setuptools and wheel:
   ```bash
   pip install --upgrade setuptools wheel
   ```
5. Install Python dependencies:
   ```bash
   pip install -r requirements_1.txt
   pip install -r requirements_2.txt
   ```
6. Install NATTEN:
   - **GPU** (replace `cu124` with your CUDA version):
     ```bash
     pip install natten==0.17.1+torch240cu124 -f https://shi-labs.com/natten/wheels
     ```
   - **CPU**:
     ```bash
     pip install natten==0.17.1+torch240cpu -f https://shi-labs.com/natten/wheels
     ```
   See [Shi-Labs.com](https://www.shi-labs.com/natten/) for more info.
7. Install MADMOM with admin privileges:
   ```bash
   sudo pip install --upgrade --no-deps --force-reinstall --quiet 'git+https://github.com/CPJKU/madmom.git'
   ```
8. Install All-In-One:
   ```bash
   sudo pip install allin1
   ```

### Windows

If you wish to run SoundLight on Windows, you must first install WSL (Windows Subsystem for Linux) and then follow the Linux installation steps inside your WSL environment.

1. Install WSL:
   ```powershell
   wsl --install
   ```
2. Open your WSL terminal and follow the Linux instructions above.

---

## Usage

SoundLight can be used as a library in your own Python scripts or directly via script.

- **Directly via script** (see `run.py` for an example):
   ```bash
   python run.py
   ```

The typical workflow is:
1. Initialize a `SoundLight` instance with a config file.
2. Add and select a song.
3. Set the patch and algorithms.
4. Set the export path.
5. Run the process to analyze, generate, and export the project.

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'New feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

Please ensure your code is tested and follows the existing style.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact

For questions, suggestions, or feedback, please contact:

- **Author**: Álvaro González Erigoyen.
- **Email**: alvaroglezeri[at]pm.com

Feel free to open issues in the repository if you encounter any problems.

---

### Acknowledgments

This repository was inspired by the need for automated lightshow generation. Special thanks to all contributors and supporters, and to the authors of open-source libraries used in this project.
