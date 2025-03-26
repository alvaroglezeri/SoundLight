from abc import ABC
from uuid import uuid4


class IFixture(ABC):
    def __init__(self) -> None:
        super().__init__()


class ParCan(IFixture):
    def __init__(self) -> None:
        super().__init__()


class MovHead(IFixture):
    def __init__(self) -> None:
        super().__init__()


class RGBW(IFixture):
    def __init__(self) -> None:
        super().__init__()
