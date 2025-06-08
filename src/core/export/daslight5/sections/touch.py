from lxml.etree import _Element as XMLElement

from core.export.daslight5.Daslight5Exporter import create_element, Section
from core.model.song import Song


class Touch(Section):
    """TOUCH element in the DLM file.
    The contents of this section are completely optional, as they are loaded on-the-fly.
    However, the section is kept to allow for the future configuration of buttons.
    """

    def __init__(self, dlmfile: XMLElement):
        ...

    def write(self, song: Song) -> XMLElement:
        ret: XMLElement = create_element('TOUCH')

        return ret
