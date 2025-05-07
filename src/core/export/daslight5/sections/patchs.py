import zlib
import base64
import lxml.etree as etree
from lxml.etree import _Element as XMLElement
from pathlib import Path
import uuid

from core.model.song import Song
from core.export.daslight5.Daslight5Creator import createElement, Section
from core.export.daslight5.SSL2Parser import SSL2Parser

# 2D-view size. 1 square = 10 units
SIZE_2D: int = 30

# Counter for the fixtures, starts in 1
FIXTURE_INDEX: int = 1


class Patchs(Section):

    def __init__(self, dlmfile: XMLElement):
        self.dlmfile = dlmfile

    @staticmethod
    def _deflatePatchData(element: str | XMLElement) -> str:
        """Deflates the Patch Data XML section into its Base64 encoded representation.
        Inlcudes the 4-byte ignored header.
        Args:
            element (str | XMLElement): XML element or string to encode.

        Returns:
            str: string with the Base64 encoded representation of the XML.
        """
        match element:
            case str():
                data: bytes = element.encode('utf-8')

            case XMLElement():
                data: bytes = etree.tostring(
                    element, encoding='utf-8')  # type: ignore

        # Compressing and padding
        data = zlib.compress(data)
        data = bytearray(data)

        # Adding empty header:
        header = bytes(4)
        data = header + data

        # return data
        return base64.b64encode(data).decode()

    def _organizeData(self, song: Song) -> dict:
        """Transforms the contents of the song object into a dict for use here.
        WRITE

        Args:
            song (Song): _description_

        Returns:
            dict: _description_
        """
        # FIXME: Update types

        organized = {}
        organized['numberFixtures'] = 0
        organized['fixtureTypes'] = []
        f_type: str
        for f_type in provided['patch']['fixtureTypes']:
            fixtureType: dict = {}
            fixtureType['name'] = f_type
            fixtureType['sslPath'] = self._get_sslPath_for(f_type)

            fixtureType['fixtures'] = []
            fixtureType['fixtures'] = provided['patch']['fixtureTypes'][f_type]['fixtures']
            organized['numberFixtures'] += len(fixtureType['fixtures'])

            organized['fixtureTypes'].append(fixtureType)

        return organized

    def _get_sslPath_for(self, fixtureType: str) -> str:
        # TODO: Externalize this
        paths: dict = {
            "ParCan": r"V:\Programas\Daslight\ScanLibrary\_Generic\PAR 64.ssl2",
            "RGBW": r"V:\Programas\Daslight\ScanLibrary\_Generic\RGBW.ssl2"
        }
        return paths[fixtureType]

    # -------------------------------------------------------------

    def write(self, song: Song) -> XMLElement:
        # Reset fixture index
        global FIXTURE_INDEX
        FIXTURE_INDEX = 1

        # Organize and prepare the data for the structure creation
        data = self._organizeData(song)

        # Generate the XML structure
        xml_patch_data: XMLElement = self._patch_data(data)

        # Deflate and code in Base64 for export
        attribs = {
            'DATA': self._deflatePatchData(xml_patch_data)
        }

        return createElement('PATCHS', attribs)

    # -------------------------------------------------------------

    def _patch_data(self, data: dict) -> XMLElement:
        patch: XMLElement = createElement('PATCH')

        # The total number of fixtures in the patch
        patch.set('NBFIXTURE', str(data['numberFixtures']))

        # Each section deals with a specific type of fixture
        for fixtureType in data['fixtureTypes']:
            patch.append(self._fixtures(fixtureType))

        return patch

    # -------------------------------------------------------------

    def _fixtures(self, fixtureType: dict) -> XMLElement:
        sectionFixtures: XMLElement = createElement('FIXTURES')

        # SSLLIBRARY
        sectionSslLibrary: XMLElement = self._ssl_library(fixtureType)
        sectionFixtures.append(sectionSslLibrary)

        # FIXTURE
        for fixture in fixtureType['fixtures']:
            sectionFixtures.append(self._fixture(sectionSslLibrary, fixture))

        return sectionFixtures

    # -------------------------------------------------------------

    def _ssl_library(self, fixtureType: dict) -> XMLElement:
        # Parser for the SSL2 file
        ssl2_parser: SSL2Parser = SSL2Parser()
        ssl2_parser.load(fixtureType['sslPath'])

        # <SSLLIBRARY>
        sectionSslLibrary: XMLElement = createElement('SSLLIBRARY')
        sectionSslLibrary.set(
            'SSLFIXUID', ssl2_parser.parse('//SSLLIBRARY/@SSLLCUID'))

        sslName: str = str(Path(*Path(fixtureType['sslPath']).parts[-2:]))
        sectionSslLibrary.set('SSLNAME', sslName)

        # The whole SSLPROPERTIES section can be imported as-is
        sectionSslProperties = ssl2_parser.get(
            '/DLMFILE/SSLLIBRARY/SSLPROPERTIES')
        sectionSslLibrary.append(sectionSslProperties)

        # The whole SSLMODES section can be imported as-is
        sectionSslModes = ssl2_parser.get(
            '/DLMFILE/SSLLIBRARY/SSLMODES')
        sectionSslLibrary.append(sectionSslModes)

        return sectionSslLibrary

    # -------------------------------------------------------------

    def _fixture(self, sectionSslLibrary: XMLElement, fixtureType: dict) -> XMLElement:
        global FIXTURE_INDEX
        sectionSslProperties: XMLElement = sectionSslLibrary[0]

        sectionFixture: XMLElement = createElement('FIXTURE')

        sectionFixture.set('TYPE', '0')  # Default 0, unknown value

        # Setting UUID and saving it
        fixture_DasUID: str = str(uuid.uuid4())
        fixtureType['DasUID'] = fixture_DasUID
        sectionFixture.set('DASUID', fixture_DasUID)

        sectionFixture.set('NAME', str(
            sectionSslProperties.get('SSLRDMFIXTURENAME', 'unknown')))
        # Global number of the fixture
        sectionFixture.set('INDEX', str(FIXTURE_INDEX))
        sectionFixture.set('SHAPE', '1')   # Default 1
        sectionFixture.set('SIZE', str(SIZE_2D))
        # We add 1 to avoid bugs in 0,0. The result is visually the same
        # X-coord in 2D view
        sectionFixture.set('POSX', str(fixtureType['coords'][0] + 1))
        # Y-coord in 2D view
        sectionFixture.set('POSY', str(fixtureType['coords'][1] + 1))
        sectionFixture.set('ANGLE', '0')  # Default 0
        sectionFixture.set('ADDRESS', str(fixtureType['address']))
        sectionFixture.set('UNIVERS', str(fixtureType['universe']))

        # This properties can be safely ignored, as they are loaded on-the-fly
        # sectionFixture.set('OUTMODE', )
        # sectionFixture.set('FLAG', )

        # sectionFixture.append(self._beam(fixtureType))

        FIXTURE_INDEX += 1
        return sectionFixture

    def _beam(self, fixtureType: dict) -> XMLElement:
        ret: XMLElement = createElement('BEAM')

        ret.set('INDEX', '0')
        ret.set('POSX', str(fixtureType['coords'][0] + 1))
        ret.set('POSY', str(fixtureType['coords'][1] + 1))

        return ret
