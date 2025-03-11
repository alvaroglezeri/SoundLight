from core.exceptions import NotFoundException
import core.logger as Logger
from ui.cli.menu import Menu
from ui.cli.commands import *
from ui.cli.consoleUtils import ConsoleUtils

class Cli():

    def __init__(self):
        Logger.enable = False
        self.menu = Menu()
        self._c = ConsoleUtils
        self.setUpOptions()

    def setUpOptions(self) -> None:            
        self.menu.addOption(AddFile())
        self.menu.addOption(SelectFile())
        self.menu.addOption(AnalyzeFile())
        self.menu.addOption(Exit())

    def setPath(self, path: str) -> None:
        self.menu.setPath(path)

    def run(self):
        self.menu.splashScreen()

        while True:
            self.menu.showOptions()

            option: ICommand
            try:
                option = self.menu.askOption()
                option.execute()
            except NotFoundException as nfe:
                self._c.printError(f'Unknown option')
            except Exception as e:
                self._c.printError(f'An error has ocurred:')
                self._c.printInfo(f'Error type: {type(e)}')
                self._c.print(e)
            
                
            