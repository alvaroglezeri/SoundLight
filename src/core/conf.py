import json
from pathlib import Path
import toml

from src.core.exceptions import InvalidArgumentException, InvalidStateException


class Conf():
    """Stores the configuration parameters loaded from 'soundlight.toml'
    """

    def __new__(cls, config_path: Path | None = None):
        """
        Singleton implementation. The config is set on the first call.
        """
        if not hasattr(cls, 'instance'):
            cls.instance = object.__new__(cls)
            try:
                cls.instance.__setup__(config_path)
            except Exception as e:
                del cls.instance
                raise e
        return cls.instance

    @classmethod
    def reset(cls) -> None:
        if hasattr(cls, 'instance'):
            del cls.instance

    def __setup__(self, config_path: Path | None = None) -> None:
        """Loads the setup file into an internal dict.

        Args:
            config_path (Path | None, optional): Path to the TOML file.
        """
        if config_path is None or not config_path.is_file():
            raise InvalidArgumentException(
                'Invalid path to config file provided!')

        try:
            with open(config_path, "r") as f:
                self._config = toml.load(f)
        except toml.TomlDecodeError as e:
            raise InvalidArgumentException(
                'The content of the file cannot be parsed as TOML!')
        if self._config is None:
            raise InvalidArgumentException('The file could not be loaded!')

    def __init__(self, config_path: Path | str | None = None) -> None:
        """Provides an access to the current Configuration, regardless of context.
        Implemented as a singleton. The first call must provide the 'config_path' param.

        Args:
            config_path (Path | str | None): Path to the TOML file with the configuration parameters.
        """
        # Empty __init__, so to not rebuild the singleton
        return

    def __getitem__(self, key: str):
        """Obtains an entry from the configuration file.

        Raises:
            ValueError: When the key is not present.
        """
        if not self._config:
            raise InvalidStateException('No configuration data exists!')
        try:
            return self._config[key]
        except:
            raise ValueError('Key not found!')

    def __setitem__(self, key, value) -> None:
        """Setting data in the config file is not supported!

        Raises:
            Exception: When called.
        """
        raise Exception('This method is not supported!')
