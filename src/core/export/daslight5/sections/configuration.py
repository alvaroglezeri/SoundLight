import zlib
import lxml.etree as etree
from lxml.etree import _Element as XMLElement

from ....conf import Conf
from ....model.song import Song
from ....export.daslight5.Daslight5Exporter import create_element, Section


class Configuration(Section):
    """CONFITURATION element in the DLM file.
    """

    def __init__(self, dlmfile: XMLElement):
        self.dlmfile = dlmfile

    @staticmethod
    def _deflate_touchdock(element: str | XMLElement) -> str:
        """Returns the encoded, deflated Touch Control data in the correct format.
        DOCUMENT: This had to be reverse engineered

        Args:
            element (str | XMLElement): XMLElement to deflate.

        Returns:
            str: Deflated string in hexadecimal format.
        """

        match element:
            case str():
                data: bytes = element.encode("utf-8")

            case XMLElement():
                data: bytes = etree.tostring(
                    element, xml_declaration=True, encoding="utf-8"  # type: ignore
                )

        # Remove zlib header and checksum
        data: bytes = zlib.compress(data)[2:-4]

        # Adding empty header
        header = bytes(4)
        full_data = header + data

        return full_data.hex()

    def write(self, song: Song) -> XMLElement:
        """Crafts the XMLElement CONFIGURATION, for the .dvc file.

        Args:
            song (Song): Song for which to create the configuration. Currently ignored.
        """

        touch_dock_manager_data = f"""
        <?xml version="1.0" encoding="UTF-8"?>
        <QtAdvancedDockingSystem Version="1" UserVersion="0" Containers="0">
        </QtAdvancedDockingSystem>"""

        data: dict = Conf()['export']['daslight5']['configuration']

        attribs = {
            "VIEWZOOM": data['VIEWZOOM'],
            "VIEWPOSX": data['VIEWPOSX'],
            "VIEWPOSY": data['VIEWPOSY'],
            "TOUCH_DOCK_MANAGER": self._deflate_touchdock(touch_dock_manager_data),
            "TOUCH_ZOOMS": data['TOUCH_ZOOMS'],
        }

        ret: XMLElement = create_element("CONFIGURATION", attribs)

        return ret
