from abc import ABC, abstractmethod
from enum import Enum

from core.logger import Logger, LOG_CAT
from core.model.fixtures import IFixture


class Group(ABC):
    """_summary_

    """

    def __init__(self, name: str, *fixtures: IFixture) -> None:
        self._name: str = name
        if fixtures is not None:
            self._fixtures: list[IFixture] = list(fixtures)
        else:
            raise ValueError()

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def select(*fixtures: int):
        pass


class LightManager():
    """
    WRITE
    Manages the available fixtures, generates UUIDs, and provides address groups
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance: LightManager = super(LightManager, cls).__new__(cls)
            cls.instance._groups = []
            cls.instance._fixtures = {}
            Logger.log(LOG_CAT.SUCCESS, f'Created Light Manager')
        return cls.instance

    def __init__(self) -> None:
        self._groups: list[Group]
        self._fixtures: dict[type[IFixture], list[IFixture]]

    def __str__(self) -> str:
        fixtures_str: list[str] = []
        for t in self._fixtures.keys():
            fixtures_str.append(
                f'    {t.__name__}: {len(self._fixtures[t])}\n')

        fixtures_str = ''.join(fixtures_str)
        return f'--- LightManager ---\n > Fixtures:\n{fixtures_str}\n > Groups:\n{"-"}'

    # ----------------

    def createFixtures(self, type: type[IFixture], n: int = 1) -> list[IFixture]:
        """
        Registers a new (set of) fixtures
        """
        if type not in self._fixtures or self._fixtures[type] is None:
            self._fixtures[type] = []

        newFixtures = []
        for i in range(n):
            n: IFixture = type()
            newFixtures.append(n)
            self._fixtures[type].append(n)

        return newFixtures

    def registerFixtures(self, *fixtures: IFixture) -> list[IFixture]:
        if self._checkNotExist(fixtures):
            for f in fixtures:
                if type(f) not in self._fixtures or self._fixtures[type(f)] is None:
                    self._fixtures[type(f)] = []
                self._fixtures[type(f)].append(f)

    def addGroup(self, name: str, *fixtures: IFixture) -> None:
        """_summary_

        Args:
            name (str): _description_
        """
        if self._checkExist(fixtures):
            g = Group(name, fixtures)
            self._groups.append(g)

    def _checkExist(self, fixtures: tuple[IFixture]) -> bool:
        for f in fixtures:
            if f not in self._fixtures.values():
                return False
        return True

    def _checkNotExist(self, fixtures: tuple[IFixture]) -> bool:
        for f in fixtures:
            for t in self._fixtures.values():
                if f in t:
                    Logger.log(LOG_CAT.ERROR,
                               f'Fixture already registered: {f.dasuid}')
                    return False
        return True

    # ----------------------------------------------------
