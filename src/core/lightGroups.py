from abc import ABC, abstractmethod
from enum import Enum

from core.logger import DCL, LOG_CAT


class IFixture(ABC):
    pass


class Group():
    """_summary_

    """

    def __init__(self, name: str, type: IFixture, units: int) -> None:
        self._name: str = name
        self._type: IFixture = type
        self._units: int = units

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return self._type

    @property
    def units(self) -> str:
        return self._units


class LightManager():
    """
    WRITE
    Manages the available fixtures, generates UUIDs, and provides address groups
    """

    def __init__(self) -> None:
        self._groups: dict = {}
        pass

    def createGroup(self, name: str, type: IFixture, n: int) -> bool:
        """
        Creates a new group of lights as specified
        """

    def group_ParCan(self, *fixtures: int) -> Group:
        pass


class ParCan(Group):
    def __init__(self, *fixtures: int) -> None:
        """
        Creates a ParCan group for the specified fixtures
        """

        if fixtures:
            self._fixtures = list(fixtures)
        else:
            self._fixtures = [1, 2, 3, 4, 5, 6, 7, 8]

    def __str__(self) -> str:
        return f'[ParCan ({[i for i in self._fixtures]})]'


class MovHead(Group):
    def __init__(self) -> None:
        pass


class RGBW(Group):
    def __init__(self) -> None:
        pass
