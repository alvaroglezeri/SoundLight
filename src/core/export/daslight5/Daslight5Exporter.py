from abc import ABC, abstractmethod
from typing import List
import lxml.etree as etree
from lxml.etree import Element as NewElement
from lxml.etree import _Element as XMLElement
from src.core.exceptions import InvalidArgumentException

from ...conf import Conf
from ...export.exporter import IExportAlgorithm
from ...model.song import Song


def create_element(name: str, attributes: dict | None = None) -> XMLElement:
    """Creates a new XMLElement and adds all attributes passed.

    Args:
        name (str): Element name.
        attributes (dict | None): Attribute dictionary (key -> value pairs, mapped to attribute name -> value). If `None`, omits attribute creation.

    Returns:
        XMLElement: Built XMLElement with all attributes set.
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

# --------------------------------------------------------------------------


class Section(ABC):
    """Represents a section of the XML file to be generated.
    """
    @abstractmethod
    def __init__(self, dlmfile: XMLElement):
        """Instantiate the section, with the XML element on which to generate.

        Args:
            dlmfile (XMLElement): XML element for the file.
        """
        ...

    @abstractmethod
    def write(self, song: Song) -> XMLElement:
        """Creates the XMLElement data for the section, for the specified song.
        Must then be added to the DLM file. 
        Args:
            song (Song): Song for which to generate the section.

        Returns:
            XMLElement: Section, in XML form.
        """
        ...

# --------------------------------------------------------------------------


class Daslight5Exporter(IExportAlgorithm):
    """Export algorithm for Daslight 5's .dvc files. Generates the patch, the scenes and a timeline scene with all features placed.
    """

    def __init__(self) -> None:
        """
        Represents and builds the .dvc file.

        Call the export() method to start the XMLElement exportation, and the get() method to obtain the results.
        """
        self.dlmFile: XMLElement | None = None

    def set_song(self, song: Song) -> None:
        self._song = song

    def get_keystring(self) -> str:
        return 'daslight5'

    @property
    def file_extension(self) -> str:
        return 'dvc'

    # --------------------------------------------------------------------------

    def export(self) -> List[str]:
        """Runs the export process for this song. Feature generation must be complete, otherwise no features will be generated.

        Args:
            song (Song): Song to export.
        """
        # Sections are imported now to avoid circular dependencies.
        from core.export.daslight5.sections.configuration import Configuration
        from core.export.daslight5.sections.patchs import Patchs
        from core.export.daslight5.sections.fixturegroups import FixtureGroups
        from core.export.daslight5.sections.scenes import Scenes
        # from core.export.daslight5.sections.shortcuts import Shortcuts
        from core.export.daslight5.sections.touch import Touch
        # from core.export.daslight5.sections.devices import Devices

        attribs: dict = Conf()['export']['daslight5']['dlmfile']

        self.dlmFile = create_element('DLMFILE', attribs)

        configuration = Configuration(self.dlmFile)
        self.dlmFile.append(configuration.write(self._song))

        patchs = Patchs(self.dlmFile)
        self.dlmFile.append(patchs.write(self._song))

        fixturegroups = FixtureGroups(self.dlmFile)
        self.dlmFile.append(fixturegroups.write(self._song))

        scenes = Scenes(self.dlmFile)
        self.dlmFile.append(scenes.write(self._song))

        # shortcuts = Shortcuts(self.dlmFile)
        self.dlmFile.append(create_element('SHORTCUTS'))

        touch = Touch(self.dlmFile)
        self.dlmFile.append(touch.write(self._song))

        # devices = Devices(self.dlmFile)
        self.dlmFile.append(create_element('DEVICES'))

        ret: str = etree.tostring(
            self.dlmFile, pretty_print=True, encoding="unicode")  # type: ignore reportCallIssue
        return ret.splitlines()
