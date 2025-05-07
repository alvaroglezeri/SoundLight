from abc import ABC, abstractmethod
import lxml.etree as etree
from lxml.etree import Element as NewElement
from lxml.etree import _Element as XMLElement
import json

from core.export.exporter import ProjectCreator
from core.model.song import Song


def createElement(name: str, attributes: dict | None = None) -> XMLElement:
    """Creates a new XMLElement and adds all attributes passed.

    Args:
        name (str): _Element name._
        attributes (dict | None): _Attribute dictionary (key -> value pairs, mapped to attribute name -> value). If `None`, omits attribute creation._

    Returns:
        XMLElement: _Built XMLElement with all attributes set._
    """
    try:
        ret: XMLElement = NewElement(name, attrib=None, nsmap=None)
        if attributes:
            for key, value in attributes.items():
                ret.set(key, value)

        return ret
    except Exception as e:
        print(f'Error creating element "{name}": {e}')
        return NewElement(name, attrib=None, nsmap=None)


class Section(ABC):
    """_summary_
    WRITE

    Args:
        ABC (_type_): _description_
    """
    @abstractmethod
    def __init__(self, dlmfile: XMLElement):
        ...

    @abstractmethod
    def write(self, song: Song) -> XMLElement:
        ...


class DVCFileCreator(ProjectCreator):

    _FILE_EXTENSION = 'dvc'

    def __init__(self) -> None:
        """
        Represents and builds the .dvc file.

        Call the export() method to start the XMLElement exportation, and the get() method to obtain the results.
        """
        self.dlmFile: XMLElement | None = None
        self.done: bool = False

    @property
    def fileExtension(self) -> str:
        return self._FILE_EXTENSION

    def get(self) -> list[str] | None:
        """
        Returns the XML file as a list of strings
        """
        if not self.done:
            print('WARNING: Export not finished!')
            return None
        if not self.dlmFile == None:
            ret: str = etree.tostring(
                self.dlmFile, pretty_print=True, encoding="unicode")  # type: ignore reportCallIssue
            return ret.splitlines()
        else:
            return None

    def export(self, song: Song) -> None:
        """_summary_
        WRITE

        Args:
            song (Song): _description_
        """
        from core.export.daslight5.sections.configuration import Configuration
        from core.export.daslight5.sections.patchs import Patchs
        from core.export.daslight5.sections.fixturegroups import FixtureGroups

        # Root
        attribs: dict = {
            'TYPE': 'Daslight',
            'VERSION': '5',
            'DASBUILD': '24.1016.154.85',
            'VERSIONFILE': '2',
        }
        self.dlmFile = createElement('DLMFILE', attribs)

        # Section -> CONFIGURATION
        configuration = Configuration(self.dlmFile)
        self.dlmFile.append(configuration.write(None))
        print(f'Successfully created CONFIGURATION')

        # Section -> PATCHS
        patchs = Patchs(self.dlmFile)
        self.dlmFile.append(patchs.write(song))
        print(f'Successfully created PATCHS')

        # Section -> FIXTUREGROUPS
        fixturegroups = FixtureGroups(self.dlmFile)
        self.dlmFile.append(fixturegroups.write(song))
        print(f'Successfully created FIXTUREGROUPS')

        # Other sections...

        self.done = True
