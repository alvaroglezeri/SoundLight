import zlib
import lxml.etree as etree
from pathlib import Path
from lxml.etree import Element as NewElement
from lxml.etree import _Element as XMLElement

from core.logger import Logger, LOG_CAT

_PATCH_DATA_FILE = r"src/core/export/daslight5/patchData"


class DVCFileCreator():

    FILE_EXTENSION = 'dvc'

    def __init__(self, data: dict, attribs: dict | None = None) -> None:
        """
        Represents and builds the .dvc file.

        Parameters
        ----------
        data: dict
            Data for the fixture groups, scenes, etc.
            TODO: Extra explanations

        args: dict
            Attributes for the DLMFILE element itself. Can be left blank.

        Return
        ------
        element: lxml.etree._Element
            XML object representing the contents of the file
        """

        if not attribs:
            attribs: dict = {
                'TYPE': 'Daslight',
                'VERSION': '5',
                'DASBUILD': '24.1016.154.85',
                'VERSIONFILE': '2',
            }

        if not data:
            Logger.log(LOG_CAT.ERROR, f'No data to export!')
            raise RuntimeError(f'No data to export!')
        self._data = data

        self.dlmFile: XMLElement = self._createElement('DLMFILE', attribs)
        self.dlmFile.append(self._sectionConfiguration())
        self.dlmFile.append(self._sectionPatch())
        self.dlmFile.append(self._sectionFixtureGroups())

    def get(self) -> XMLElement:
        """
        WRITE
        """
        return self.dlmFile

    def _deflate(element: str | XMLElement, output: str = 'base64') -> str:
        """Returns the encoded, deflated string in the correct format

        DOCUMENT: All problems encountered with the Inflate/Deflate methods

        Args:
            element (str | XMLElement): _description_
            output (str, optional): _description_. Defaults to 'base64'.

        Returns:
            str: _description_
        """

        match element:
            case str():
                element: str
                data: str = element.replace(' ', '')
                # Remove zlib header and checksum, important for correct compression
                data: bytes = zlib.compress(data.encode('utf-8'))[2:-4]
            case XMLElement():
                element: XMLElement
                data: bytes = etree.tostring(
                    element, xml_declaration=True, encoding='utf-8')
                # Remove zlib header and checksum, important for correct compression
                data: bytes = zlib.compress(data)[2:-4]

        # Add Daslight header and compose full data packet
        header = bytes.fromhex('00000133')
        full_data = header + data

        match output:
            case 'base64':
                pass
            case 'hex':
                return full_data.hex()
            case _:
                pass

    def _createElement(self, name: str, attributes: dict | None) -> XMLElement:
        """
        Creates a new Element and adds all attributes passed
        """
        try:
            ret: XMLElement = NewElement(name)
            if attributes:
                for key, value in attributes.items():
                    ret.set(key, value)

            return ret
        except Exception as e:
            Logger.log(LOG_CAT.ERROR, f'Error creating element "{name}": {e}')
            return NewElement(name)

    # ------ SECTIONS -------

    def _sectionConfiguration(self, attribs: dict | None = None) -> XMLElement:
        """
        WRITE
        """

        dock_manager_data = '''
        <?xml version="1.0" encoding="UTF-8"?>
        <QtAdvancedDockingSystem Version="1" UserVersion="0" Containers="1">
            <Container Floating="0">
                <Splitter Orientation="-" Count="1">
                    <Area Tabs="1" Current="Page 1">
                        <Widget Name="Page 1" Closed="0"/>
                    </Area>
                    <Sizes>
                        18 
                    </Sizes>
                </Splitter>
            </Container>
        </QtAdvancedDockingSystem>'''

        if not attribs:
            attribs = {
                'VIEWZOOM': '0.75',
                'VIEWPOSX': '-90',
                'VIEWPOSY': '250',
                'TOUCH_DOCK_MANAGER': self._deflate(),
                'TOUCH_ZOOMS': '1',
            }

        ret: XMLElement = self._createElement('CONFIGURATION', attribs)
        Logger.log(LOG_CAT.SUCCESS, f'Successfully created CONFIGURATION')

        return ret

    def _sectionPatch(self, attribs: dict | None = None) -> XMLElement:
        """
        WRITE
        """

        if not attribs:
            try:
                path = Path(_PATCH_DATA_FILE)
                print(path)
                with open(path) as patchDataFile:
                    patchData: str = patchDataFile.read()

                attribs = {
                    'DATA': f'{patchData}',
                }
            except Exception as e:
                Logger.log(LOG_CAT.ERROR, f'Could not load patchData!')
                attribs = {}

        ret: XMLElement = self._createElement('PATCHS', attribs)
        Logger.log(LOG_CAT.SUCCESS, f'Successfully created PATCH')

        return ret

    def _sectionFixtureGroups(self, attribs: dict) -> XMLElement:
        """
        WRITE
        """

        ret: XMLElement = self._createElement('FIXTUREGROUPS')

        # Load data from lightGroups:

        for group in attribs['lightGroups']:
            ret.append(self._fixtureGroup(group))

        Logger.log(LOG_CAT.SUCCESS, f'Successfully created FIXTUREGROUPS')

        return ret

    def _fixtureGroup(self, group: dict) -> XMLElement:
        return self._createElement(f'{group["name"]}')

    # -------------------------------------------------
