from pathlib import Path
import lxml.etree as etree
from lxml.etree import _Element as XMLElement

from ARACrypt import ARACrypt as Crypt

KEY_FILE = r'src/core/export/daslight5/key'

# TODO: Build this class


class SSL2Parser():

    def __init__(self):
        self.crypt = Crypt()

        # Loading key from file
        with open(KEY_FILE, 'rb') as keyfile:
            self.key = keyfile.read()

    def load(self, path: str | Path) -> None:
        with open(path, 'rb') as ssl_file:
            # Decrypting SSL witht the key
            decrypted: bytearray = self.crypt.transform_bytes(
                self.key, ssl_file.read())
        # Parsing bytearray as XML
        self.xml: XMLElement = etree.fromstring(bytes(decrypted))

    def parse(self, x_path: str) -> str:
        ret = self.xml.xpath(x_path)

        if isinstance(ret, list):
            ret = ret[0]
        return str(ret)

    def get(self, x_path: str) -> XMLElement | list[XMLElement]:
        ret = self.xml.xpath(x_path)

        if isinstance(ret, list) and len(ret) == 1:
            ret = ret[0]
        return ret
