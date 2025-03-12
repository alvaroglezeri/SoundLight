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

        if not attribs:
            attribs = {
                'VIEWZOOM': '0.75',
                'VIEWPOSX': '-90',
                'VIEWPOSY': '250',
                'TOUCH_DOCK_MANAGER': '0000013378da758f4b0fc2201084effe8a0d77adde3c20c6d478f4115f672c9b86d882816da3fe7a976ab879627686fd06e4f2d936d06388d6bb85984da602d055de58572fc4f9b419cfc552c903ad4caf5d8566edab3b67c757246ce19217059c23863c33a6f48eb475eca458c93cc3a6f19a868229fbc7476389d8de058b7c8506c038013a47dfdd55400d277d1b50507621608af6ba4648f9d59a1a09b6bac5ec42d9f8882695144a1609c165f68d51cde6208bafe4f3d7cf323f91f59f2fabd107e73f6544',
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
