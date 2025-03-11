from io import TextIOWrapper
from pathlib import Path
from deprecated import deprecated
from lxml import etree

from core.logger import DCL, LOG_CAT
from core.fileManager import FileManager

from .features import *
from .Daslight5Structure import DVCFileCreator 

_FILE_EXTENSION: str = '.dvc'

class Daslight5Exporter():

    def __init__(self) -> None:
        """
        WRITE
        """
        # FIXME: A way to represent the fixtures is needed
        self._fm: FileManager = FileManager()

        DCL.log(LOG_CAT.WARN, f'Fixture Groups are not available!')
        self._groups: list = list()
        DCL.log(LOG_CAT.WARN, f'Banks are not available!')
        self._banks: list = list()

    def export(self, path: Path):
        """
        WRITE
        """
        DCL.log(LOG_CAT.INFO, f'Starting export...')

        try:
            exportPath: Path = Path(f'{path.absolute().joinpath(self._fm.getSelectedFile().title)}{_FILE_EXTENSION}')
            DCL.log(LOG_CAT.INFO, f'Output file: {exportPath}')

            with open(exportPath, 'wt') as output:
                xml = DVCFileCreator().get()
                for line in etree.tostring(xml, pretty_print=True, encoding="unicode").splitlines():
                    print(f'Writing: {line}')
                    print()
                    output.write(f'{line}\n')
                
        except Exception as e:
            DCL.log(LOG_CAT.ERROR, f'Error exporting file: {e}')    

    # --------------------
