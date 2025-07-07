from abc import ABC, abstractmethod
from collections.abc import Callable
from enum import Enum
import inspect

enable: bool = True


class COLORS:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class LOG_CAT(Enum):
    ERROR = 'FAIL'
    INFO = 'INFO'
    WARN = 'WARN'
    SUCCESS = 'SUCC'
    DEBUG = 'DEBG'


class Logger():
    """
    Default logger for the application.
    """

    _outF: Callable = print

    @classmethod
    def set_output_function(cls, output: Callable) -> None:
        """Sets the function to which the message strings will be passed.

        Args:
            output (Callable): Function receiving a string.
        """
        cls._outF = output

    @staticmethod
    def log(category: LOG_CAT, msg) -> None:
        """Logs a message. Also records the category of the message.

        Args:
            category (LOG_CAT): _description_
            msg (_type_): _description_
        """
        if enable:
            # Obtain caller function frame
            c_frame = inspect.currentframe()
            if c_frame != None:
                frame = c_frame.f_back
            else:
                frame = None
            class_name: str | None = None

            if frame == None:
                class_name = None
            elif "self" in frame.f_locals:  # For instance methods
                class_name = frame.f_locals["self"].__class__.__name__
            elif "cls" in frame.f_locals:  # For class methods
                class_name = frame.f_locals["cls"].__name__

            caller_name: str | None
            if frame != None:
                caller_name = frame.f_code.co_name
            else:
                caller_name = None

            # Select terminal color
            match category:
                case LOG_CAT.ERROR as cat:
                    label: str = f'{COLORS.BOLD}{COLORS.FAIL}[{cat.value}]{COLORS.ENDC}'
                case LOG_CAT.INFO as cat:
                    label: str = f'{COLORS.BOLD}[{cat.value}]{COLORS.ENDC}'
                case LOG_CAT.WARN as cat:
                    label: str = f'{COLORS.BOLD}{COLORS.WARNING}[{cat.value}]{COLORS.ENDC}'
                case LOG_CAT.SUCCESS as cat:
                    label: str = f'{COLORS.BOLD}{COLORS.OKGREEN}[{cat.value}]{COLORS.ENDC}'
                case LOG_CAT.DEBUG as cat:
                    label: str = f'{COLORS.UNDERLINE}[{cat.value}]{COLORS.ENDC}'
                case _:
                    label: str = f'[????]'

            # Construct final message
            if class_name and caller_name:
                Logger._outF(f'{label} at {class_name}.{caller_name}: {msg}')
            elif class_name:
                Logger._outF(f'{label} at {class_name}: {msg}')
            elif caller_name:
                Logger._outF(f'{label} at {caller_name}: {msg}')
            else:
                Logger._outF(f'{label}: {msg}')

    @staticmethod
    def is_enabled() -> bool:
        return enable
