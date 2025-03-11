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
#CATEGORY = Enum('Category', ['ERROR', 'INFO', 'WARN', 'SUCCESS', 'DEBUG'])

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

class DCL(ILogger):
    """
    Debug Console Logger
    
    WRITE
    """
    """
    @staticmethod
    def log(msg: any) -> None:
        if enable:
            print(f'[DEBUG]: {msg}') 
        
    @staticmethod
    def log(location: str, msg: any) -> None:
        if enable:
            print(f'[DEBUG] at {location}: {msg}')
            
    @staticmethod
    def log(category: CATEGORY, location: str, msg: any) -> None:
        if enable:
            print(f'[DEBUG:{category.value}] at {location}: {msg}')
    """

    @staticmethod
    def log(category: LOG_CAT, msg: any) -> None:
        if enable:
            frame = inspect.currentframe().f_back  # Marco de la función que llamó a log()
            class_name:str = None

            if "self" in frame.f_locals:  # Si es un método de instancia
                class_name:str = frame.f_locals["self"].__class__.__name__
            elif "cls" in frame.f_locals:  # Si es un método de clase
                class_name:str = frame.f_locals["cls"].__name__

            caller_name: str = frame.f_code.co_name

            # Select terminal color
            match category:
                case LOG_CAT.ERROR as cat:
                    label: str = f'{COLORS.BOLD}{COLORS.FAIL}[DEBUG:{cat.value}]{COLORS.ENDC}'
                case LOG_CAT.INFO as cat:
                    label: str = f'{COLORS.BOLD}[DEBUG:{cat.value}]{COLORS.ENDC}'
                case LOG_CAT.WARN as cat:
                    label: str = f'{COLORS.BOLD}{COLORS.WARNING}[DEBUG:{cat.value}]{COLORS.ENDC}'
                case LOG_CAT.SUCCESS as cat:
                    label: str = f'{COLORS.BOLD}{COLORS.OKGREEN}[DEBUG:{cat.value}]{COLORS.ENDC}'
                
                case _:
                    label: str = f'[DEBUG]'
                    

            if class_name:
                print(f'{label} at {class_name}.{caller_name}: {msg}')
            else:
                print(f'{label} at {caller_name}: {msg}')

    @staticmethod
    def isEnabled() -> bool:
        return enable
    

