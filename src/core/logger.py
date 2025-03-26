from abc import ABC, abstractmethod
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
# CATEGORY = Enum('Category', ['ERROR', 'INFO', 'WARN', 'SUCCESS', 'DEBUG'])


class ILogger(ABC):
    def __new__(cls):
        """
        Singleton implementation
        #WRITE
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(ILogger, cls).__new__(cls)
        return cls.instance

    @abstractmethod
    def log(msg: any) -> None:
        pass

    @abstractmethod
    def log(location: str, msg: any) -> None:
        pass

    @abstractmethod
    def log(category: LOG_CAT, location: str, msg: any) -> None:
        pass

    @staticmethod
    def isEnabled() -> bool:
        pass


class Logger(ILogger):
    """
    Debug Console Logger

    WRITE
    """

    _outF: callable = print

    @classmethod
    def setOutputFunction(cls, output: callable) -> None:
        cls._outF = output

    @staticmethod
    def log(category: LOG_CAT, msg: any) -> None:
        if enable:
            # Obtain caller function frame
            frame = inspect.currentframe().f_back
            class_name: str = None

            if "self" in frame.f_locals:  # For instance methods
                class_name: str = frame.f_locals["self"].__class__.__name__
            elif "cls" in frame.f_locals:  # For class methods
                class_name: str = frame.f_locals["cls"].__name__

            caller_name: str = frame.f_code.co_name

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
            if class_name:
                Logger._outF(f'{label} at {class_name}.{caller_name}: {msg}')
            else:
                Logger._outF(f'{label} at {caller_name}: {msg}')

    @staticmethod
    def isEnabled() -> bool:
        return enable
