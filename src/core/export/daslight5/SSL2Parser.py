from pathlib import Path
from typing import List
import lxml.etree as etree
from lxml.etree import _Element as XMLElement
from lxml.etree import XPathEvalError

from ....lib.ARACrypt import ARACrypt as Crypt


class SSL2Parser():
    """Class to parse .ssl2 files. Provides methods to access the underlying XML structure.
    """

    def __init__(self, keyFile_path: Path | str) -> None:
        """Instantiates the class for a specific file.

        Args:
            keyFile_path (Path | str): Path to the file containing the decryption key.
        """
        self.crypt: Crypt = Crypt()

        # Loading key from file
        with open(keyFile_path, 'rb') as keyfile:
            self.key = keyfile.read()

    def load(self, path: str | Path) -> None:
        """Loads an .ssl2 file.

        Args:
            path (str | Path): Path to the .ssl2 file.
        """
        with open(path, 'rb') as ssl_file:
            # Decrypting SSL with the key
            decrypted: bytearray = self.crypt.transform_bytes(
                self.key, ssl_file.read())
            # Parsing bytearray as XML
            self.xml: XMLElement = etree.fromstring(bytes(decrypted), None)

    # ---------------------------------------------------------------------------

    def parse(self, x_path: str) -> str:
        """Parses an XPath expression, and returns the result as a string. If the result is a list, returns the first entry.

        Args:
            x_path (str): String containing a valid XPath expression.

        Raises:
            ValueError: When no file is loaded, or when an evaluation error is raised due to an invalid XPath expression.

        Returns:
            str: The result of the XPath expression evaluation.
        """
        if self.xml is None:
            raise ValueError('No file loaded!')

        try:
            ret = self.xml.xpath(x_path)
        except XPathEvalError:
            raise ValueError('Invalid expression')

        # TODO: This could be improved by allowing to return a list as well as a str.
        if isinstance(ret, list):
            ret = ret[0]
        return str(ret)

    # ---------------------------------------------------------------------------

    def get(self, x_path: str) -> XMLElement | List[XMLElement]:
        """Parses an XPath expression, and returns the result as an XMLElement.

        Args:
            x_path (str): String containing a valid XPath expression.

        Raises:
            ValueError: When no file is loaded, or when an evaluation error is raised due to an invalid XPath expression.

        Returns:
            XMLElement | List[XMLElement]: The result of the XPath expression evaluation.
        """
        if self.xml is None:
            raise ValueError('No file loaded!')

        try:
            ret = self.xml.xpath(x_path)
        except XPathEvalError:
            raise ValueError('Invalid expression')

        if isinstance(ret, list) and len(ret) == 1:
            ret = ret[0]
        return ret
