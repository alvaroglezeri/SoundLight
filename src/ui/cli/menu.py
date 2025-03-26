from ui.cli.consoleUtils import ConsoleUtils
from ui.cli.commands import ICommand
from core.exceptions import DuplicateElementException, NotFoundException


class Menu:
    def __init__(self) -> None:
        self._c = ConsoleUtils
        self._options: dict[str, ICommand] = {}

    def addOption(self, o: ICommand) -> None:
        if o.getKey() not in self._options.keys():
            self._options.update({o.getKey(): o})
        else:
            raise DuplicateElementException(f'This option already exists.')

    # def setPath(self, path: str) -> None:
    #    self._path = path

    def _getOption(self, key) -> ICommand:
        if key in self._options.keys():
            return self._options.get(key)
        else:
            raise NotFoundException(f'This option cannot be found')

    def showOptions(self) -> None:
        self._c.nl()
        self._c.print(f'Available commands: ')
        for o in self._options.values():
            self._c.print(f'> "{o.getKey()}": {o.getDescription()}')
        self._c.nl()

    def askOption(self) -> ICommand:
        choice = self._c.input(f'Choose an option:')

        return self._getOption(choice)

    def splashScreen(self) -> None:
        self._c.clear()
        self._c.nl()
        self._c.print(
            f'----------------------------------------------------------------------------------------')
        self._c.print(
            f'                                    SoundLight CLI                                      ')
        self._c.print(
            f'----------------------------------------------------------------------------------------')
        # self.c.printInfo(f'Running {__file__} as {__name__} in {__package__} from: {self._path}')
        self._c.nl()
