from abc import ABC, abstractmethod

# TODO: Apply this models into the patch


class IFixture(ABC):
    def __init__(self, coords: tuple[int, int, int], address: int, universe: int) -> None:
        self._coords: tuple[int, int, int] = coords
        self._address: int = address
        self._universe: int = universe

    def get_coords(self) -> tuple[int, int, int]:
        return self._coords

    def get_address(self) -> int:
        return self._address

    def get_universe(self) -> int:
        return self._universe

    @abstractmethod
    def get_channels(self) -> int:
        ...

# --------------------------------------------------------------------------


class ParCan(IFixture):
    def get_channels(self) -> int:
        return 1


class MovHead(IFixture):
    def get_channels(self) -> int:
        return 12


class RGBW(IFixture):
    def get_channels(self) -> int:
        return 4
