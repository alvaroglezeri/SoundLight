

from lxml.etree import Element as NewElement
from lxml.etree import _Element as XMLElement

from core.logger import Logger, LOG_CAT

import core.export.daslight5.sections.dlmfile as dlmfile
import core.export.daslight5.sections.configuration as configuration
import core.export.daslight5.sections.patchs as patchs
import core.export.daslight5.sections.fixturegroups as fixturegroups


def createElement(name: str, attributes: dict | None) -> XMLElement:
    """Creates a new XMLElement and adds all attributes passed.

    Args:
        name (str): _Element name._
        attributes (dict | None): _Attribute dictionary (key -> value pairs, mapped to attribute name -> value). If `None`, omits attribute creation._

    Returns:
        XMLElement: _Built XMLElement with all attributes set._
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

        Call the export() method to start the XMLElement exportation, and the get() method to obtain it.
        """

        self._d = {}
        self.dlmFile = None

        if not data:
            Logger.log(LOG_CAT.ERROR, f'No data to export!')
            # raise RuntimeError(f'No data to export!')
            self._data = {}
        else:
            self._data = data

    @property
    def d(self) -> dict:
        """Data created by the generator, employed by the export phases

        Returns:
            dict: _description_
        """
        return self._d

    def get(self) -> XMLElement:
        """
        Returns the XML DML file when created
        """
        return self.dlmFile

    def export(self) -> None:
        # Root
        dlmFile: XMLElement = dlmfile.write(self)

        # Section -> CONFIGURATION
        dlmFile.append(configuration.write(self))
        Logger.log(LOG_CAT.SUCCESS, f'Successfully created CONFIGURATION')

        # Section -> PATCHS
        dlmFile.append(patchs.write(self))
        Logger.log(LOG_CAT.SUCCESS, f'Successfully created PATCHS')

        # Section -> FIXTUREGROUPS
        dlmFile.append(fixturegroups.write(self))
        Logger.log(LOG_CAT.SUCCESS, f'Successfully created FIXTUREGROUPS')

        # Publishing dmlFile
        self.dlmFile = dlmFile
