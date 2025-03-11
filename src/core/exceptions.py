class DuplicateElementException(Exception):
    """
    WRITE
    """
    def __init__(self, msg=f'This element is already registered.'):    
        super().__init__(msg)

class NotFoundException(Exception):
    """
    WRITE
    hola tomás
    """
    def __init__(self, msg=f'This element cannot be found.'):            
        super().__init__(msg)

class InvalidFileException(Exception):
    """
    WRITE
    """
    def __init__(self, msg=f'This file is invalid.'):            
        super().__init__(msg)

class CodecConversionExeption(Exception):
    """
    WRITE
    """
    def __init__(self, msg=f'A codec conversion must be performed.'):
        super().__init__(msg)

class NothingSelectedException(Exception):
    """
    WRITE
    """
    def __init__(self, msg=f'Nothing is selected.'):
        super().__init__(msg)