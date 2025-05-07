import zlib
import lxml.etree as etree
from lxml.etree import _Element as XMLElement

from core.model.song import Song
from core.export.daslight5.Daslight5Creator import createElement, Section


class Configuration(Section):

    def __init__(self, dlmfile: XMLElement):
        self.dlmfile = dlmfile

    @staticmethod
    def _deflateTouchDock(element: str | XMLElement) -> str:
        """Returns the encoded, deflated Touch Control data in the correct format
        DOCUMENT
        WRITE

        Args:
            element (str | XMLElement): _description_

        Returns:
            str: _description_
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
        """
        WRITE
        """

        touch_dock_manager_data = f"""
        <?xml version="1.0" encoding="UTF-8"?>
        <QtAdvancedDockingSystem Version="1" UserVersion="0" Containers="0">
        </QtAdvancedDockingSystem>"""

        attribs = {
            "VIEWZOOM": "1",
            "VIEWPOSX": "200",  # Center of the 2D view for 1080p, varies with resolution
            "VIEWPOSY": "100",
            "TOUCH_DOCK_MANAGER": self._deflateTouchDock(touch_dock_manager_data),
            "TOUCH_ZOOMS": "1",
        }

        if song:
           # For now, we can ignore any data in the provided dict
            ...

        ret: XMLElement = createElement("CONFIGURATION", attribs)

        return ret
