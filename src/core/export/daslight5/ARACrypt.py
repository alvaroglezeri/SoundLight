# ARACrypt implementation (https://www.codeproject.com/articles/2329/aracrypt-a-crypto-class) in Python,
# based on the original source and in the C# implementation by HakanL (https://gist.github.com/HakanL/f67fb9452d086856f105d64bc13a3f46)
# Author: Álvaro G.E. (https://github.com/alvaroglezeri)
# Version: v.1.1


class ARACrypt:
    def __init__(self):
        # Initialising registers
        self.lfsrA: int = 0x13579BDF
        self.lfsrB: int = 0x2468ACE0
        self.lfsrC: int = 0xFDB97531
        self.maskA: int = 0x80000062
        self.maskB: int = 0x40000020
        self.maskC: int = 0x10000002
        self.rot0A: int = 0x7FFFFFFF
        self.rot0B: int = 0x3FFFFFFF
        self.rot0C: int = 0x0FFFFFFF
        self.rot1A: int = 0x80000000
        self.rot1B: int = 0xC0000000
        self.rot1C: int = 0xF0000000
        self.key: bytes = ""

    def _get_key(self) -> str:
        return self.key

    def _set_key(self, key: bytes):
        """Sets the key for the transformation

        Args:
            key (bytes): Key to be used for the transformation. Unlike the original implementation, this does not allow a default key.

        Raises:
            ValueError: When no key is provided.
        """
        if not key:
            raise ValueError("Key cannot be empty")

        self.key = key
        csSeed: bytearray = bytearray(key)

        # Lengthening the key if less than 12 bytes long.
        idx = 0
        while len(csSeed) < 12:
            csSeed += bytes([csSeed[idx]])
            idx += 1

        self.lfsrA = self.lfsrB = self.lfsrC = 0
        for i in range(4):
            self.lfsrA = (self.lfsrA << 8) | csSeed[i + 0]
            self.lfsrB = (self.lfsrB << 8) | csSeed[i + 4]
            self.lfsrC = (self.lfsrC << 8) | csSeed[i + 8]

        if self.lfsrA == 0:
            self.lfsrA = 0x13579BDF
        if self.lfsrB == 0:
            self.lfsrB = 0x2468ACE0
        if self.lfsrC == 0:
            self.lfsrC = 0xFDB97531

    def _transform_byte(self, byte: int) -> int:
        """Performs a single-byte transformation

        Args:
            byte (int): Byte to transform

        Returns:
            int: Transformed byte
        """
        crypto = 0
        outB = self.lfsrB & 0x00000001
        outC = self.lfsrC & 0x00000001

        for _ in range(8):
            if self.lfsrA & 0x00000001:
                # Masking with 0xFFFFFFFF to constrain size
                self.lfsrA = (((self.lfsrA ^ self.maskA) >> 1)
                              | self.rot1A) & 0xFFFFFFFF
                if self.lfsrB & 0x00000001:
                    self.lfsrB = (((self.lfsrB ^ self.maskB) >> 1)
                                  | self.rot1B) & 0xFFFFFFFF
                    outB = 1
                else:
                    self.lfsrB = (self.lfsrB >> 1) & self.rot0B
                    outB = 0
            else:
                self.lfsrA = (self.lfsrA >> 1) & self.rot0A
                if self.lfsrC & 0x00000001:
                    self.lfsrC = (((self.lfsrC ^ self.maskC) >> 1)
                                  | self.rot1C) & 0xFFFFFFFF
                    outC = 1
                else:
                    self.lfsrC = (self.lfsrC >> 1) & self.rot0C
                    outC = 0
            crypto = ((crypto << 1) | (outB ^ outC)) & 0xFF

        ret = byte ^ crypto
        if ret == 0:
            ret = ret ^ crypto

        return ret

    def transform_bytes(self, key: bytes, data: bytes) -> bytes:
        """Performs a transformation on a set of bytes, byte by byte. This works symmetrically as encryption/decryption.

        Args:
            key (bytes): Bytes to use as the encryption/decryption key.
            data (bytes): `bytes` object on which to perform the transformation.

        Returns:
            bytes: Transformed bytes.

        Raises:
            ValueError: When no key is provided.
        """
        if not key:
            raise ValueError("Key cannot be empty.")

        self._set_key(key)

        ret_bytes: bytearray = bytearray()
        b: int
        for b in data:
            ret_bytes.append(self._transform_byte(b))

        return ret_bytes
