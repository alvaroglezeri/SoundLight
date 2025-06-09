from deprecated import deprecated


class DuplicateElementException(Exception):
    """
    Raised when trying to add an element that is already registered.
    """

    def __init__(self, msg=f'This element is already registered.'):
        super().__init__(msg)


class NotFoundException(Exception):
    """
    Raised when an element cannot be found.
    """

    def __init__(self, msg=f'This element cannot be found.'):
        super().__init__(msg)


class InvalidFileException(Exception):
    """
    Raised when the format for a file is invalid.
    """

    def __init__(self, msg=f'This file is invalid.'):
        super().__init__(msg)


@deprecated
class CodecConversionExeption(Exception):
    """
    DEPRECATED: Raised when a codec conversion must be performed. Contains the path where the new conversion must be done at.
    """

    def __init__(self, newPath: str, msg=f'A codec conversion must be performed.'):
        super().__init__(msg)
        self._newPath = newPath

    def get_new_path(self) -> str:
        return self._newPath


class NothingSelectedException(Exception):
    """
    Raised when asked for the selected element, but none is selected.
    """

    def __init__(self, msg=f'Nothing is selected.'):
        super().__init__(msg)


class ArgumentException(Exception):
    """Raised when checking function arguments.
    """

    def __init__(self, msg=f'The argument provided is invalid!'):
        super().__init__(msg)


class InvalidStateException(Exception):
    """Raised when checking the state of objects before or after operations.
    """

    def __init__(self, msg=f'Object is in an invalid state!'):
        super().__init__(msg)
